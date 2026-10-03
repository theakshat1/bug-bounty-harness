#!/usr/bin/env python3
"""
Zero-dependency validator for findings/*.jsonl.

The harness's doctrine (docs/04 §4.2) is that verdict schemas should be enforced by
code, with distinct required AND FORBIDDEN field sets per verdict, so that a
`needs_validation` record cannot carry a severity. This is that enforcement.

Contract: schema/finding.schema.md

Usage:
    python3 scripts/validate-findings.py [FILE ...] [--strict] [--quiet]

    No FILE arguments -> validates findings/confirmed.jsonl and
    findings/rejected.jsonl if they exist.

Exit codes:
    0  clean (warnings allowed unless --strict)
    1  violations found
    2  usage error
"""

from __future__ import annotations

import json
import os
import re
import sys

VERDICTS = ("confirmed", "needs_validation", "rejected")

COMMON_REQUIRED = ("verdict", "fingerprint", "class", "location", "target", "date")

REQUIRED = {
    "confirmed": (
        "root_cause", "trace", "evidence", "conditions", "impact_sentence",
        "severity", "confidence", "remediation", "gate_6_human_reviewed",
    ),
    "needs_validation": (
        "claimed_root_cause", "trace", "evidence", "blockers", "validation_plan",
    ),
    "rejected": ("claimed_root_cause", "reason", "gate_failed"),
}

FORBIDDEN = {
    "confirmed": ("claimed_root_cause", "blockers", "validation_plan", "reason"),
    "needs_validation": (
        "severity", "confidence", "execution", "remediation", "root_cause",
        "impact_sentence", "gate_6_human_reviewed",
    ),
    "rejected": ("severity", "confidence", "remediation", "gate_6_human_reviewed"),
}

OPTIONAL_COMMON = ("crowding", "seed", "cost_usd", "reopen_if", "notes", "run")

SEVERITIES = ("informational", "low", "medium", "high", "critical")
CONFIDENCES = ("low", "medium", "high")
PREVALENCES = ("default", "common", "unusual")
TRACE_KINDS = ("entrypoint", "propagation", "sink")

_FINGERPRINT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]*$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# A fingerprint must identify a root cause, not a moment in a run.
_FINGERPRINT_BANNED = ("wave", "agent", "severity", "verdict", "line")

# Hedges that mean the claim is not actually established (CLAUDE.md "Writing honestly").
_HEDGES = (
    "likely", "presumably", "probably", "appears to", "could potentially",
    "an attacker might", "in theory", "should be possible", "may be able to",
)


class Problems:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def _check_trace(rec: dict, where: str, p: Problems) -> None:
    trace = rec.get("trace")
    if not isinstance(trace, list) or len(trace) < 2:
        p.err(where, "trace must be a list of at least 2 entries (entrypoint -> sink)")
        return
    for i, hop in enumerate(trace):
        if not isinstance(hop, dict):
            p.err(where, f"trace[{i}] must be an object")
            continue
        kind = hop.get("kind")
        if kind not in TRACE_KINDS:
            p.err(where, f"trace[{i}].kind must be one of {TRACE_KINDS}, got {kind!r}")
        for field in ("file", "description"):
            if not isinstance(hop.get(field), str) or not hop.get(field):
                p.err(where, f"trace[{i}].{field} must be a non-empty string")
        line = hop.get("line")
        if not isinstance(line, int) or isinstance(line, bool) or line < 1:
            p.err(where, f"trace[{i}].line must be an integer >= 1, got {line!r}")
    if isinstance(trace[0], dict) and trace[0].get("kind") != "entrypoint":
        p.err(where, "trace[0].kind must be 'entrypoint' -- a chain must start at a "
                     "real lower-trust entry point (Gate 2)")
    if isinstance(trace[-1], dict) and trace[-1].get("kind") != "sink":
        p.err(where, "last trace entry .kind must be 'sink'")


def _check_evidence(rec: dict, where: str, p: Problems) -> None:
    ev = rec.get("evidence")
    if not isinstance(ev, list) or not ev:
        p.err(where, "evidence must be a non-empty list")
        return
    for i, item in enumerate(ev):
        if not isinstance(item, dict):
            p.err(where, f"evidence[{i}] must be an object")
            continue
        for field in ("file", "description"):
            if not isinstance(item.get(field), str) or not item.get(field):
                p.err(where, f"evidence[{i}].{field} must be a non-empty string")


def _check_confirmed(rec: dict, where: str, p: Problems) -> None:
    sev = rec.get("severity")
    if sev not in SEVERITIES:
        p.err(where, f"severity must be one of {SEVERITIES}, got {sev!r}")
    conf = rec.get("confidence")
    if conf not in CONFIDENCES:
        p.err(where, f"confidence must be one of {CONFIDENCES}, got {conf!r}")

    if not isinstance(rec.get("gate_6_human_reviewed"), bool):
        p.err(where, "gate_6_human_reviewed must be a boolean")

    impact = rec.get("impact_sentence")
    if not isinstance(impact, str) or len(impact.split()) < 6:
        p.err(where, "impact_sentence must be a sentence naming who can do what to "
                     "whose asset (Gate 3)")
    elif found := [h for h in _HEDGES if h in impact.lower()]:
        p.err(where, f"impact_sentence contains hedge(s) {found} -- a hedged impact "
                     "means the verdict is not 'confirmed'")

    conds = rec.get("conditions")
    if not isinstance(conds, list):
        p.err(where, "conditions must be a list (may be empty only if truly none)")
    else:
        for i, c in enumerate(conds):
            if not isinstance(c, dict):
                p.err(where, f"conditions[{i}] must be an object")
                continue
            if c.get("prevalence") not in PREVALENCES:
                p.err(where, f"conditions[{i}].prevalence must be one of "
                             f"{PREVALENCES}, got {c.get('prevalence')!r}")

    _check_trace(rec, where, p)
    _check_evidence(rec, where, p)


