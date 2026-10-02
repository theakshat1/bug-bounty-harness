# 11 — Non-Obvious Thinking (the core principle)

> Every hunter now has an agent. The agents are good at the same things, because
> they were trained on the same disclosed reports and run the same playbooks. So the
> binding constraint on earnings is no longer *coverage* — it is **originality of
> hypothesis**.
>
> This document is the most important one in the knowledge base. The validation
> ladder in [05](./05-validation-gates.md) stops you submitting things that are
> *wrong*. This stops you submitting things that are *already known*.

---

## 11.1 The duplicate is the expensive failure

Two ways a finding dies. They do **not** cost the same.

| Failure | What you spent | What you lost |
|---|---|---|
| **False positive** | hunting + some validation | triage goodwill, signal score |
| **Duplicate** | hunting + validation + proof + **writing** + waiting | **the entire pipeline, for zero** |

A false positive is caught by your own gates, cheaply, before submission. A
duplicate passes **every gate you have** — it's real, it's reachable, it has impact,
you proved it — and still pays nothing. You only discover it after you've spent
everything.

The one public dataset makes the scale clear. XBOW's ~1,060 reports:

```
132  confirmed/resolved
303  triaged
125  under review
208  DUPLICATE          ← full pipeline cost, zero return
209  INFORMATIVE        ← full pipeline cost, zero return
```

**~39% of that output was work done perfectly and paid nothing.** And the same
record shows total earnings under $40,000 since Feb 2024 while ranking #1 on
reputation. Volume and correctness were not the constraint. **Novelty was.**

> **Operating conclusion:** an obvious idea is not merely low-value. It is
> **negative-value** — you pay full cost and collect nothing. Kill obvious ideas
> *before* they consume validation budget, not after.

---

## 11.2 Why a checklist cannot make you original

This is the trap, and it's worth being precise about.

If your method is *"work through a list of bug classes"*, then your output is
approximately the **intersection** of everyone else's output — because everyone has
the same list. The OWASP Top 10, the `hunt-*` skill packs, the popular YouTube
methodology, the nuclei template set: these are **shared** knowledge. Shared
knowledge produces shared findings. Shared findings are duplicates.

Worse, the 2026 skill-pack ecosystem has converged: the 7-Question Gate, `hunt-*`
naming, and `triage-validation` recur **verbatim** across the major packs — one
lineage, copied. If you install a popular pack and run its playbook, you are running
*the same playbook as everyone who installed it.*

**Therefore:** non-obvious ideas cannot come from a list of bugs. They must come
from **generators** — transformations you apply to *this specific target* that
produce hypotheses nobody else's generic pass would produce.

That is what §11.4 is. Not a list of bugs. A list of *operations on the target*.

---

## 11.3 The Obviousness Test (apply before investing)

Before spending validation budget on any candidate, score it. This is **Gate N**,
and it runs **early** — right after a hypothesis is formed, before proof work.

### The three disqualifying questions

1. **Would a generic agent, handed this target and asked to find bugs, propose this
   in its first ten ideas?**
   If yes — fifty other people's agents already did, this week. **Deprioritize.**

2. **Would an off-the-shelf scanner or a nuclei template find this?**
   If yes, it's found continuously by everyone, forever. **Deprioritize.**

3. **Is this the textbook first move for this surface type?**
   (XSS on a search box. IDOR on a numeric ID. SQLi on a filter param. Open redirect
   on `?next=`.) **Deprioritize.**

### The crowding score

Count the signals. Negative total = pursue; positive total = probably a duplicate.

| Signal | Score |
|---|---|
| A scanner/nuclei template would find it | **+3** |
| It's the textbook first move for this surface | **+3** |
| The surface is linked from the main UI navigation | **+2** |
| The class appears in this program's public disclosures already | **+2** |
| Reachable with zero authentication and zero setup | **+1** |
| Single request, no chain | **+1** |
| Requires **≥2 chained steps** | **−2** |
| Requires knowing **what the business actually does** | **−3** |
| Requires a **non-default account state** (suspended, mid-migration, invited-not-accepted, former member, SSO-vs-local) | **−2** |
| Requires reading JS/source/mobile binary to know the surface **exists** | **−2** |
| Feature shipped in the **last 90 days** | **−2** |
| Lives at a **seam between two subsystems** | **−2** |
| Only reachable via API, never the UI | **−2** |
| Requires a **second tenant** to even observe | **−1** |

