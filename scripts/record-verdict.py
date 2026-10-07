#!/usr/bin/env python3
"""
Record a disprover verdict as a schema-valid line in findings/*.jsonl.

The disprover returns a verdict; it never writes the ledger. The orchestrator (or the
human) turns that verdict into a record with this script, which validates the record
with scripts/validate-findings.py before appending it, so a malformed line can never
reach the ledger.

Usage:
    python3 scripts/record-verdict.py record.json            # one record (object) or several (array)
    python3 scripts/record-verdict.py - < record.json

The input is the record itself, in the schema from schema/finding.schema.md. Convenience
normalisations applied before validation:
    * `verdict` is lower-cased ("CONFIRMED" -> "confirmed")
    * a disprover label is mapped: FALSE/UNPROVEN/NO_IMPACT -> rejected (a note is kept in
      `reason` if `reason` is missing)
    * `gate_failed` given as "gate_3_impact" / "Gate 3" is reduced to the integer 3
    * `gate_6_human_reviewed` is forced to false on confirmed records (only a human may set it)
Records go to findings/confirmed.jsonl or findings/rejected.jsonl by verdict
(`needs_validation` records also go to rejected.jsonl's sibling, findings/needs_validation.jsonl).
Exit 0 on success, 1 when validation fails (nothing is written).
"""
from __future__ import annotations
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib
vf = importlib.import_module("validate-findings")  # type: ignore

ROOT = os.path.dirname(HERE)
TARGETS = {
    "confirmed": os.path.join(ROOT, "findings", "confirmed.jsonl"),
    "rejected": os.path.join(ROOT, "findings", "rejected.jsonl"),
    "needs_validation": os.path.join(ROOT, "findings", "needs_validation.jsonl"),
}
LABEL_MAP = {"false": "rejected", "unproven": "rejected", "no_impact": "rejected", "confirmed": "confirmed"}


def normalise(rec: dict) -> dict:
    v = str(rec.get("verdict", "")).strip().lower()
    if v in LABEL_MAP:
        label = v
        v = LABEL_MAP[v]
        if v == "rejected" and "reason" not in rec:
            rec["reason"] = f"disprover verdict {label.upper()}"
    rec["verdict"] = v
    g = rec.get("gate_failed")
    if isinstance(g, str):
        m = re.search(r"(\d)", g)
        if m:
            rec["gate_failed"] = int(m.group(1))
    if v == "confirmed":
        rec["gate_6_human_reviewed"] = False
    return rec


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    raw = sys.stdin.read() if argv[1] == "-" else open(argv[1]).read()
    data = json.loads(raw)
    recs = data if isinstance(data, list) else [data]
    recs = [normalise(r) for r in recs]
    problems = vf.Problems()
    for i, r in enumerate(recs):
        vf.validate_record(r, f"record[{i}]", problems)
    if problems.errors:
        for e in problems.errors:
            print("ERROR ", e)
        print("nothing written")
        return 1
    for w in problems.warnings:
        print("WARN  ", w)
    for r in recs:
        path = TARGETS[r["verdict"]]
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a") as fh:
            fh.write(json.dumps(r) + "\n")
        print(f"recorded {r['verdict']} -> {os.path.relpath(path, ROOT)}  ({r.get('fingerprint')})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
