#!/usr/bin/env python3
"""
Stop hook: refuse to end a session with broken findings artifacts.

docs/04 §4.6 says guarantees belong in hooks and preferences belong in prompts.
Two of the harness's rules were prompt-only until now, which means they were
requests rather than controls:

  1. findings/*.jsonl must satisfy schema/finding.schema.md
  2. a report draft may only exist for a finding a HUMAN has reviewed
     (CLAUDE.md non-negotiables #1 and #2)

This enforces both at session end.

Deliberately NOT enforced: the mere existence of unreviewed confirmed findings.
That is the normal, correct resting state of a campaign -- findings sit waiting for
the researcher to read them. Blocking on it would make every session unendable.
The violation is a *report drafted from* an unreviewed finding.

Loop safety: Claude Code sets `stop_hook_active` when a Stop hook already fired for
this turn. We allow in that case, so a persistent problem cannot trap the session.
Say what is wrong once and let the human act.
"""

from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys

MAX_REPORT_BYTES = 2_000_000


def allow() -> None:
    sys.exit(0)


def block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.stderr.write(reason + "\n")
    sys.exit(2)


def _read_jsonl(path: str) -> list[dict]:
    out: list[dict] = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for raw in fh:
                if raw.strip():
                    try:
                        rec = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(rec, dict):
                        out.append(rec)
    except OSError:
        pass
    return out


def main() -> None:
    raw = sys.stdin.read()
    try:
        event = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        allow()  # never trap a session over our own parse failure
        return

    # Already blocked once this turn -- don't loop.
    if event.get("stop_hook_active"):
        allow()
        return

    root = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()
    findings_dir = os.path.join(root, "findings")
    reports_dir = os.path.join(root, "reports")

    if not os.path.isdir(findings_dir):
        allow()  # no campaign in progress
        return

    problems: list[str] = []

    # --- 1. schema validation -------------------------------------------------
    validator = os.path.join(root, "scripts", "validate-findings.py")
    if not os.path.exists(validator):
        validator = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "validate-findings.py")
    if os.path.exists(validator):
        try:
            proc = subprocess.run(
                [sys.executable, validator],
                capture_output=True, text=True, timeout=30,
                cwd=root, env={**os.environ, "CLAUDE_PROJECT_DIR": root},
            )
            if proc.returncode == 1:
                detail = (proc.stdout or proc.stderr or "").strip()
                problems.append(
                    "findings/*.jsonl violate schema/finding.schema.md:\n"
                    + "\n".join(detail.splitlines()[:25])
                )
        except (OSError, subprocess.SubprocessError) as exc:
            problems.append(f"could not run the findings validator: {exc}")

    # --- 2. report drafted from an unreviewed finding --------------------------
    confirmed = _read_jsonl(os.path.join(findings_dir, "confirmed.jsonl"))
    unreviewed = {
        str(r.get("fingerprint") or r.get("location") or "")
        for r in confirmed
        if r.get("gate_6_human_reviewed") is not True
    }
    unreviewed.discard("")

    if unreviewed and os.path.isdir(reports_dir):
        offenders: list[str] = []
        for path in glob.glob(os.path.join(reports_dir, "**", "*"), recursive=True):
            if not os.path.isfile(path):
                continue
            try:
                if os.path.getsize(path) > MAX_REPORT_BYTES:
                    continue
                body = open(path, "r", encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            for ident in unreviewed:
                if ident and re.search(re.escape(ident), body):
                    offenders.append(f"{os.path.relpath(path, root)} references {ident!r}")
                    break
        if offenders:
            problems.append(
                "report draft(s) exist for finding(s) no human has reviewed "
                "(gate_6_human_reviewed is not true):\n  "
                + "\n  ".join(offenders[:10])
                + "\n\nGate 6 is the one gate that is never automated. A human reads the "
                  "finding, then sets gate_6_human_reviewed: true. Only you can do that "
                  "-- the agent must not."
            )

    if problems:
        block(
            "bb-harness stop-gate blocked session end:\n\n"
            + "\n\n".join(f"- {p}" for p in problems)
            + "\n\nFix the above, or end the session again to override (this hook "
              "does not fire twice in a row)."
        )
        return

    allow()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - must never trap a session
        sys.stderr.write(f"[stop-gate] internal error, allowing: {exc}\n")
        sys.exit(0)
