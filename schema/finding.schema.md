# Finding record schema

The contract `findings/*.jsonl` must satisfy. Enforced by
`scripts/validate-findings.py` (stdlib only, no dependencies) and by the `Stop`
hook, so it is a gate rather than a convention.

Design follows [docs/04 §4.2](../docs/04-harness-architecture.md): **distinct required
field sets per verdict, and forbidden fields per verdict**, so that a
`needs_validation` record *cannot* carry a severity. That one property is what stops
speculative leads being laundered into findings.

One JSON object per line. Unknown top-level fields are rejected — the equivalent of
`additionalProperties: false`.

---

## Common fields (every verdict)

| Field | Type | Required | Notes |
|---|---|---|---|
| `verdict` | `"confirmed"` \| `"needs_validation"` \| `"rejected"` | ✅ | drives which other fields are legal |
| `fingerprint` | string | ✅ | stable, source-derived identity for one root cause. `^[A-Za-z0-9][A-Za-z0-9._:/@+-]*$`. **Must not encode** line number, wave, agent, severity or verdict — so the same root cause keeps one identity across states and runs |
| `class` | string | ✅ | `idor`, `bfla`, `ssrf`, `race`, … |
| `location` | string | ✅ | `file:line` or `METHOD /path` |
| `target` | string | ✅ | the in-scope asset |
| `date` | string | ✅ | `YYYY-MM-DD` |
| `crowding` | integer | — | score from the obviousness filter ([docs/11](../docs/11-non-obvious-thinking.md)); negative is good |
| `seed` | string | — | corpus card or anomaly-ledger entry that informed it |
| `cost_usd` | number | — | spend attributable to this candidate, for ROI tracking |

---

## `verdict: "confirmed"`

**Required:** `root_cause`, `trace`, `evidence`, `conditions`, `impact_sentence`,
`severity`, `confidence`, `remediation`, `gate_6_human_reviewed`

**Forbidden:** `claimed_root_cause`, `blockers`, `validation_plan`, `reason`

| Field | Type | Notes |
|---|---|---|
| `trace` | array, ≥2 entries | **first entry `kind` must be `entrypoint`, last must be `sink`**; intermediates `propagation` |
| `evidence` | array, ≥1 | each `{file, line, description}` |
| `conditions` | array | each `{kind, detail, prevalence}`; `prevalence` ∈ `default` \| `common` \| `unusual` |
| `impact_sentence` | string | must contain concrete nouns; the validator rejects the banned hedges |
| `severity` | enum | `informational` \| `low` \| `medium` \| `high` \| `critical` |
| `confidence` | enum | `low` \| `medium` \| `high` |
| `gate_6_human_reviewed` | boolean | **only a human sets this true** |

`trace` entry: `{kind, file, line, scope, description}` with `line` an integer ≥ 1.

---

## `verdict: "needs_validation"`

**Required:** `claimed_root_cause`, `trace`, `evidence`, `blockers`, `validation_plan`

**Forbidden:** `severity`, `confidence`, `execution`, `remediation`, `root_cause`,
`impact_sentence`, `gate_6_human_reviewed`

| Field | Type | Notes |
|---|---|---|
| `blockers` | array of strings, ≥1 | the **exact decisive fact** not obtainable from source or local observation |
| `validation_plan` | object | ≥1 non-empty step under `local` and/or `deployment` |

> **A candidate disproved by source is `rejected`, not `needs_validation`.**
> `needs_validation` is never a parking place for a speculative idea — which is why it
> carries no severity.

---

## `verdict: "rejected"`

**Required:** `claimed_root_cause`, `reason`, `gate_failed`

**Forbidden:** `severity`, `confidence`, `remediation`, `gate_6_human_reviewed`

| Field | Type | Notes |
|---|---|---|
| `reason` | string | the specific thing that failed, with evidence. This is the negative ledger's whole value |
| `gate_failed` | integer 0–8 | which gate killed it; the distribution tells you where your hunting is weakest ([docs/05 §5.6](../docs/05-validation-gates.md)) |
| `reopen_if` | string | — what new evidence would bring it back. *"A kill records what would bring it back."* |

Rejected records are **retained**, so future runs don't repeat an unsupported claim
without changed evidence.

---

## Validate

```bash
python3 scripts/validate-findings.py                     # both default files
python3 scripts/validate-findings.py findings/*.jsonl    # explicit
python3 scripts/validate-findings.py --strict             # also fail on warnings
```

Exit `0` clean, `1` violations found, `2` usage error. The `Stop` hook runs it and
refuses to end a session on malformed findings, or on a report draft built from a
finding no human has reviewed.
