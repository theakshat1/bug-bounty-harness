# 12 — Triage & Report Mechanics

> A proven, novel bug still pays nothing if a triager closes it Informative, marks it
> Not Applicable, or stalls it in Needs More Info until it auto-closes. This document
> is the platform machinery: the exact states, the exact point values, and the exact
> rubrics you are being graded against.
>
> Verified 2026-10-02. **[V]** = verified against primary platform docs/changelogs or
> first-party blog. **[U]** = unconfirmed or secondary.

---

## 12.1 The eight findings that change decisions

Read these even if you skip the rest.

1. **Not Applicable is a two-part test, and it costs you −5.** HackerOne's own
   definition: *"The report doesn't contain a valid reproducible issue, **and** the
   security implications have not been demonstrated."* **[V]** So a report that
   reproduces perfectly but whose impact you merely *asserted* is eligible for N/A
   (−5), not just Informative (0). Asserting impact is not a style problem — it is a
   −5.

2. **Self-closing is free, and almost nobody uses it.** Self-closed as N/A = **0
   reputation**, and it stays out of Signal entirely. **[V]** If a triager signals your
   report is heading to N/A, self-closing converts a −5 into a 0. This is the most
   underused mechanic on HackerOne.

3. **Your severity is now a routing input, not an opinion.** Mandatory on HackerOne
   since **2026-09-21**, because triage *"now routes reports based on their initial
   severity, and reports without severity were missing priority routing."* **[V]**
   Under-scoring no longer reads as modesty — **it buries your own report behind
   other people's Highs.** Over-scoring puts it in front of a senior triager who will
   downgrade it and remember you.

4. **A machine can close your report before any human reads it.** Hai Triage
   auto-reviews shortly after submission, and one of its three paths is *"automatic
   closure for clear duplicates, spam, or non-issues."* **[V]** Your title, weakness
   classification, severity and first paragraph are the inputs to that decision.

5. **On Intigriti, a Duplicate *increases* your validity ratio.** **[V]** It's proof
   you found a real bug. Compare HackerOne, where a duplicate of an N/A or a
   post-disclosure duplicate is **−5**. Consequence: on Intigriti, fear of duplicates
   should not suppress submissions — fear of **Out of Scope** should.

6. **"Account for real-world mitigations" is now an explicit quality bar.** HackerOne's
   Code of Conduct lists four requirements of a high-quality submission, and the third
   is *"Account for real-world mitigations and context"*; failing to account for
   existing mitigations is a stated **invalidity** criterion. **[V]** Pre-empting
   "but WAF/CSP/SameSite/rate-limiting blocks this" inside the report is part of the
   bar now, not a nicety.

7. **On Bugcrowd, the triager rewrites your report and the rewrite is what the
   customer reads.** *"The edited submission details are what the customer will receive
   for review and reward."* **[V]** Write so the edit is unnecessary.

8. **Letting Needs More Info rot for 30 days auto-closes it Informative with no
   reputation harm.** **[V]** Reputation-safe, but you lose the bounty and the +7. NMI
   is not a crisis — it's a slow leak.

---

## 12.2 HackerOne