**Rule of thumb:** if the score isn't negative, you are racing. Either find an angle
that makes it non-obvious, or move on to a better-scoring hypothesis.

### The honest counterweight
A *confirmed critical* that happens to score +2 is still worth submitting — impact
beats elegance, and being first still wins. The score governs **where you spend
hunting time**, not whether you report something real you already proved. Use it to
choose what to hunt next, not to talk yourself out of a finished finding.

---

## 11.4 The twelve generators

These produce target-specific hypotheses. Each takes something you can observe about
the target and transforms it into a question nobody's generic pass asked.

Work them in roughly this order — the early ones are cheapest and highest-yield.

---

### G1 · Assumption extraction and inversion
**Operation:** read the code or probe the behavior, write down what the system
*assumes is true*, then negate each assumption and test the negation.

The assumptions are target-specific, which is exactly why this generates
non-obvious ideas.

| Assumption you'll find | Its negation |
|---|---|
| the tenant in the session matches the tenant in the path | they differ |
| email is immutable once verified | change it mid-flow |
| this webhook fires exactly once | it fires twice, or zero times |
| IDs are opaque to the client | client supplies its own |
| the list is filtered before it's returned | ask for page 10,000 |
| a user belongs to one org | belongs to two, or zero |
| the order of these two calls is fixed | reverse it |
| this value was validated upstream | reach the handler by another route |
| the file was rewritten after scanning | read it during the window |
| the session was invalidated on logout | use the old one |

**Output format:** `ASSUMPTION: <x>. NEGATION: <y>. OBSERVABLE IF BROKEN: <z>.`

---

### G2 · The defended-treasure inversion
**Operation:** find what the developers *defended* — then find an undefended path to
the same prize.

Defenses are a **map to what the team considers valuable**: rate limits, captcha,
step-up auth, audit logging, extra validation, a confirmation email, a feature flag,
a code comment saying "DO NOT REMOVE".

The question is never "can I beat this defense." It is:

> **They defended path A to this prize. What is path B?**

If password change needs the current password, does *email* change? If the admin UI
requires MFA, does the admin *API*? If the export endpoint is rate-limited, is the
*email digest* that contains the same data? If transfers are audit-logged, are
*refunds*?

This is one of the highest-yield generators and almost nobody runs it, because it
requires reading the defenses rather than attacking them.

---

### G3 · Seam hunting (handoffs, not components)
**Operation:** enumerate every place two subsystems hand data to each other, and ask
whether both sides agree about it.

Bugs live at seams because **nobody owns a seam.** Component A's author assumed B
would handle it; B's author assumed A did.

This is not a hunch — it is the unifying lesson of PortSwigger's 2025 Top 10, where
**every single entry** exploited a disagreement between subsystems about parsing,
caching, or normalizing.

Seams to enumerate: proxy↔app · router↔handler · parser↔validator · validator↔sink ·
cache↔origin · app↔database · service↔service · client↔server · frontend
normalization↔backend normalization · auth layer↔application layer · queue↔consumer.

At each seam, do both sides agree about:
**encoding** · **length/truncation** · **type** (scalar vs array vs null) ·
**case** · **unicode normalization** · **duplicate keys/headers** ·
**ordering** · **identity** (who is this?) · **time** (is this still valid?) ·
**units**?

> The sharpest single question here: *"what does one side guarantee, and what does
> the next side assume?"* Where those don't match, there's a bug.

---

### G4 · Lifecycle tracing
**Operation:** stop testing requests; trace *objects and credentials through their
whole life*.

Almost everyone tests the **consume** stage. Walk all of them:

```
issue → store → transmit → consume → refresh → revoke → audit → export → delete
```

For every credential (session, token, API key, magic link, OTP, invite) and every
object (document, account, membership, subscription):

