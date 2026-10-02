---
name: hypothesis-forge
description: Generate non-obvious, duplicate-resistant vulnerability hypotheses for a target by running generators against its specifics, then score each for crowding before any proof effort is spent. Use after recon and BEFORE hunting. This is the step that stops you racing every other hunter's agent to the same findings.
argument-hint: "[component-or-surface]"
---

# Hypothesis Forge

Your competition is a generic agent running a shared playbook. If an idea would occur
to that agent in its first ten guesses, fifty people's agents already submitted it
this week.

**Your job here is not to find bugs. It is to invent questions nobody else is
asking.** Proving comes later and elsewhere.

## The rule that governs this skill

> **Never generate a list of bug classes.** Everyone has that list — OWASP, the
> `hunt-*` packs, the nuclei template set. A shared list produces shared findings,
> and shared findings are duplicates.
>
> Generate by applying **operations to this target's specifics**. The output must be
> impossible to produce without having looked at *this* target.

If a hypothesis you wrote would read identically for a different target, delete it.
It's a bug class, not a hypothesis.

## Before you start

Read, in this order:
1. `scope/<program>.md` — scope, accepted-risk list, test accounts
2. `recon/inventory.md`, `recon/routes.md` — what actually exists
3. `recon/coverage.md` — what's already been hunted (don't re-cover)
4. `findings/rejected.jsonl` — what's already been killed, and why
5. The program's **public disclosures** — these are the crowded ideas. Read them to
   learn what *not* to propose, and to harvest shapes for variant analysis.

### Then seed from the private corpus

Read `corpus/README.md`, then the cluster docs matching your surface under
`corpus/x-bookmarks-2026-09/bb-research/x-bookmarks-2026-09-detailed/` (`01-idor-bola.md`,
`04-llm-hunting-process.md`, `05-mcp-tooling.md`, `10-n-day-patch.md`, …). Also read
`recon/anomalies.md` if it exists — unexplained observations are your highest-value and
most private seed.

**This is the "seed it with your own expertise" move** from
`docs/11-non-obvious-thinking.md` §11.10 — one of only two things that reliably
differentiate a hunter when everyone runs the same models on the same scope.

> **A corpus card is a starting point, never a hypothesis.**

The corpus is distilled from **public** posts thousands of others bookmarked, so a card on
its own is just a bug class — and §11.2 is explicit that working down a list of bug classes
is what produces duplicates. What's unique is the combination:

```
corpus card  ×  a specific observation about THIS target  →  hypothesis
```

For every card you use, name the recon observation that makes it suspicious *here*. If you
can't, you don't have a hypothesis. **Read `corpus/README.md`'s "Known-bad cards" section
first** — five corpus positions contradict `docs/` (breadth-over-narrow, class-checklists,
multi-program parallelism) and must not be imported. Respect the corpus's own `thin` /
`anecdotal` /
`blocked-recovered` labels — those are leads, not facts.

Then run the generators. Aim for **15–25 hypotheses** before scoring any of them.
Quantity first, judgment second — judging too early collapses you onto the obvious.

---

## The generators

Run each. Skip one only if the target genuinely has no such surface, and say so.
Full evidence and attribution for every one is in `docs/11-non-obvious-thinking.md`.

### G0 · Pick the surface, not the bug — do this first
> Mark Dowd: **"The attack surface *is* the vulnerability — finding a bug there is just
> a detail."** · Orange Tsai: **"A good attack surface achieves twice results with half
> the effort."**

Name the architectural surface you are attacking, and *why nobody has named it before*.
If you cannot, you are hunting someone else's surface.

Selection question (zhero): *"What technology/component is often present but rarely
discussed or exploited?"* — maximize **(prevalence in scope) × (minus research
attention)**. The property you want is "almost systematically in-scope."

### G1 · Anomaly ledger — the one input no competitor shares
> Kettle: *"Treat as a lead anything that makes you say **'this makes no sense'**."*
> *"Spotting anomalies is the single most important skill for finding race conditions."*

Read and append to `recon/anomalies.md`. Log every observation you cannot explain, even
when it isn't exploitable today — Kettle's whole race-condition class came from a
**7-year-old** unexplained anomaly. Then ask: *what have I seen that I never explained?*

**Benchmark-then-deviate:** establish normal behaviour quantitatively, then look for any
deviation. Faster than expected ⇒ threading or a short-circuit error path; slower ⇒
locking.

### G2 · Mine the changelog, issue tracker and release notes
> joaxcar: *"Reading through the release blog posts (especially the monthly security
> release) has probably been the most fruitful for me."*

For each disclosed bug: understand the root cause, then **search for edge cases where
developers missed the protection in similar code.** Read the public issue tracker for
features you didn't know existed. Follow docs "version history" → epic → merged MR →
**which files changed** → test there. Read **discussion threads about problems with a
previous fix** — joaxcar found an access-control bug that had been *reintroduced without
the developers realising*.

