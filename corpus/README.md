# corpus/ — the private seed corpus

> **This directory is the harness's competitive advantage, and it is the one part of
> this repo that cannot be downloaded by anyone else.**

[`docs/11 §11.10`](../docs/11-non-obvious-thinking.md) identifies the two moves that
actually differentiate a hunter in 2026, when everyone is running the same models on the
same scope:

> **1. "Point the agent at niche surface."**
> **2. "Seed it with your own expertise. Feed the prompt your past reports and program
> notes so the agent inherits real program-specific knowledge."**

Everything in `docs/` is synthesized from public research — which means every other
hunter can, in principle, read the same sources. **This directory is move #2.** It is a
curated, privately-assembled idea bank, and feeding it into ideation is what makes this
harness's hypotheses diverge from a generic agent's.

Add to it over time. Its value compounds, and it is the only input your competition
cannot replicate.

---

## What's here

### `x-bookmarks-2026-09/`
A methodology knowledge base distilled from X/Twitter bookmarks across the September 2026
window, merged from three independent extract lanes (Researchy 24 · Researcher 23 · Deep
Research 22 = **69 source items → 68 unique ideas after dedupe**, in 14 clusters).

**Methodology only.** The corpus was built under an explicit constraint — no
reproduction steps, payloads, PoC code, exploit commands, bypass recipes, or weaponized
strings. Verified on ingest: the only matches for payload-shaped patterns are
*classification language* in titles (naming `javascript:` as a scheme, for instance), not
payloads.

| Path | What it is |
|---|---|
| `bb-research/x-bookmarks-2026-09/Bug-Bounty-Ideas-KB.md` | The merged summary KB — one-paragraph idea cards across all 14 clusters |
| `bb-research/x-bookmarks-2026-09-detailed/` | **The useful one.** Per-item cards with root-cause class, affected component, impact, conditions, and abstract teaching. Split by cluster (`01-idor-bola.md` … `14-thin-tangential.md`) |
| `bb-research/x-bookmarks-2026-09-detailed/SOURCES.md` | Every unique source URL with title, lane and quality rating |
| `bb-research/x-bookmarks-2026-09-detailed/00-overview.md` | Stats, the high-diversity reusable patterns, cluster map |
| `bb-research/x-bookmarks-2026-09/deep-research-deep/` · `researcher-deep/` | Deepened lane-native extracts (the longest-form versions) |
| `bb-bookmark-lane-researchy/` · `bug-bounty-corpus/x-bookmark-lane/` · `researcher-lane-extract-2026-10.md` | Raw lane sources of truth, `.md` + `.jsonl` |

**Quality is labelled honestly** in the corpus itself: 6 items marked *thin*, 2
*blocked-recovered* (primary URL gated, content from an alternate summary), several marked
*anecdotal* or *culture signal*. **Respect those labels** — a thin item is a lead, not a
fact.

---

## How the harness uses it

| Consumer | Uses the corpus for |
|---|---|
[`ideator`](../agents/ideator.md) | Reads the cluster docs relevant to the assigned surface, then generates hypotheses that **combine** a corpus idea with this target's specifics. Also harvests root-cause **shapes** for variant hunting. |
| [`hypothesis-forge`](../skills/hypothesis-forge/SKILL.md) | Same, as the skill's documented seed step. |
| [`regression-sweep`](../skills/regression-sweep/SKILL.md) | Cluster `10-n-day-patch.md` for n-day and patch-diff patterns. |
| [`authz-hunt`](../skills/authz-hunt/SKILL.md) | Cluster `01-idor-bola.md` — seven authorization-mismatch cards. |

### The rule that keeps it useful

> **A corpus idea is a starting point, never a hypothesis.**

A corpus card says *"hidden role UUIDs in role-assignment APIs can exceed what the UI
offers."* That is a **bug class** — and per
[`docs/11 §11.2`](../docs/11-non-obvious-thinking.md), working down a list of classes is
precisely what produces duplicates, because this corpus is itself assembled from **public**
posts that thousands of other people also bookmarked.

The value is not the idea. The value is **the idea applied to a specific observation about
this target** — which nobody else's agent will make, because they don't have your recon
and they aren't combining the two.

So: `corpus card × this target's specifics → hypothesis`. Never `corpus card → report`.

---

## Growing it

The corpus gets more valuable the more private it becomes. Highest-value additions, in
order:

1. **Your own resolved reports.** The single best seed — your real findings, with their
   root causes abstracted. (Keep these out of git if they're under NDA; see
   `.gitignore`.)
2. **Your anomaly ledger** (`recon/anomalies.md`, gitignored) — every observation you
   couldn't explain. Per [`docs/11 §G1`](../docs/11-non-obvious-thinking.md), Kettle's
   entire race-condition class came from a 7-year-old unexplained anomaly. **This log is
   private by construction, so it is the one input no competitor shares.**
3. **Per-program notes** — architecture you've reverse-engineered, their conventions,
   their past fixes, which defenses they've added over time.
4. **Negative results** — `findings/rejected.jsonl` kill reasons, so ideation stops
   re-proposing dead ends.

### Keep a clean provenance boundary

Vendored third-party material stays in `corpus/` with its original structure and receipts
intact, **unmodified**. Your own notes and reports are engagement data: they belong in
the gitignored working directories (`scope/`, `findings/`, `recon/`, `reports/`), or in a
private corpus subdirectory you add to `.gitignore` yourself.

Don't edit the vendored lane files — their value is partly that they're a faithful,
dated, auditable record.