- **issue** — predictable? bound to the requester?
- **store** — where else is it written? logs? cache?
- **transmit** — Referer, URL, third-party analytics?
- **consume** — single-use enforced? (the stage everyone tests)
- **refresh** — does refresh re-check authorization, or trust the old grant?
- **revoke** — **the most under-tested stage.** Does revocation actually terminate
  live sessions, active websockets, in-flight jobs, cached permissions?
- **audit** — is the action logged under the right actor?
- **export** — does export re-apply the ACL, or dump what the query returns?
- **delete** — soft-delete leaving data readable? Deletion of one tenant's object by
  another?

**Revoke, refresh, export and delete are where the money is**, because the happy
path gets all the attention.

---

### G5 · Follow the data past the obvious sink
**Operation:** ask where your input goes *after* the place you can see.

Your value doesn't stop at the response. It propagates into **derived copies**, and
derived copies rarely re-apply the original's controls:

search indexes · caches (app, CDN, framework-internal) · logs · analytics pipelines ·
email and notification templates · PDF/CSV/XLSX exports · webhooks to third parties ·
backups and replicas · audit trails · mobile sync payloads · admin dashboards ·
support-agent views · LLM/RAG context.

The question: **"my input is stored here — what else reads this store, and does it
apply the same escaping/authorization?"**

Stored XSS that only fires in the *support agent's* console. An ACL that's enforced
in the API but not in the search index. A redaction applied to the UI but not the
PDF export. These are non-obvious by construction, because the sink isn't where you
put the input.

---

### G6 · Second-order and temporal
**Operation:** stop asking "can I do X" and start asking what happens to X *in time*.

For every state-changing operation:
- **twice** (idempotency)
- **concurrently** (races — anything with a limit is a target)
- **out of order** (step 3 before step 2)
- **while Y is in flight** (mid-migration, mid-upload, mid-payment)
- **after Z was revoked** (permission cached?)
- **then undone** (does undo restore more than it should?)
- **partially failed** (rollback leaves what behind?)
- **retried** (duplicate side effects?)
- **at a boundary** (midnight, month end, quota reset, trial expiry, DST, leap day)

> The canonical shape: *a check happens, then an act happens, and the world can
> change in between.*

---

### G7 · Cross-feature composition
**Operation:** feature A is safe. Feature B is safe. Test **A∘B**.

Enumerate pairs of features that touch **the same state** or **the same identity**,
then compose them:

- share a document + transfer ownership
- change email + accept an invite
- enable SSO + keep a local password
- bulk import + per-item authorization
- API key scoped to project X + a project move
- delete an account + a pending invite it issued
- downgrade a plan + resources the old plan allowed

This is **compositional risk**, and it is strategically important: it's the class
that produced HackerOne's own critical RCE (three individually-safe commits by
different authors over time), and the prevailing agent architecture — **partition the
repo into context-window-sized chunks** — structurally cannot see it.

> **A bug that requires seeing two parts at once is a bug partitioned agents miss by
> design.** That makes it duplicate-resistant against exactly your competition.

---

### G8 · The full actor × state matrix
**Operation:** don't test "user vs admin." Build the real matrix and look at the
cells nobody populated.

**Actors** — include the weird ones, which is the point:
anonymous · self-registered · invited-but-not-accepted · member · admin · owner ·
**suspended** · **deleted/deactivated** · **former member** · service account ·
API-key-only · SSO user · local-password user · user in two orgs · user mid-migration ·
support/impersonating staff · partner/reseller.

**Object states:** draft · active · archived · soft-deleted · expired · locked ·
pending-approval · mid-migration · over-quota.

**Operations:** create · read · list · update · delete · share · export · transfer ·
restore.

The interesting cells are almost always **a weird actor against a weird object
state** — a suspended user acting on an archived object; a former member restoring a
soft-deleted doc; an invited-not-accepted account listing resources. Nobody builds
that test, so nobody finds that bug.

---

### G9 · Read history as an oracle
**Operation:** use the target's own record of its changes to aim.

- **Recently shipped** (changelog, release notes, new UI strings, new routes in JS) →
  **fewer eyes have seen it.** This is the single cheapest novelty edge available.
- **Recently fixed** → the fix is *new code* written under time pressure; adjacent
  code is suspect; and siblings of the fixed path are often unfixed
  (→ [regression-sweep](../skills/regression-sweep/SKILL.md)).
