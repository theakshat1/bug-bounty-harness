---
name: report-writer
description: Write a bug bounty report engineered to get TRIAGED rather than closed Not Applicable, Informative, or stalled in Needs More Info. Use after a finding is CONFIRMED and human-reviewed, before submission. Encodes the exact per-platform state machines, reputation costs, and triager rubrics.
argument-hint: "[finding-id] [hackerone|bugcrowd|intigriti|yeswehack]"
---

# Report Writer

A proven, novel bug pays nothing if a triager closes it Informative, marks it Not
Applicable, or lets it rot in Needs More Info. This skill writes against the platforms'
*published rubrics*.

## Refuse to draft without these

- The finding is `CONFIRMED` in `findings/confirmed.jsonl`
- `gate_6_human_reviewed` is `true`
- An impact sentence exists with concrete nouns
- Evidence was produced on an in-scope asset

Say exactly which is missing and stop. Drafting an unvalidated finding is how accounts
get banned.

## The costs you are writing against

**HackerOne reputation:** Triaged/Resolved **+7** · Informative **0** · **Not Applicable
−5** · dup after public disclosure **−5** · dup of an N/A **−5** · Spam **−10** ·
**self-closed 0**.

Three mechanics that change how you write:

1. **N/A is a two-part test:** *"doesn't contain a valid reproducible issue, **and** the
   security implications have not been demonstrated."* **A report that reproduces
   perfectly but whose impact you merely asserted is eligible for −5, not 0.** Asserting
   impact is not a style problem. It is a reputation penalty.
2. **Severity is a routing input** (mandatory since 2026-09-21). Under-scoring buries
   your own report behind other people's Highs. Over-scoring puts it in front of a senior
   triager who downgrades it and remembers you.
3. **A machine may close it before a human reads it.** Hai Triage auto-closes clear
   duplicates and non-issues. Your **title, weakness class, severity and first
   paragraph** are the inputs to that decision.

**Bugcrowd:** `Accuracy = Valid/(Valid+Invalid)`; **>50% in 90 days is required for
private invites.** Informational/P5 counts as **valid**. **Out of Scope** and **Not
Reproducible** count as invalid. Not Reproducible is almost always a *reporting* defect.

**Intigriti:** **a Duplicate *increases* your validity ratio** — Out of Scope decreases
it. So don't suppress a submission out of duplicate fear here; be precise about asset
selection instead.

**YesWeHack:** has an **RTFS** state ("Read The Fine Scope") that punishes not reading
the program rules, distinct from being wrong.

---

## Step 1 — Read the brief, and the right severity method

*"The brief is the final word."* (Bugcrowd, Ryan Black)

Capture before writing:
- The asset, named **exactly** as the program lists it — then quote that scope line in
  the report. Automated out-of-scope classifiers read your asset selection first.
- The **accepted-risk / non-qualifying list**. If your finding is on it, stop; submitting
  anyway is a signal hit (and on YesWeHack, an RTFS).
- **Which severity method applies:** CVSS 3.1 / CVSS 4.0 / manual / VRT. And on
  Intigriti, **PoC-based (default) vs vulnerability-type-based** — under PoC-based an
  undemonstrated chain scores **nothing**.
- Whether the brief mandates **video** (Intigriti does not require it platform-wide;
  individual briefs do).

## Step 2 — Title

```
[Vuln class] in [specific component/parameter] — [concrete consequence] ([auth context])
```
≤140 characters. **No URL on Intigriti** (separate endpoint field). **No hedging** —
"possible", "potential", "might", "suspected" read as low confidence to a triager
scanning a queue, and now feed automated dedupe and routing.

- ✅ *"Remote File Inclusion in Resume Upload Form allows remote code execution"*
- ✅ *"Stored XSS in User Profile Comments Allowing Account Takeover"*
- ✅ *"SQL injection in [reports.example.com] parameter [filter=]"*
- ❌ *"RFI Injection found"* · ❌ *"XSS in app.example.com"* · ❌ *"Possible IDOR"*

Titles are explicitly the mechanism by which teams prioritize and identify duplicates.

## Step 3 — Body, in this order