~3–8% of a program's fixed bugs regress. Near-duplicate-free lane.

### G3 · Variant-hunt every disclosed bug
40–50% of real in-the-wild 0-days are **variants of already-patched bugs**, because
*"the execution flow that the proof-of-concept exploits took were patched, but the root
cause issue was not addressed."*

> **The class is public, but the enumeration of its instances is private.**

Climb the ladder: exact string → same sink different file → same sink different
language/service → same **invariant** different sink → same invariant at a different
**lifecycle stage** → same invariant in a fork, vendored copy, mobile client, or legacy
API version.

### G4 · Build the scanner the paper's author didn't
> Kettle: *"Did the researcher miss anything? Did they release a scanning tool? If not,
> can I make one? Does it detect every vulnerability mentioned in the paper?"*

CL.0 desync was *"overlooked by the community"* precisely because **no tool shipped**.
**The gap between a published technique and a published scanner for it is where
non-duplicate bugs live.**

And the inversion: after a new technique drops, **the most-saturated assets become the
best targets**, because they were cleared under the old technique and nobody re-tests.

### G5 · Lifecycle tracing
`issue → store → transmit → consume → refresh → revoke → audit → export → delete`

Everyone tests **consume**. Prioritize **revoke** (do revocations terminate live
sessions, websockets, in-flight jobs, cached permissions? *"You cannot revoke a
self-contained token; you can only outlive it."*), **refresh**, **export** (does it
re-apply the ACL or dump what the query returns?), **delete**.

Kettle's collision prediction: *identify objects with security controls, then locate
**all** endpoints reading/writing them.*

### G6 · Hunt seams, not components
> **Two components can each be individually correct and the seam still be exploitable —
> which is exactly why single-component scanners never see it.**

proxy↔origin · CDN↔app · framework↔runtime · ORM↔DB · serializer↔deserializer ·
unicode normalizer↔validator · auth service↔resource service · router↔handler ·
cache↔origin · queue↔consumer.

At each seam: do both sides agree about encoding · length/truncation · type · case ·
normalization · duplicate keys/headers · ordering · identity · time · units?
**What does one side guarantee, and what does the next side assume?**

### G7 · Cross-feature composition
A is safe, B is safe — test **A∘B**. Enumerate feature *pairs* touching the same state or
identity: SSO × invite · export × templating · cache × personalization · impersonation ×
audit · soft-delete × re-invite · rate-limit × retry.

Prioritize this: **a bug requiring two parts seen at once is one that partitioned agents
miss by design.**

### G8 · Workflow / order inversion
> Douglas Day: *"Instead of going through the prescribed workflow … **what if I reverse
> the process?** What would happen if I change some of the data that feeds the engine?"*

Run the intended step order out of order, skip steps, repeat steps, run two orders
concurrently. Also: twice · after a revocation · then undone · partially failed · retried ·
at a boundary (midnight, month end, quota reset, trial expiry).

**Anything with a limit is a race target.**

### G9 · Model the developer's corner-cutting
> Inti: *"**what are the things that they may try to cut corners on because it's not
> super relevant to their business?**"*

Rank features by **(security consequence) ÷ (business centrality)**; hunt the
high-consequence / low-centrality quadrant. Read *all* the docs and API docs. **Read
their job postings** — they reveal where the company puts its resources.

Related: treat each control as a *confession* of what the team believed the attack was,
then ask what other path reaches the same asset without that control on it.

### G10 · The boring/hard-stuff filter
> Rosén: **"Focus on BORING/HARD STUFF, other hackers won't."** · zhero: *"Move toward
> what others avoid."* · Kettle: *"If a technique has a reputation for being difficult,
> fiddly, or dangerous, that's a topic in dire need of further research."*

Rosén worked through **all 80 integrations** in the docs → one faulty implementation →
**$20k**. Rank candidate work by how much other hunters would hate doing it.
**Treat inconvenience as a duplicate-rate discount.**

### G11 · Out-of-band sources agents ignore
Agents *"didn't consider accessing this public data source"* (Wiz). A human found an
exposed `/rabbitmq/` in 5 minutes that an agent missed across ~500 tool calls.

GitHub repos and gists · package registries · archived docs (Wayback CDX) · job ads ·
Crunchbase acquisitions · CT logs · app-store binaries · support forums · status pages ·
orphaned git history (zero-commit force-push events).

### G12 · Micro-inspiration against spec text
Feed **1–3 sentence fragments** of RFCs/specs — not whole documents — because *"models
aggressively anchor on all context provided, so every extra sentence of prompt risks
context-contamination."* Ask a narrow high-value question and **explicitly exclude
low-value answers**.

**A standards document is un-mined precisely because reading it is boring.**

### G13 · Cascade (runs after a hit, not during ideation)
After **any** confirmed finding, two mandatory questions:
> **"How can I detect similar behavior elsewhere?"** · **"Does the origin enable other
> attacks?"**