- **Reverted commits** → something was shipped, broke, and came back. How?
- **`TODO` / `FIXME` / `HACK` / `XXX`** and defensive comments ("don't remove this
  check", "temporary workaround") → the author knew. Believe them.
- **Migrations** → dual-write/dual-read windows, and code that must handle both the
  old and new shape. Fertile.
- **Deprecated-but-live** code paths → weaker auth, not just older features.

---

### G10 · The un-demoed feature
**Operation:** ask what would *never* appear in a sales demo, and go there.

Testers (and agents, and scanners) cluster on the product's showcase. The showcase is
the most-tested surface on any target.

Go instead to: export/print/download · archive and restore · undo · bulk import ·
data migration tools · GDPR/legal data export · account deletion · billing edge cases
(proration, refunds, plan downgrade, failed payment, dunning) · the admin audit log ·
email digests and notification generation · file preview/thumbnail generation ·
deprecation and sunset paths · the status page · developer sandboxes · webhook
management · API key rotation.

> **Heuristic:** if a feature has no screenshot in the marketing site, it probably
> has no test either.

---

### G11 · Scope archaeology
**Operation:** find what's in scope that nobody *thinks of* as the product.

Acquired-company infrastructure (the richest seam — different conventions, different
auth, often orphaned ownership) · regional/localized deployments (`.de`, `.jp`,
`-eu`) · mobile-only and desktop-app-only endpoints · partner and reseller portals ·
status and trust pages · documentation sites with authenticated sections · marketing
tools wired into real SSO · developer sandboxes and demo tenants · internal tools
accidentally exposed · older API versions · non-English surfaces where validation was
reimplemented.

**Localization is systematically under-tested**: validation, encoding and date/number
handling are frequently reimplemented per locale, by different people, at different
times.

---

### G12 · Apply a brand-new technique before the crowd
**Operation:** be early. Novelty has a half-life.

When a genuinely new technique is published, there is a window — weeks to a few
months — where almost nobody has applied it to *your* targets.

Keep a standing watch on: PortSwigger Research and the annual Top 10 ·
Black Hat / DEF CON / OffensiveCon materials · elttam, watchTowr, Assetnote, slcyber,
Doyensec research blogs · security advisories for frameworks your targets use.

2026's clearest example: **HTTP Terminator** published source *and a reusable
blueprint* after Black Hat, having found ~700 vulnerable targets among 30,000
authorized sites. Desync was widely assumed dead; it was merely under-explored.
Anyone who read that post in the first month had a large, temporary edge.

> **Corollary:** the more popular a technique becomes, the worse its duplicate rate.
> By the time it's a nuclei template, it is a crowding signal (+3), not an
> opportunity.

---

## 11.5 Research-driven beats recon-driven

Two ways to hunt:

| | **Recon-driven** | **Research-driven** |
|---|---|---|
| Method | find many targets, apply known techniques | study one technology deeply, discover a new technique |
| Scales with | assets enumerated | understanding |
| Competition | **everyone**, with better automation | almost nobody |
| Duplicate rate | high | low |
| Time to first bug | fast | slow |
| Bug quality | whatever's left | often a **new class** |

Recon-driven hunting is where AI agents are strongest and where you are most
replaceable. **Research-driven hunting is where a human still compounds** — because
a new technique applies to *every* target that uses the technology, and for a while
you're the only one holding it.

**The practical blend:** use agents for recon-driven breadth to pay the bills, and
deliberately spend a fixed fraction of your time (say 20–30%) going deep on one
technology, protocol, or framework your targets share. The deep work is what produces
findings nobody can duplicate.

---

## 11.6 Variant analysis: turning one bug into many

The highest-leverage move available after any finding — yours or someone else's.

**Operation:** take a known bug (a disclosed report, a CVE, your own finding),
abstract it to its **root cause shape**, then systematically find everywhere else
that shape occurs.

```
1. What is the SHAPE?   not "IDOR in /invoices" but
                        "object loaded by ID before the tenant check"
2. Where else could that shape exist?
     - same codebase, different route        (lexical variant)
     - same framework, different app         (structural variant)
     - same logic, different trigger         (logical variant)
3. Search for the shape, not the symptom.
4. Establish each variant's conditions and impact INDEPENDENTLY.
```

Why this produces *non-obvious* results from *obvious* seeds: the original is public
and duplicated to death, but **the variants are not**, because finding them requires
abstracting the root cause rather than pattern-matching the symptom. Most hunters read
a disclosed report and test the exact same endpoint on another target. That's the
crowded move. Abstracting the shape is the uncrowded one.

Trail of Bits ships a `variant-analysis` skill; Project Zero has written extensively
on this as a discipline. It is the single best use of a disclosed report.

---

## 11.7 Anti-patterns that guarantee duplicates

Each of these is a reliable way to do real work for zero pay.

| Anti-pattern | Why it duplicates |
|---|---|
| Running nuclei across the whole scope and submitting hits | Everyone runs the same templates continuously. You are racing a cron job. |
| Testing the login/registration/password-reset flow first | The most-tested surface on every target in existence. |
| Submitting the first thing you find | The first thing found is the easiest thing to find — for everyone. |
| Following a popular YouTube/blog methodology verbatim | You are now running a shared playbook; expect shared results. |
| Hunting the programs everyone streams and tweets about | Attention is the duplicate signal. |
| "Find all vulns" on a whole target | Produces generic output. A focused prompt measurably finds more *and* more unusual bugs. |
| Installing a 90-skill mega-pack and running its autopilot | Convergent playbooks, convergent findings — plus a per-turn context tax. |
| Reporting the exact endpoint from a disclosed writeup | Thousands read that writeup. Abstract the shape instead (§11.6). |
| Chasing the newest CVE on day 3 | Day 0–1 is an edge; day 3 is a queue. |
| Skipping recon to start testing | You end up testing only what's linked from the homepage — i.e. what everyone tests. |

---

## 11.8 How this changes the pipeline

[04 — Harness Architecture](./04-harness-architecture.md) gets one new phase, placed
**early**, because that's the whole point:

```
   SCOPE  →  RECON  →  ✦ IDEATE ✦  →  ✦ OBVIOUSNESS FILTER ✦  →  HUNT
                            │                    │
                 run the 12 generators    kill crowded ideas HERE,
                 against this target      before they cost validation budget
                            ↓
                      HUNT → DISPROVE → RE-VERIFY → HUMAN → REPORT
```

Two concrete rules:

1. **Ideate before hunting.** Generate 15–25 hypotheses with the generators, score
   them all, then hunt the best-scoring 3–5. Do not hunt the first idea you have —
   the first idea is, definitionally, the obvious one.
2. **The obviousness filter is a budget gate, not a quality gate.** Its job is to
   stop you spending proof effort on a race you'll lose.

Implemented as:
- `skills/hypothesis-forge/SKILL.md` — runs the generators, scores, and ranks
- `agents/ideator.md` — a subagent whose only job is divergent hypothesis generation,
  deliberately *separated* from the hunter so that proving pressure doesn't collapse
  its creativity

> **Why a separate agent:** an agent that must both invent and prove will quietly
> bias toward hypotheses that are easy to prove — which are the obvious ones. Keeping
> ideation in its own context, with no obligation to validate anything, is what keeps
> the ideas strange. This is the same structural logic as separating the hunter from
> the disprover, applied one stage earlier.

---

## 11.9 The one-page version

> **Obvious ideas are negative-value: full cost, zero return.**
>
> Your competition is a generic agent running a shared playbook. So:
> **if a generic agent would propose it first, don't hunt it.**
>
> Generate ideas with **operations on the target** (assumptions, defenses, seams,
> lifecycles, derived copies, time, composition, actor matrices, history, un-demoed
> features, scope archaeology, fresh techniques) — never from a list of bug classes,
> because everyone has the same list.
>
> Score for crowding **before** you spend proof effort, not after.
>
> Then prove it ruthlessly ([05](./05-validation-gates.md)) and write it so a triager
> can't close it ([07](./07-reporting-that-gets-paid.md)).

---

**Next:** [05 — Validation Gates](./05-validation-gates.md) ·
[07 — Reporting](./07-reporting-that-gets-paid.md) ·
[06 — Target Selection](./06-target-selection.md)