```markdown
## Summary
<2–3 sentences. The whole finding: what boundary breaks, who is affected, what the
attacker gains. Concrete nouns. Never the class name as the impact.>

## Affected asset
- Asset (as listed in scope): <exact>   ← quote the scope line
- Endpoint: <METHOD /path>              ← as TEXT, never a screenshot
- Component/version: <if known>
- Discovered / Verified: <dates>

## Preconditions
- Accounts needed: <how many, what roles, how to create them, email verification?>
- <precondition> — DEFAULT / COMMON / UNUSUAL
- Reproducibility: deterministic | timing-dependent (<success rate> over <N> attempts)

## Steps to reproduce
1. <One instruction per line. Numbered. Minimal. Name the account used at each step.>

Account A (attacker): acct-a@...        Account B (victim): acct-b@...
Canary in B's data: CANARY-B-7f3a       ← makes the proof unambiguous

## Request / response evidence
<Raw HTTP as TEXT in fenced blocks, tokens and cookies redacted.
Never screenshot a request. Keep every URL copy-pasteable.>

## Expected vs actual behavior
Expected: <...>
Actual:   <...>

## Impact

**Demonstrated now:**
An [unauthenticated | self-registered | low-privilege] attacker can [verified action]
against [named asset], obtaining [specific data or capability] for [scale], without
[the mitigation expected to prevent it].

**Potential if chained:** <separate paragraph, clearly marked as not demonstrated>

## Mitigations considered
- WAF: <why it doesn't stop this>
- CSP / SameSite / CSRF token / rate limiting / MFA: <each, or "not applicable because…">

## Severity
<Band> — <full CVSS vector string>
- AV:<x> because <reason>    - PR:<x> because <reason>
- UI:<x> because <reason>    - C/I/A:<x> because <reason>
Capped at <band> because <the honest limiting factor>.

## VRT classification        ← Bugcrowd only
<Category → Sub-Category → Variant>, e.g. "Broken Access Control → IDOR → Horizontal"
<If above the VRT baseline, state the specific facts that elevate it.>

## Remediation
<2–3 concrete sentences. Name the check and where it belongs.>

## Testing metadata
- Window: <timestamps>          - Source IP: <so they can correlate their logs>
- Browser/OS/client version: <...>
- Prior art checked: <disclosed reports + hacktivity; nearest non-matching report>
- Affected surface: same root cause affects <X, Y, Z>   ← ONE report, not N
- Conduct: no data touched in accounts I don't own; <what I read/wrote>; artifacts removed
```

## Step 4 — The impact section is where reports die

**Closed Informative** names a vulnerability class and asserts its textbook
consequences — *"an attacker could steal cookies and take over accounts"* after
demonstrating only `alert(1)`. Generic, class-level, copy-pasted.

**Paid** names (a) the specific asset and data, (b) the trust boundary crossed, (c) the
attacker's starting privilege, (d) what the attacker ends up holding, (e) scale, and
(f) why existing mitigations don't stop it — **with every clause traceable to a step in
your repro.**

Write the published tests into the draft and answer them literally:
- *"Why is this important for the business?"*
- Does fixing it *"improve your security posture"*?
- *"Demonstrate the current impacts and describe the potential impacts"* — **separate
  paragraphs**, so a triager cannot read your speculation as your claim.

> **The rule that avoids −5:** where you have the primitive but not the chain, **say so
> explicitly and score accordingly.** Claiming a chain you didn't demonstrate is exactly
> what converts a would-be Informative (0) into an N/A (**−5**).

### Low-baseline classes that need re-framing
Self-XSS · clickjacking on logged-out pages · open redirect · missing headers ·
improperly scoped cookies · HTML injection claimed as XSS without a WAF bypass · CVE
references without a working PoC · unverified scanner output.

For any of these, your impact section must terminate in an **authentication,
authorization, or tenancy boundary you actually crossed** — and you must *show* the
crossing, not assert it.

## Step 5 — Severity without self-harm

Publish the **full vector string with a one-line justification per metric.** A vector
with reasoning is arguable; a bare number gets overwritten.