*"When you make a significant research discovery, it may contain a clue to something
conceptually nearby."* **Never submit the first finding unescalated.**

### Prioritization
Highest yield and least-run by others: **G0, G1, G2, G3, G4, G5-revoke, G7, G10.**
G2 and G3 are near-zero-cost and phone-doable — run them first on any target with public
disclosures or release notes.

## Scoring — the Obviousness Filter

Score **every** hypothesis before any proof work. This is a **budget gate**: its job
is to stop you spending proof effort on a race you'll lose.

### Three disqualifying questions
1. Would a generic agent propose this in its first ten ideas?
2. Would a scanner or nuclei template find it?
3. Is it the textbook first move for this surface?

Remember the sharper axis: **how many independent observations are needed before this bug
becomes visible at all?** One observation, no state, no domain knowledge → everyone finds
it.

Any "yes" → the hypothesis starts at a heavy penalty and needs a real angle to survive.

### Crowding score

| Signal | Score |
|---|---|
| A scanner/nuclei template would find it | **+3** |
| Textbook first move for this surface | **+3** |
| Reachable **unauthenticated** | **+2** |
| Surface linked from main UI navigation | **+2** |
| This class already appears in the program's public disclosures | **+2** |
| Single observation — one request/response, no state | **+2** |
| Requires ≥2 chained steps | **−2** |
| Requires knowing what the business actually does | **−3** |
| **Post-authentication, deep feature** | **−2** |
| Requires a non-default account state | **−2** |
| Requires reading JS/source/mobile binary to know it exists | **−2** |
| Feature shipped in last 90 days | **−2** |
| Lives at a seam between subsystems | **−2** |
| API-only, never reachable via UI | **−2** |
| Requires **out-of-band** data (GitHub, archives, job ads, app binary) | **−2** |
| Requires a second tenant to observe | **−1** |
| Other hunters would find the work **tedious** | **−2** |

**Negative total → pursue. Zero or positive → you're racing.** Either find an angle
that makes it non-obvious, or move on.

### Counterweight — don't over-apply this
A real, confirmed critical that scores +2 is still worth reporting. Impact beats
elegance and being first still wins. The score decides **where to spend hunting
time**, never whether to report something real you already proved.

---

## Output

Write `recon/hypotheses.md`. One block per hypothesis, ranked by score ascending (most
non-obvious first).

```
### H07 · Export re-runs the query without the tenant filter
  generator:     G5 lifecycle (export stage) + G3 variant
  seed:          corpus 01-idor-bola #1.5 (internal library wrapper missing caller authz)
  target specific: POST /api/v2/reports/export, seen only in app.bundle.js:4417;
                   no UI entry point. Accepts the same `filter` object as
                   GET /api/v2/reports, which IS tenant-scoped at
                   middleware/tenant.go:88.
  hypothesis:    the export worker builds its own query from `filter` and never
                 passes through the tenant middleware the sync path uses.
  assumption being inverted: "all report reads go through the tenant middleware"
  how to disprove fast: read the export worker's query construction; if it calls
                 the same scoped repository method, this dies immediately.
  oracle if real: tenant A exports with tenant B's filter; output contains
                 CANARY-B-7f3a.
  crowding score: -7   (API-only -2, JS-only discovery -2, needs 2nd tenant -1,
                        un-demoed feature -2)
  cost to check:  low  (one file read)
```

Required fields: `generator`, `target specific` (**the proof you looked at this
target**), `hypothesis`, `how to disprove fast`, `oracle if real`, `crowding score`
with its components, `cost to check`. Add `seed:` when a corpus card or anomaly-ledger
entry informed it — it makes the private-knowledge contribution auditable.

Then a summary table, and an explicit recommendation of the **3–5 to hunt first**,
ordered by `crowding score` then `cost to check` ascending — cheapest disqualifier
first, so you kill bad ideas for pennies.

---

## Discipline

- **Generate before judging.** Score nothing until you have 15+. Early judgment
  collapses you onto the obvious.
- **No bug-class entries.** If it reads identically for another target, it's not a
  hypothesis. Delete it.
- **Weird is the signal, not a problem.** A hypothesis that sounds strange is doing
  its job. Strange ideas are the ones nobody else submitted.
- **Say so when a generator finds nothing.** "G12: no applicable technique published
  recently" is a legitimate, useful output. Don't pad.
- **Never claim a hypothesis is a finding.** You produce questions. The hunter
  investigates; the disprover rules. Confidence language here is a category error.
- **Record the crowded ideas you rejected** in `recon/hypotheses.md` under a
  `## Rejected as crowded` heading, with scores. It stops you or a later run
  re-generating them, and it's evidence of deliberate target selection.
- **Harvest the program's disclosures for shapes, not endpoints.** Abstract each
  disclosed bug to its root-cause shape and ask where else that shape occurs
  (variant analysis). The original is duplicated to death; the variants are not.