### States **[V]**
Source: [Report States](https://docs.hackerone.com/en/articles/8475030-report-states)

**Open:**

| State | Meaning | Note |
|---|---|---|
| **New** | "The report is pending validation." | Entry state. |
| **Pending Program Review** | Validated by H1 triage, awaiting the customer team. | **Not a win yet** — state and severity can still change. |
| **Triaged** | "Validated and escalated for internal remediation." | **+7.** "In rare cases, a triaged bug may be marked as duplicate or informative after further review." |
| **Retesting** | Fixed, awaiting your verification. | **+2** |
| **Needs More Info** | Insufficient reproduction detail or impact. | **>30 days → auto-closes Informative, no reputation harm.** |

**Closed:**

| State | Reputation |
|---|---|
| Resolved | **+7** |
| Informative — "valid information, but doesn't require action" | **0** |
| Duplicate | varies, see below |
| **Not Applicable** — not reproducible **and/or** implications not demonstrated | **−5** |
| Spam | **−10** |

### Reputation **[V]**
Source: [Reputation](https://docs.hackerone.com/en/articles/8369865-reputation)

| Event | Points |
|---|---|
| Triaged or Resolved | **+7** |
| Retesting | +2 |
| Duplicate of a resolved report, filed **before** the original went public | **+2** |
| Original already resolved when you filed | 0 |
| Informative | 0 |
| **Self-closed as N/A (by you)** | **0** |
| Not Applicable | **−5** |
| Duplicate filed **after** public disclosure | **−5** |
| Duplicate of an N/A report | **−5** |
| Spam | **−10** |

Starting reputation **100**; cannot go below **0**; **duplicate chains cap at three** —
the 4th+ duplicate earns 0.

**Bounty reputation** (separate): ≥ mean + 1SD → **+50**; > mean → +25; ≥ mean − 1SD →
+15; below → +10. *"The first 10 bounties of a program will be rewarded the BOUNTY_LOW
reputation."* **[V]**

### Signal, Impact, and gating **[V]**
- **Signal** = average reputation per *closed* report. Scale **−10 to 7**. Needs >3
  closed reports. Gating uses a **rolling 365-day window**.
- **Impact** = average reputation per *bounty*. Scale **0 to 50**. Needs >3 bounties.
- Program thresholds: **Strict ≥ 1.0 · Standard ≥ 0.0 · Lenient ≥ −1.0** · off.
- Below threshold you get **trial reports** (rolling 30 days):

| | New hacker (<5 resolved) | Seasoned (>5 resolved) |
|---|---|---|
| Per program | 4 | 8 |
| Platform-wide | 6 | 12 |

> **A single −5 N/A near 0 Signal can lock you out of Strict programs for up to 365
> days.** Trial reports make every early submission a Signal bet.

**[U]** HackerOne's docs are internally inconsistent on whether Informative is excluded
from Signal (prose) or included at weight 0 (formula, which dilutes downward). Treat
Informative as mildly Signal-diluting and avoid it.

**90-day leaderboard / invites:** `Reputation × Signal Percentile × Impact Percentile`;
requires positive reputation gain, **non-negative Signal**, and zero CoC violations in
90 days. **[V]**

### The Code of Conduct is the format spec **[V]**
Four stated requirements of a high-quality submission — **use them as your section
headers**:

1. "Demonstrate clear, reproducible impact with step-by-step reproduction"
2. "Include a strong proof of concept"
3. **"Account for real-world mitigations and context"**
4. **"Assign accurate severity at the point of submission"**

Enforcement ladder for large-scale low-quality or unverified reports:
**1st = Final Warning → 2nd = 12-month ban → 3rd = permanent ban.** **[V]**

Context: a *"significant (100%+) surge in report volume"* after February 2026 model
releases; HackerOne's own program took over 1,390 reports in H1 2026 — more than 2024
and 2025 combined. **[V]**

### Report Assistant is a free pre-triage review **[V]**
`hackerone.com/hai/report_assistant` checks: steps to reproduce · expected vs actual ·
impact explanation · **asset scope alignment** · severity sanity · supporting materials ·
required program fields. Non-blocking, nothing rewritten without asking, *"data isn't
shared with programs before submission."*

**This is HackerOne's published triage rubric. Run "Run checks" before every submit.**

### Timeline and escalation **[V]**
Acknowledgment immediate → triage **2–4 business days** → program review **4–10 days** →
bounty decision **~2 weeks**.

**Mediation:** requires **Signal > 0**. Comment asking for a status update first; if no
response in **5 business days**, Request Mediation (bottom of the report). HackerOne
then asks the program to resolve within **3 business days**.

**Do not request mediation** if: closed **3+ months** ago · the report saw an update
**less than 7 days** ago · your request doesn't explain why you disagree. **[V]**

Once **Triaged**, you can only add comments — **you cannot edit a submitted report.**

---

## 12.3 Bugcrowd

### VRT is primary; CVSS is support
Current version **1.19.1, released 2026-07-08** **[V]**. Canonical:
[bugcrowd.com/vrt](https://bugcrowd.com/vrt) ·
[GitHub](https://github.com/bugcrowd/vulnerability-rating-taxonomy)

Structure is **Category → Sub-Category → Variant**. **Select the deepest matching
Variant, not the Category**, and cite its name in your report.

The GitHub repo ships **mappings to CVSS v4, CVSS v3, CWE and remediation advice** —
pull them so your CVSS vector and CWE *agree* with the VRT entry you picked. Triagers
notice when they don't.

> **Entries marked "Varies" are where your report is won or lost.** IDOR spans P4→P1.
> For a "Varies" entry you must supply the facts that justify the upper bound —
> **absent that, the triager defaults low.**

And the caveat, verbatim: *"the severity rating suggested by VRT is not guaranteed to
be the severity rating applied."* **[V]**

Recent VRT changes: 1.19.1 added Active Directory misconfigurations, Kerberos/SCCM
abuse, server misconfigurations, and streamlined SSRF classifications; 1.18 (Feb 2026)
added an OAuth Account Squatting variant at P4 and downgraded all Flash entries to P5.

### P1–P5 **[V]**
P1 Critical (unusable app, immediate attention) · P2 Severe (significant impact) ·
P3 Moderate (real flaw needing a fix) · P4 Low (minor) · **P5 Informational — an
*accepted*, non-rewardable state**, not a rejection.

### States and Accuracy **[V]**
**Open:** New, Triaged · **Accepted:** Unresolved, Resolved, Informational ·
**Rejected:** Out of scope, Not reproducible, Not acceptable

```
% Accuracy = [Valid / (Valid + Invalid)] × 100
Valid: Unresolved, Resolved, Informational
"Not Applicable" submissions are excluded from both numerator and denominator
```

**Private program invitations require >50% accuracy within a 90-day period.** **[V]**

Practical reading: **Informational/P5 protects your Accuracy. Out of Scope and Not
Reproducible destroy it.**

> **Not Reproducible is the state to design against.** It is almost always a
> *reporting* defect — missing account preconditions, an expired session, a one-shot
> race, state you consumed, or a bug fixed before triage reached it — not a research
> defect.

**Won't Fix** still pays kudos: *"submissions that are moved to a 'won't fix' substate
will have the appropriate kudos points assigned based on prioritization."* **[V]**

**Kudos [U]** — P1 40 (dup 10) · P2 20 (dup 5) · P3 10 · P4 5 · P5 0. Note Bugcrowd
**does pay partial kudos on P1/P2 duplicates**, unlike HackerOne.

### Things worth knowing
- **The ASE team edits submissions, and the edit is what the customer reads.** **[V]**
- **Priority Queue Bypass** (launched 2026-06-08): expedited triage, profile badge,
  priority private invites. Qualifying metrics are **accuracy rate, submission volume,
  and consistency over time** — explicitly motivated by AI slop, because historically
  *"a first-time submitter and a researcher with an extremely high accuracy rate ...
  land in the same queue."* **[V]**
- **CVSS 4.0** supported since April 2026, opt-in per program; switching doesn't
  retro-update existing submissions. **[V]**
- Ryan Black (Sr. Director, Security Operations): triage assesses **scope alignment,
  validity, priority per policy, reward per policy**; response *"less than 24 hours for
  critical"*; **"The brief is the final word"**; strictly **first-to-find**; **~92%** of
  post-triage submissions reach resolution. **[V]**

### Escalation **[V]**
Triage typically **7 business days**; final status **14 days**.

**Day 7+: Request a Response** — categories: Issue is Reproducible · Scope · Duplicate
State · Reward · Priority · Requesting Update · Other. SLA **48–96 hours**.
**Day 14+ (or 7 days of no owner response): email support@bugcrowd.com** with the
submission ID. Since 2026 a Request a Response can be **withdrawn** and no longer
**expires**.

Explicitly discouraged: *"Tweeting your frustrations... is unnecessary and
inflammatory"*; berating ASEs; disclosure threats; messaging daily.

---

## 12.4 Intigriti

### States **[V]**
**Draft → Triage → Pending → Accepted → Closed → Archived**

**Pending is your window:** *"In this status it is possible to adjust severity or
bounty tier"* — severity is still live, so this is when to argue it. Closed stays 14
days before archiving; Archived is locked.

### Close reasons and validity ratio **[V]** — the big divergence

| Close reason | Validity ratio |
|---|---|
| **Accepted Risk** | **increases ▲** |
| **Duplicate** | **increases ▲** |
| Informative | neutral |
| Out of Scope | decreases ▼ |
| Not Applicable | decreases ▼ |
| SPAM | decreases ▼ |

**On Intigriti a duplicate helps you.** It's evidence you found something real. So
here, don't let duplicate-fear suppress a submission — let **Out-of-Scope**-fear
discipline your asset selection instead. (And note Triage Assist now runs an automated
**out-of-scope classifier** that reads your asset selection first, so picking the wrong
asset is a *mechanical* path to an OOS close. **[V]**)

### Report requirements **[V]**
The governing principle, verbatim:

> *"All information necessary to reproduce the vulnerability should be written in the
> report, images can be used as guidance, but should not be required to understand and
> reproduce the submission."*

And their test, verbatim: **"Can my report be printed on a sheet of paper and still be
understood?"**

Specifics:
- **Never screenshot an HTTP request.** *"Copy-paste this request into your report (and
  redact the cookies/authorization token) or explain how the Triager could find this
  POST request themselves."*
- **No URL in the title** — there's a separate endpoint field. Good examples they give:
  *"Reflected XSS in search parameter"*, *"IDOR on download personal data"*.
- **For XSS use `document.domain` or `document.cookie`, not `alert(1)`** or a vanity
  string.
- Include the **IP address you tested from** so they can validate against their logs.
- Attachments **on-platform**: PNG/JPG/GIF 10 MB, other formats 1 GB. If external
  hosting is unavoidable, password-protected ZIP with the password in the report.

### Severity method — check which one the program uses **[V]**
[Triage Standards](https://kb.intigriti.com/en/articles/10335710-intigriti-triage-standards):

1. **Proof-of-Concept Assessment (default)** — severity *"based on the impact
   demonstrated."* **An undemonstrated chain scores nothing.**
2. **Vulnerability Type Assessment** — scored on the initial and immediate effect on
   the vulnerable system. **Speculative downstream chaining is irrelevant.**

Check which applies *before* writing your impact section.

### Mediation — the only platform that pays you itself **[V]**
Trigger: **"Request support"** on the submission, or comment tagging the triager.
Acknowledged usually within **2 working days**, and *"a mediator outside of the triage
team will investigate your case."* Decision up to **30 days**. **No mediation after 3
months closed.**

Outcomes:
- **For the researcher:** Intigriti proposes a counteroffer and **matches compensation
  itself if the company doesn't respond adequately within 30 days** — **€100 (low) to
  €1,000 (exceptional)**. Limit: **one claim per researcher, per program, per 90 days.**
- **For the company:** no changes, with explanation.
- **Unclear:** a **€75 swag voucher**.

Include: why the decision was wrong · **specific CVSS metrics if challenging
severity** · additional impact evidence · timeline of prior communication.
Avoid: social-media disclosure · update requests more often than every **30 days** ·
mediating before reading the triager's feedback.

### ⚠️ Correcting a common belief
**"Intigriti requires video" is not true platform-wide. [V]** Their documented standard
is **text-first** and explicitly says images *"should not be required."* Video is
"Optional"/"when it's an added value" — though individual **program briefs** do mandate
it. Correct rule: **written repro steps are mandatory; video is program-specific and
strongly advantageous for multi-step, race-condition and business-logic findings.**

---

## 12.5 YesWeHack

### States **[V]**
**New → Under Review → Assessed → (Accepted | Not Valid) → Resolved**, with **Need More
Info** as a side path.

**Invalid:** Duplicate (*"the vulnerability exists but has already been reported"* —
**hunter still receives ranking points**) · Not Applicable/Invalid · Out of Scope ·
Spam · **RTFS** ("Read The Fine Scope").

> **RTFS has no analogue on any other platform.** It punishes *not reading the program
> rules* as distinct from being wrong. Repeat offenses close as Out of Scope.

**Valid:** Won't Fix (may include reward) · Informative (reward still possible) ·
Accepted (reward issued) · Resolved.

### Points **[U — traces to a Feb 2021 post; 2026 values unverified]**
Bounty points 5–50 by tier · **quality rating +1 to +5 awarded by the program owner for
report quality** · **+1 when your CVSS scoring is appropriate** · +7 for a resolved bug.

**If still current, YesWeHack is the only platform that pays you points directly for
report-writing quality and for correct CVSS scoring** — which makes careful
self-scoring there directly profitable rather than merely risky. Treat as directional.

### Their framing questions **[V]**
> *"Does your Proof of Concept have enough detail to allow anyone to reproduce it?"*
>
> *"Did you sufficiently **demonstrate the current impacts** and **describe the
> potential impacts**?"*

That two-part structure — **demonstrate current, describe potential** — is the cleanest
published template for an impact section. Keep them in **separate paragraphs** so a
triager can't read your speculation as your claim.

CVSS rule, verbatim-adjacent: *"If you are suggesting a CVSS with a high score, you
must demonstrate those impacts to justify a reward."*

**There is an explicit "bug chaining" field on the submission form — use it.** **[V]**

### Their explicit rejection list **[V]**
Missing PoC steps · unverified scanner findings · theoretical vulnerabilities without
exploitation proof · **CVE references lacking a working PoC** · unvalidated
prerequisites · **HTML injection claimed as XSS without a WAF bypass** ·
reverse-engineered code findings without a real-world attack path.

---

## 12.6 Titles

**Canonical form [V, HackerOne]:** `<Vulnerability Type> in <Affected Scope>`
**Extended [V, Orwa/Bugcrowd]:** `<Type> in <Asset/Endpoint> parameter <param>`
**Impact-bearing [V, Hacker101 + Intigriti]:** `<Type> in <Location> allowing <Concrete Impact>`

Bugcrowd's own good/bad pair **[V]**:
- ✅ *"Remote File Inclusion in Resume Upload Form allows remote code execution"*
- ❌ *"RFI Injection found"*

Intigriti **[V]**: ❌ *"XSS in app.example.com"* → ✅ *"Stored XSS in User Profile
Comments Allowing Account Takeover"*. **No URL in the title.**

Hacker101's exercise **[V]**: *"How do I describe this vulnerability in 140 characters
or less?"* — and titles are explicitly the mechanism by which security teams
**prioritize and identify duplicates**.

### Synthesized rule
```
[Vuln class] in [specific component/parameter] — [concrete consequence] ([auth context])
≤140 chars · no URL on Intigriti · NO hedging words
```
**Banned in titles:** "possible", "potential", "might", "could be", "suspected". A
hedged title reads as low-confidence to a triager scanning a queue — and now also feeds
automated dedupe and severity routing.

---

## 12.7 Pre-empting Needs More Info

NMI is a slow leak: on HackerOne it auto-closes Informative after 30 days (0 bounty,
0 reputation gain); on Bugcrowd an unanswered report risks **Not Reproducible**, which
is *invalid* and hits the >50%/90-day private-invite gate.

**Answer all sixteen of these in the initial report** — they are the clarifying
questions derivable from the published rubrics:

1. **Account preconditions** — how many accounts, what roles, how to create them,
   whether email verification is needed
2. **Exact endpoint + full raw HTTP request as TEXT**, tokens redacted — never a
   screenshot of a request
3. **Every URL in copy-pasteable text**, not embedded in an image or video
   *("allowing triagers to easily copy and paste URLs instead of manually typing them")*
4. **Expected vs actual behavior**, stated separately
5. **Asset scope alignment** — name the asset exactly as the program lists it, and
   quote the scope line
6. **Severity with its full vector string and per-metric justification**
7. **Real-world mitigations addressed** — WAF, CSP, SameSite, rate limiting, MFA, CSRF
   tokens: say why each does not stop this
8. **Reproducibility class** — deterministic, or timing-dependent? If non-deterministic,
   give **success rate and attempt count**
9. **Environment** — browser/version, OS, client version, region/tenant
10. **Timestamp + testing source IP** so they can correlate their logs
11. **Non-destructive confirmation** — state you didn't touch data in accounts you don't
    own, and what you did read/write
12. **PoC files on-platform**, not external links
13. **Scope of affected surface** — one consolidated report per root cause: *"same root
    cause, affects X, Y, Z"*
14. **Prior-art check** — say you checked disclosed reports/hacktivity, and what the
    nearest non-matching prior report is
15. **Remediation suggestion**
16. **For "Varies" VRT entries or chains** — which specific facts elevate it above
    baseline

**While in NMI:** answer in the report comments, never off-platform. HackerOne: don't
request mediation within 7 days of an update. Intigriti: don't request updates more
than every 30 days.

---

## 12.8 Duplicates

### How they're determined
- **HackerOne [V]:** a Report Duplicate Detector matches against all prior reports to
  that program; Hai has a dedicated deduplication agent and **can auto-close clear
  duplicates with no human involved.**
- **Bugcrowd [V]:** "correlation and de-duplication", strictly **first-to-find**.
- **Intigriti [V]:** Triage Assist duplicate detection, triager accepts or overrides.
- **Root cause, not symptom [V]:** triage closes as duplicate when a bug *"shares the
  same root cause as another bug already reported"* — which is why five subdomains with
  one shared library bug collapse into one report.
- **Internal knowledge counts [V]:** you can be duped against something never publicly
  filed.

### Credit for a duplicate

| Platform | Credit |
|---|---|
| **HackerOne** | **+2** if dup of a resolved report filed *before* the original went public · **0** if already resolved · **−5** if filed after public disclosure, or dup of an N/A · chain caps at 3 |
| **Bugcrowd** | Kudos P1 10 / P2 5 **[U]**, no bounty |
| **Intigriti** | **Increases validity ratio ▲** |
| **YesWeHack** | **Hunter receives ranking points** |

### Arguing a non-duplicate
Argue **root-cause and exploit-path divergence**, never surface similarity:

1. Different root cause (different code path/component) even if same class and endpoint
2. **Materially greater impact or privilege crossing** — theirs authenticated-self,
   yours cross-tenant; theirs reflected, yours stored
3. The original was closed **N/A or Informative** — a dup of an N/A costs you −5, which
   makes this the most financially urgent dispute to raise
4. The original was **already resolved before you submitted** — a resolved-then-regressed
   bug is a new bug
5. Your submission **predates** theirs (check timestamps; collaborate, don't fight)
6. You were duped against a public disclosure that **postdates** your submission —
   this flips a −5 into a +2

**Do not argue** "mine is better written" or "I found it independently." **Independence
is irrelevant under first-to-find.** **[V]**

**If marked duplicate without participant access, ask to be added as an external
participant.** HackerOne's docs contemplate exactly this, and without it you cannot
verify the duplicate claim. **[V]**

**Self-inflicted duplicates:** consolidate one root cause across subdomains and
endpoints into a **single** report. Filing them separately is a straight path to −5s.
**[V, Orwa]**

---

## 12.9 Mediation etiquette (holds everywhere)

1. **Every platform has a ~3-month-after-closure cutoff.** Dispute early or lose the right.
2. **Argue the metric, not the outcome.** Intigriti asks for *"specific CVSS metrics if
   challenging severity."* A vector with per-metric reasoning is arguable; a bare number
   gets overwritten.
3. **Never go public first.** Discouraged or forbidden on all four platforms.
4. **Respect cooling periods:** H1 ≥7 days since last update · Bugcrowd 7/14 business
   days · Intigriti 30 days between update requests.
5. **Bring new evidence.** Mediation that restates your original claim is explicitly
   rejected on HackerOne.

---

## 12.10 CVSS in 2026

| Platform | Status **[V]** |
|---|---|
| **HackerOne** | Program picks CVSS 3.1 / CVSS 3.0-H1-custom / **CVSS 4.0** / manual. **Severity mandatory since 2026-09-21.** |
| **Bugcrowd** | **VRT priority is primary.** CVSS 3.1 + 4.0 (4.0 opt-in since April 2026). |
| **Intigriti** | CVSSv3 primary, 4.0 emerging. PoC-based vs type-based assessment per program. |
| **YesWeHack** | Metrics assessed per report; **[U]** on the 2026 default version. |

### 3.1 → 4.0 structural changes that move your score **[V]**
- **Scope (S) was retired in 4.0** — removed due to inconsistent scoring *"even by
  CVSS's own designers."*
- **Attack Complexity narrowed and split:** exploit prerequisites moved into the new
  **Attack Requirements (AT)**. In 4.0, AC means *active evasion of a hardening
  mechanism*; AT means *deployment conditions must be present*.

### The eight over-scoring mistakes
1. **Carrying `S:C` from 3.1 habits onto a same-app issue.** Scope change requires
   crossing a *security authority* boundary. Biggest 3.1 inflator — and it doesn't
   exist in 4.0.
2. **`AC:L` when a victim must be logged in, or an unguessable token is needed** — that
   belongs in `AT:P` in 4.0.
3. **`PR:N` when any authenticated session is required** — a self-registered free
   account is `PR:L`, not `PR:N`.
4. **`UI:N` on reflected XSS / CSRF / clickjacking.**
5. **Maxing `C:H/I:H/A:H` off one leaked field.** Reading one user's email is not total
   confidentiality loss. Fastest route from High to Low in a triager's hands.
6. **`AV:N` for something only reachable internally or from localhost.**
7. **Scoring the chain you imagined rather than the one you demonstrated.**
8. **Ignoring existing mitigations** — now an explicit CoC criterion.

### And two under-scoring mistakes (newly costly)
9. Since severity drives **routing**, a genuinely critical finding scored Medium gets
   queued behind other people's Highs.
10. Scoring the **category** instead of the **instance** — generic "IDOR = Medium"
    instead of the specific cross-tenant PII read you actually performed. This also
    wastes the "Varies" VRT upside.

> **The counter to both inflation and program underrating is the same: publish your
> full vector string with a one-line justification per metric.**

**Rule of thumb:** Bugcrowd → lead with the **VRT entry**, CVSS as support. HackerOne
and Intigriti → lead with the **CVSS vector + per-metric rationale**. YesWeHack →
score every metric deliberately; correct CVSS may be worth a literal +1 **[U]**.

---

## 12.11 Impact statements

### The published tests — use them as literal prompts **[V]**

| Source | The question |
|---|---|
| HackerOne triager | **"Why is this important for the business?"** |
| HackerOne *Art of Triage* | Does fixing it **"improve your security posture"**? |
| Hacker101 | **"if this bug were exploited, what could happen?"** |
| Intigriti | **"what can I do with this vulnerability... and why would this be an issue"** |
| YesWeHack | **"demonstrate the current impacts and describe the potential impacts"** |

### Informative vs paid — the structural difference
**Closed Informative:** names a vulnerability class and asserts its textbook
consequences. *"An attacker could steal cookies and take over accounts"* after
demonstrating only `alert(1)`. Generic, class-level, copy-pasted — which Orwa names as
a top mistake.

**Paid:** names (a) the specific asset and data, (b) the trust boundary crossed, (c) the
attacker's starting privilege, (d) what the attacker ends up holding, (e) scale, and
(f) why existing mitigations don't stop it — **with every clause traceable to a step in
your repro.**

### The one-sentence skeleton
> *"An **[unauthenticated / self-registered / low-privilege]** attacker can **[verified
> action]** against **[named asset]**, obtaining **[specific data or capability]** for
> **[scale: any user / all tenants / N accounts]**, without **[the mitigation that was
> expected to prevent it]**."*

### Classes closed Informative unless re-framed **[V on the pattern]**
Self-XSS · clickjacking on logged-out pages · open redirect · missing security headers ·
improperly scoped cookies / "privacy issues without security impact" (named verbatim in
Intigriti's close reasons) · HTML injection claimed as XSS without a WAF bypass · CVE
references without a working PoC · unverified scanner output · reverse-engineered
findings with no real-world attack path · publicly leaked third-party credentials.

**The re-framing rule:** for any low-baseline class, your impact section must terminate
in an **authentication, authorization, or tenancy boundary you actually crossed** — and
you must *show* the crossing, not assert it.

> Where you have the primitive but not the chain, **say so explicitly and score
> accordingly.** Claiming a chain you didn't demonstrate is exactly what converts a
> would-be Informative (0) into an N/A (**−5**).

### Where to declare a chain
YesWeHack has an explicit **bug chaining field**. HackerOne's CoC **requires** you to
*"connect all steps in an attack chain."* Bugcrowd's **"Varies"** VRT entries are the
formal mechanism for arguing above-baseline impact. Intigriti's PoC-based severity means
an undemonstrated chain contributes **nothing**.

---

## 12.12 Operating checklist

**Before writing:** read the brief end to end (*"The brief is the final word"*) ·
confirm the asset is listed exactly as you'll select it · check disclosed
reports/hacktivity for prior art · note the severity method (CVSS 3.1/4.0/manual/VRT,
PoC-based vs type-based) · note the non-qualifying list (YesWeHack closes **RTFS** for
missing it).

**Title:** `<Type> in <specific component/parameter> — <concrete consequence>`,
≤140 chars, no URL on Intigriti, **no hedging**.

**Body, in this order:**
Summary (2–3 sentences, whole finding) → Affected asset + endpoint **as text** →
Preconditions (accounts, roles, setup) → Numbered repro steps, one instruction per line →
Raw HTTP requests **as text**, redacted → Expected vs actual → **Impact: demonstrated
now / potential if chained** (separate paragraphs) → **Mitigations considered and why
they don't block this** → Severity with full vector + per-metric justification → VRT
entry (Bugcrowd) → Remediation suggestion → Testing metadata (timestamp, source IP,
browser/env) → Attachments **on-platform**.

**Then:** run HackerOne's Report Assistant "Run checks" · confirm the report is
understandable **printed on paper with no images** · confirm **one report per root
cause**, not one per subdomain.

**After:** answer NMI within days, not weeks. **If heading for N/A on HackerOne,
self-close (0) rather than absorb −5.** Dispute inside the cooling periods. Argue
**metrics and root cause**, never the outcome or the quality of your prose. Never go
public first.

---

**Next:** [07 — Reporting](./07-reporting-that-gets-paid.md) ·
[11 — Non-Obvious Thinking](./11-non-obvious-thinking.md) ·
[05 — Validation Gates](./05-validation-gates.md)
