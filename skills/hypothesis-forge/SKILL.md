---
name: hypothesis-forge
description: Generate non-obvious, duplicate-resistant vulnerability hypotheses for a target by running twelve generators against its specifics, then score each for crowding before any proof effort is spent. Use after recon and BEFORE hunting. This is the step that stops you racing every other hunter's agent to the same findings.
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

Then run the generators. Aim for **15–25 hypotheses** before scoring any of them.
Quantity first, judgment second — judging too early collapses you onto the obvious.

---

## The twelve generators

Run each. Skip one only if the target genuinely has no such surface, and say so.

### G1 · Assumption inversion
List what the system assumes is true, then negate each.

Look for assumptions in: validation code, type signatures, DB constraints, comments,
error messages, UI flows that imply an order, and anything the API accepts without
checking.

Emit: `ASSUMPTION: <x>` → `NEGATION: <y>` → `OBSERVABLE IF BROKEN: <z>`

### G2 · Defended-treasure inversion
Find what the developers **defended** — rate limits, captcha, step-up auth, audit
logging, confirmation emails, extra validation, "DO NOT REMOVE" comments.

Those defenses mark what the team thinks is valuable. Then ask the only question that
matters:

> **They defended path A to this prize. What is path B?**

Password change needs the current password — does *email* change? Admin UI needs MFA —
does the admin *API*? Export is rate-limited — is the *email digest* carrying the same
data? Transfers are audit-logged — are *refunds*?

### G3 · Seam hunting
Enumerate every handoff between two subsystems, then ask whether both sides agree.

Seams: proxy↔app · router↔handler · parser↔validator · validator↔sink · cache↔origin ·
app↔db · service↔service · client↔server · auth layer↔app layer · queue↔consumer ·
frontend normalization↔backend normalization.

Agreement about: encoding · length/truncation · type (scalar vs array vs null) · case ·
unicode normalization · duplicate keys/headers · ordering · identity · time · units.

> The question: **what does one side guarantee, and what does the next side assume?**

Nobody owns a seam, which is why bugs live there. Every entry in PortSwigger's 2025
Top 10 was a seam bug.

### G4 · Lifecycle tracing
For each credential and each object, walk:
`issue → store → transmit → consume → refresh → revoke → audit → export → delete`

Everyone tests **consume**. Prioritize **revoke** (do revocations terminate live
sessions, websockets, in-flight jobs, cached permissions?), **refresh** (does it
re-check authorization or trust the old grant?), **export** (does it re-apply the ACL,
or dump what the query returns?), and **delete** (soft-delete still readable?).

### G5 · Follow the data past the obvious sink
Your input is stored somewhere. Ask **what else reads that store, and does it apply
the same escaping and authorization?**

Derived copies: search indexes · caches (app/CDN/framework-internal) · logs ·
analytics · email and notification templates · PDF/CSV/XLSX exports · webhooks ·
backups/replicas · audit trails · mobile sync · admin dashboards · **support-agent
views** · LLM/RAG context.

### G6 · Second-order and temporal
For each state-changing operation, ask what happens when it is: twice · concurrently ·
out of order · while something else is in flight · after a revocation · then undone ·
partially failed · retried · at a boundary (midnight, month end, quota reset, trial
expiry).

**Heuristic: anything with a limit is a race target.**

### G7 · Cross-feature composition
A is safe, B is safe — test **A∘B**. Enumerate feature pairs touching the same state or
the same identity.

Prioritize this generator: a bug requiring two parts seen at once is a bug that
**partitioned agents miss by design**, which makes it duplicate-resistant against
exactly your competition.

### G8 · Actor × object-state matrix
Build the matrix; look at cells nobody populated.

Actors (the weird ones are the point): anonymous · invited-not-accepted · member ·
admin · owner · **suspended** · **deleted** · **former member** · service account ·
API-key-only · SSO user · local-password user · user in two orgs · mid-migration ·
impersonating staff · partner.

Object states: draft · active · archived · soft-deleted · expired · locked ·
pending-approval · over-quota.

The interesting cell is almost always **weird actor × weird object state.**

### G9 · History as oracle
Changelog, release notes, new JS routes, git history if available.

**Recently shipped = fewer eyes** (cheapest novelty edge there is). Recently fixed =
new code under time pressure, plus unfixed siblings. Reverted commits. `TODO`/`FIXME`/
`HACK` and defensive comments. Migration dual-write windows. Deprecated-but-live paths.

### G10 · The un-demoed feature
What would never appear in a sales demo? Export/print · archive/restore · undo · bulk
import · migration tools · GDPR export · account deletion · billing edges (proration,
refunds, downgrade, failed payment) · admin audit log · email digests · file
preview/thumbnail · deprecation paths · webhook management · API key rotation.

> **If a feature has no screenshot on the marketing site, it probably has no test either.**

### G11 · Scope archaeology
What's in scope that nobody thinks of as the product? Acquired-company infrastructure
(richest seam — different conventions, orphaned ownership) · regional/localized
deployments · mobile-only and desktop-only endpoints · partner portals · status pages ·
docs sites with authenticated sections · developer sandboxes · older API versions ·
non-English surfaces where validation was reimplemented.

### G12 · Fresh technique application
Is there a technique published in the last ~3 months that applies here and that the
crowd hasn't applied yet? Novelty has a half-life; by the time it's a nuclei template
it's a crowding signal, not an opportunity.

---

## Scoring — the Obviousness Filter

Score **every** hypothesis before any proof work. This is a **budget gate**: its job
is to stop you spending proof effort on a race you'll lose.

### Three disqualifying questions
1. Would a generic agent propose this in its first ten ideas?
2. Would a scanner or nuclei template find it?
3. Is it the textbook first move for this surface?

Any "yes" → the hypothesis starts at a heavy penalty and needs a real angle to survive.

### Crowding score

| Signal | Score |
|---|---|
| A scanner/nuclei template would find it | **+3** |
| Textbook first move for this surface | **+3** |
| Surface is linked from main UI navigation | **+2** |
| This class already appears in the program's public disclosures | **+2** |
| Zero auth, zero setup | **+1** |
| Single request, no chain | **+1** |
| Requires ≥2 chained steps | **−2** |
| Requires knowing what the business actually does | **−3** |
| Requires a non-default account state | **−2** |
| Requires reading JS/source/mobile binary to know it exists | **−2** |
| Feature shipped in last 90 days | **−2** |
| Lives at a seam between subsystems | **−2** |
| API-only, never reachable via UI | **−2** |
| Requires a second tenant to observe | **−1** |

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
  generator:     G4 lifecycle (export stage) + G5 derived copy
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
with its components, `cost to check`.

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
