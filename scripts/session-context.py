#!/usr/bin/env python3
"""
SessionStart hook: re-inject durable harness state into context.

Agent context is lossy — it compacts, it resets, sessions end. The ledgers on disk
are the source of truth. This hook puts a summary of them back in front of the
model at every session start and resume, so a new session knows what is in scope,
what has already been covered, and what has already been killed.

Emits JSON with hookSpecificOutput.additionalContext. Never blocks.
"""

from __future__ import annotations

import json
import os
import sys

MAX_REJECTED = 25
MAX_LINES = 120


def read_lines(path: str, limit: int | None = None) -> list[str]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            lines = [ln.rstrip("\n") for ln in fh if ln.strip()]
    except OSError:
        return []
    return lines[-limit:] if limit else lines


def read_jsonl(path: str, limit: int) -> list[dict]:
    out: list[dict] = []
    for line in read_lines(path):
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out[-limit:]


def main() -> None:
    raw = sys.stdin.read()
    try:
        event = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        event = {}

    root = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()
    parts: list[str] = []

    # --- scope ---
    allowlist = os.path.join(root, "scope", "allowlist.txt")
    hosts = [h for h in read_lines(allowlist) if not h.startswith("#")]
    if hosts:
        parts.append(
            "## Active scope allowlist (hook-enforced)\n"
            + "\n".join(f"- {h}" for h in hosts[:40])
            + "\n\nAny host not matching these is HARD BLOCKED by the scope-guard "
              "PreToolUse hook. Do not attempt to work around it; if an asset is "
              "genuinely in scope, re-verify the program policy and add it."
        )
    else:
        parts.append(
            "## Active scope allowlist\n"
            "**NONE CONFIGURED.** All outbound network tool calls are blocked until "
            "`scope/allowlist.txt` exists. Run the `scope-guard` skill to build it "
            "from the program policy before any testing."
        )

    # --- coverage ledger ---
    coverage = os.path.join(root, "recon", "coverage.md")
    cov_lines = read_lines(coverage, MAX_LINES)
    if cov_lines:
        # Count data rows only: skip the markdown header row and the |---|---| rule.
        data_rows = [
            ln
            for ln in cov_lines
            if ln.lstrip().startswith("|")
            and set(ln.replace("|", "").replace(" ", "")) != {"-"}
            and "Component" not in ln
        ]
        not_yet = sum(1 for ln in data_rows if "NOT YET" in ln)
        parts.append(
            f"## Coverage ledger (`recon/coverage.md`)\n"
            f"{len(data_rows)} surface(s) tracked, {not_yet} not yet hunted. "
            "Treat one pass as roughly 50% recall — repeated runs are only additive "
            "if you update this file. Pick unhunted surfaces first."
        )

    # --- anomaly ledger (highest-value private seed) ---
    anomalies = [
        # strip any existing markdown bullet so we don't render "- - item"
        ln.lstrip().lstrip("-*").strip()
        for ln in read_lines(os.path.join(root, "recon", "anomalies.md"), MAX_LINES)
        if not ln.lstrip().startswith("#")
    ]
    anomalies = [ln for ln in anomalies if ln]
    if anomalies:
        parts.append(
            f"## Anomaly ledger — {len(anomalies)} unexplained observation(s)\n"
            + "\n".join(f"- {ln}" for ln in anomalies[-15:])
            + "\n\nThese are observations nobody could explain. They are private by "
              "construction, so they are the one ideation seed no competitor shares — "
              "an unexplained anomaly became an entire new bug class for one researcher "
              "seven years later. Revisit them when ideating, and never prune the file."
        )

    # --- negative ledger ---
    rejected = read_jsonl(os.path.join(root, "findings", "rejected.jsonl"), MAX_REJECTED)
    if rejected:
        lines = []
        for r in rejected:
            cls = r.get("class", "?")
            loc = r.get("location", "?")
            reason = (r.get("kill_reason") or "?")[:140]
            lines.append(f"- [{cls}] {loc} — KILLED: {reason}")
        parts.append(
            "## Already killed — do NOT re-propose these (negative ledger)\n"
            + "\n".join(lines)
            + "\n\nRe-proposing a killed candidate with the same kill reason wastes "
              "validation budget. If you believe a kill was wrong, say why the "
              "evidence changed."
        )

    # --- confirmed awaiting human review ---
    confirmed = read_jsonl(os.path.join(root, "findings", "confirmed.jsonl"), 25)
    unreviewed = [c for c in confirmed if not c.get("gate_6_human_reviewed")]
    if unreviewed:
        parts.append(
            f"## {len(unreviewed)} CONFIRMED finding(s) awaiting human review (Gate 6)\n"
            + "\n".join(
                f"- [{c.get('class','?')}] {c.get('location','?')}" for c in unreviewed
            )
            + "\n\nThese must be read by a human before any report is drafted or "
              "submitted. Do not submit anything yourself."
        )

    if not parts:
        sys.exit(0)

    header = (
        "# bb-harness state\n"
        "Authorized bug bounty testing only.\n"
        "- Originality decides what to hunt: seed ideation from `corpus/` and "
        "`recon/anomalies.md`, and score crowding BEFORE spending proof budget.\n"
        "- Validation decides what to submit: a candidate is not a finding until the "
        "disprove ladder passes and a human has reviewed it.\n"
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": header + "\n" + "\n\n".join(parts),
                }
            }
        )
    )
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - observational hook must never break a session
        sys.stderr.write(f"[session-context] {exc}\n")
        sys.exit(0)