def _check_needs_validation(rec: dict, where: str, p: Problems) -> None:
    blockers = rec.get("blockers")
    if not isinstance(blockers, list) or not blockers or not all(
        isinstance(b, str) and b.strip() for b in blockers
    ):
        p.err(where, "blockers must be a non-empty list of non-empty strings naming "
                     "the exact decisive fact that is not observable")
    plan = rec.get("validation_plan")
    if not isinstance(plan, dict):
        p.err(where, "validation_plan must be an object with 'local' and/or "
                     "'deployment' steps")
    else:
        steps = []
        for k in ("local", "deployment"):
            v = plan.get(k)
            if isinstance(v, list):
                steps += [s for s in v if isinstance(s, str) and s.strip()]
            elif isinstance(v, str) and v.strip():
                steps.append(v)
        if not steps:
            p.err(where, "validation_plan needs at least one concrete step under "
                         "'local' or 'deployment'")
    _check_trace(rec, where, p)
    _check_evidence(rec, where, p)


def _check_rejected(rec: dict, where: str, p: Problems) -> None:
    reason = rec.get("reason")
    if not isinstance(reason, str) or len(reason.split()) < 3:
        p.err(where, "reason must state specifically what failed -- the negative "
                     "ledger's whole value is the kill reason")
    gate = rec.get("gate_failed")
    if not isinstance(gate, int) or isinstance(gate, bool) or not 0 <= gate <= 8:
        p.err(where, f"gate_failed must be an integer 0-8, got {gate!r}")
    if "reopen_if" not in rec:
        p.warn(where, "no 'reopen_if' -- a kill is more useful when it records what "
                      "evidence would bring it back")


def validate_record(rec: dict, where: str, p: Problems) -> None:
    if not isinstance(rec, dict):
        p.err(where, "record must be a JSON object")
        return

    verdict = rec.get("verdict")
    if verdict not in VERDICTS:
        p.err(where, f"verdict must be one of {VERDICTS}, got {verdict!r}")
        return

    for field in COMMON_REQUIRED:
        if field not in rec:
            p.err(where, f"missing required field {field!r}")

    for field in REQUIRED[verdict]:
        if field not in rec:
            p.err(where, f"verdict '{verdict}' requires field {field!r}")

    for field in FORBIDDEN[verdict]:
        if field in rec:
            p.err(where, f"verdict '{verdict}' must NOT carry {field!r} "
                         "(see schema/finding.schema.md)")

    allowed = set(COMMON_REQUIRED) | set(OPTIONAL_COMMON) | set(REQUIRED[verdict])
    for field in rec:
        if field not in allowed:
            p.err(where, f"unknown field {field!r} (schema is closed)")

    fp = rec.get("fingerprint")
    if isinstance(fp, str):
        if not _FINGERPRINT_RE.match(fp):
            p.err(where, f"fingerprint {fp!r} must match {_FINGERPRINT_RE.pattern}")
        if bad := [b for b in _FINGERPRINT_BANNED if b in fp.lower()]:
            p.warn(where, f"fingerprint contains {bad} -- it should identify a root "
                          "cause, not a run position, so it stays stable across states")
    elif fp is not None:
        p.err(where, "fingerprint must be a string")

    date = rec.get("date")
    if isinstance(date, str) and not _DATE_RE.match(date):
        p.err(where, f"date {date!r} must be YYYY-MM-DD")

    crowd = rec.get("crowding")
    if crowd is not None and (not isinstance(crowd, int) or isinstance(crowd, bool)):
        p.err(where, f"crowding must be an integer, got {crowd!r}")

    if verdict == "confirmed":
        _check_confirmed(rec, where, p)
    elif verdict == "needs_validation":
        _check_needs_validation(rec, where, p)
    else:
        _check_rejected(rec, where, p)


def validate_file(path: str, p: Problems) -> int:
    count = 0
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for lineno, raw in enumerate(fh, 1):
                if not raw.strip():
                    continue
                where = f"{path}:{lineno}"
                try:
                    rec = json.loads(raw)
                except json.JSONDecodeError as exc:
                    p.err(where, f"invalid JSON: {exc.msg}")
                    continue
                validate_record(rec, where, p)
                count += 1
    except OSError as exc:
        p.err(path, f"cannot read: {exc}")
    return count


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    quiet = "--quiet" in argv
    files = [a for a in argv if not a.startswith("--")]

    if not files:
        root = os.environ.get("CLAUDE_PROJECT_DIR", ".")
        files = [
            os.path.join(root, "findings", name)
            for name in ("confirmed.jsonl", "needs_validation.jsonl", "rejected.jsonl")
        ]
        files = [f for f in files if os.path.exists(f)]
        if not files:
            if not quiet:
                print("no findings files yet -- nothing to validate")
            return 0

    p = Problems()
    total = sum(validate_file(f, p) for f in files)

    if not quiet:
        for e in p.errors:
            print(f"ERROR  {e}")
        for w in p.warnings:
            print(f"WARN   {w}")
        status = "FAIL" if p.errors or (strict and p.warnings) else "OK"
        print(
            f"\n{status}: {total} record(s) across {len(files)} file(s); "
            f"{len(p.errors)} error(s), {len(p.warnings)} warning(s)"
        )

    if p.errors or (strict and p.warnings):
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(130)