**The eight over-scoring mistakes:**
1. `S:C` on a same-app issue — scope change needs a *security authority* boundary
   crossing (and the metric doesn't exist in CVSS 4.0 at all)
2. `AC:L` when a victim must be logged in or an unguessable token is needed (that's
   `AT:P` in 4.0)
3. `PR:N` when any authenticated session is required — a self-registered free account is
   `PR:L`
4. `UI:N` on reflected XSS / CSRF / clickjacking
5. Maxing `C:H/I:H/A:H` off one leaked field — reading one user's email is not total
   confidentiality loss
6. `AV:N` for something only reachable internally
7. **Scoring the chain you imagined rather than the one you demonstrated**
8. Ignoring existing mitigations

**And two under-scoring mistakes:** severity drives routing, so a genuine critical scored
Medium queues behind other Highs; and scoring the *category* ("IDOR = Medium") instead of
the *instance* wastes the VRT "Varies" upside.

**Platform lead:** Bugcrowd → lead with the **VRT entry**, CVSS as support. HackerOne and
Intigriti → lead with the **CVSS vector + per-metric rationale**.

## Step 6 — Pre-empt every Needs More Info question

Confirm all sixteen are answered before submitting:

```
[ ] 1  Account preconditions: count, roles, how to create, verification needed
[ ] 2  Exact endpoint + full raw HTTP request as TEXT, redacted
[ ] 3  Every URL copy-pasteable, not inside an image or video
[ ] 4  Expected vs actual, stated separately
[ ] 5  Asset named exactly as the program lists it, scope line quoted
[ ] 6  Severity with full vector + per-metric justification
[ ] 7  Real-world mitigations addressed one by one
[ ] 8  Reproducibility class; success rate + attempt count if non-deterministic
[ ] 9  Environment: browser/version, OS, client, region/tenant
[ ] 10 Timestamp + testing source IP
[ ] 11 Non-destructive confirmation; what you read/wrote
[ ] 12 PoC files attached ON-PLATFORM, not external links
[ ] 13 One report per root cause — "same root cause, affects X, Y, Z"
[ ] 14 Prior-art check stated, nearest non-matching report named
[ ] 15 Remediation suggestion
[ ] 16 For "Varies" VRT entries or chains: which facts elevate it above baseline
```

## Step 7 — Final checks before handing it over

- **The paper test** (Intigriti's own): *"Can my report be printed on a sheet of paper
  and still be understood?"* Images are guidance; they must not be **required**.
- **On HackerOne, run Report Assistant's "Run checks"** — it grades against HackerOne's
  own rubric (repro clarity, expected vs actual, impact, **asset scope alignment**,
  severity sanity, supporting materials) and data isn't shared with the program
  pre-submission. Free pre-triage review; use it every time.
- **One report per root cause.** Five subdomains sharing one library bug is one report.
  Filing them separately creates self-duplicates — a straight path to −5s.
- **For XSS, prove execution with `document.domain` or `document.cookie`**, not
  `alert(1)` or a vanity string.
- **Write so the summary survives.** On Bugcrowd the ASE team may **edit** your
  submission and *"the edited submission details are what the customer will receive"*; on
  HackerOne a Hai triage summary is injected into the engineer's Jira ticket. Your first
  paragraph is what reaches the person who decides.

## Step 8 — Output

Write to `reports/<date>-<target>-<class>.md`. **A human submits it. Never submit
anything yourself.**

Then tell the user: the proposed severity and why it's capped there, which NMI questions
were hardest to answer (a signal about evidence gaps), and whether any part of the impact
is asserted rather than demonstrated.

---

## After submission — the mechanics worth knowing

- **Heading for N/A on HackerOne? Self-close instead.** Self-closed = **0**; N/A = **−5**.
  This converts a penalty into a neutral and keeps it out of Signal. Most underused
  mechanic on the platform.
- **Needs More Info >30 days auto-closes Informative** (reputation-safe, but zero
  bounty). Answer in days.
- **Disputing a duplicate:** argue **root-cause and exploit-path divergence**, never
  surface similarity. Strongest grounds: different code path; materially greater
  privilege crossing; the original was closed N/A or Informative (a dup of an N/A costs
  you −5, so this is the most financially urgent dispute); the original was already
  resolved before you filed; your submission predates theirs; you were duped against a
  disclosure that postdates you (flips −5 to +2). **Never argue "mine is better written"
  or "I found it independently"** — independence is irrelevant under first-to-find.
  If marked duplicate without participant access, **ask to be added as an external
  participant.**
- **Cooling periods:** HackerOne — comment first, then 5 business days, then mediate;
  never within 7 days of an update; **never after 3 months closed** (mediation needs
  Signal > 0). Bugcrowd — Request a Response at day 7 (48–96h SLA), support@ at day 14.
  Intigriti — "Request support", mediator from outside triage, up to 30 days, and
  Intigriti may pay **€100–€1,000 itself** if the company doesn't respond in 30 days
  (one claim per program per 90 days).
- **Argue the metric, not the outcome.** Bring new evidence; mediation that restates your
  original claim is explicitly rejected.
- **Never go public first.** Discouraged or forbidden everywhere.

→ Full mechanics in [`docs/12`](../../docs/12-triage-and-report-mechanics.md).
