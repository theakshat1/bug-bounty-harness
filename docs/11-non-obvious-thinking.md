# 11 — Non-Obvious Thinking (the core principle)

> **"Depth stopped being a moat. Everyone points Codex and Claude at the same scope
> and finds the same bugs, so dupe rate is way up."**
> — Critical Thinking Bug Bounty, HackerNotes Ep. 187, 2026

That is the defining finding of the year, and it sets the whole strategy. When the
agent is a commodity, the differentiator is **(a) which 2% of the scope you aim at**,
and **(b) what non-public knowledge is in the context window.** Two hunters with
identical models and identical scope get identical bugs.

The validation ladder in [05](./05-validation-gates.md) stops you submitting what is
*wrong*. This document stops you submitting what is *already known* — and in 2026 that
is the larger loss.

**Labels:** **[V]** verified against a primary/first-party source · **[S]** secondary or
single-source, directional · **[SYN]** my synthesis — coherent and usable, but **not**
established literature; don't cite it as such.

---

## 11.1 The duplicate is the expensive failure

| Failure | What you spent | What you lost |
|---|---|---|
| **False positive** | hunting + some validation | triage goodwill, signal score |
| **Duplicate** | hunting + validation + proof + **writing** + waiting | **the entire pipeline, for zero** |

A false positive is caught by your own gates, cheaply. **A duplicate passes every gate
you own** — it's real, reachable, impactful, and you proved it — and still pays nothing.

### The audited numbers

**XBOW**, ~1,060 submissions over ~90 days on HackerOne **[V, self-published]**:
```
Resolved     130      Triaged    303      Pending  125
Duplicate    208      Informative 209     N/A       36     New  33
```
Severity mix: 54 Critical, 242 High, 524 Medium, 65 Low. Third-party analysis puts
overall accuracy near **37.5%** — about 1 in 3 reports valid. **[S]**

> **Duplicates (208) ≈ Informatives (209) ≈ 20% each. Roughly 40% of all effort
> produced zero dollars — and the duplicate half were *real, exploitable bugs*.**
>
> **That is a race loss, not a skill loss. You attack it with strategy, not with
> capability.**

**rez0 / xssdoctor hackbot**, 2026 — the best-instrumented recent dataset **[V]**:
- **126 bugs in 5 months; 112 of 126 (89%) confirmed real; 35 of 126 (28%) duplicates.**
  70% High/Critical. Largest single bounty $15k.
- False-positive rate **~80% before** an adversarial validator, **~60% after**.
- Saturation signal: IDOR, broken access control and authn-bypass patterns *"appeared
  repeatedly across different targets."*
- **"Post-authentication attack surfaces yielded substantially higher-quality findings;
  unauth surfaces face heavier competition."** ← directly actionable.

**Low-competition baselines** (for comparison) **[V, academic]**: Chromium ~18.2%
duplicates (σ 4.9% annually); Firefox 1,262 of 6,066 valid reports were duplicates
(~20.8%).

Commonly cited platform figures — HackerOne up to 40% duplicates, Intigriti >50% on
high-competition programs, programs rejecting 50–70% as duplicates or false positives —
all trace to vendor blogs restating each other. **[S]** Treat as directional. Note too
that HackerOne duplicate counts are structurally **under**-reported, because programs
aren't obliged to mark reports duplicate — so true rates are probably worse.

**Honest counterweight [V]:** Rhynorater, mid-2026: *"The volume of reports has gone up,
and I haven't seen a large effect on quality or duplicates."* Not everyone sees the
crisis equally — likely because he hunts where the crowd isn't.

### And the trend confirms the gradient
HackerOne's 2025 HPSR (580k+ validated vulns, $81M payouts) **[V]**:
- *"Five year trend data … shows a rise in vulnerability categories that require
  **understanding how systems work rather than how payloads break them**."*
- Authorization/IDOR/access-control and misconfigurations **rising**; traditional XSS
  **declining from its 2024 peak**.
- *"Reports written entirely by AI are often polished but technically shallow, and
  triage teams can identify them quickly."*
- *"**Deeper understanding continues to be more valuable than surface level
  enumeration.**"*

And HackerOne CEO Kara Sprague, on the limits of even a frontier model **[V]**:
> *"Mythos can't model your business. It can't tell you that the real crown jewel isn't
> in the codebase at all."*

---

## 11.2 Why a checklist cannot make you original

If your method is *"work down a list of bug classes"*, your output is approximately the
**intersection** of everyone else's output — because everyone has the same list. OWASP,
the `hunt-*` skill packs, the nuclei template set: all **shared** knowledge. Shared
knowledge produces shared findings. Shared findings are duplicates.

The 2026 skill-pack ecosystem has converged too: the 7-Question Gate, `hunt-*` naming,
`triage-validation` recur **verbatim** across the major packs — one lineage, copied.

**Therefore** non-obvious ideas must come from **generators** — operations applied to
*this specific target* — never from a list of bugs. That is §11.5.

---

## 11.3 What makes a class duplicate-resistant

My earlier framing was "scanner-findable." The research sharpens it:

> **The real axis is: how many independent observations are needed before the bug
> becomes visible at all?**

One observation, no state, no domain knowledge → everyone finds it.

| Duplicate-**prone** | Why |
|---|---|
| Reflected XSS, esp. marketing/edge pages | single request/response; template coverage; 78% of valid hackbot findings |
| Missing SPF/DMARC, headers, misconfig | zero-effort template |
| Subdomain takeover | continuous-monitoring commodity — everyone's cron runs hourly |
| Spring Boot actuator / exposed debug / open dir / public S3 | agents solved these in ~6–23 steps in Wiz's benchmark |
| Known CVE on a public asset | nuclei template exists within hours of disclosure |
| **Unauthenticated** IDOR on a documented REST endpoint | agents enumerate in one pass; "appeared repeatedly across targets" |
| Login / password-reset basics | the most-tested surface on earth |

| Duplicate-**resistant** | Why |
|---|---|
| Business logic / money-flow abuse | requires modelling what the business *means* |
| Multi-step chains | *"models find atoms but humans still build molecules"* |
| Race conditions / sub-state bugs | needs a conceptual model of hidden intermediate states |
| Multi-tenant isolation, subscription/entitlement logic | needs two accounts, two orgs, and the licensing model |
| **Post-auth deep features** | *"substantially higher-quality findings"* **[V, rez0]** |
| Protocol/parser-level (desync, parser differentials, cache keying) | *"live deep in the HTTP stack, between CDNs, load balancers, and backend servers, and are invisible to most tools"* |
| Second-order / stored-then-consumed | the sink is in a different subsystem than the source; a single-shot agent never revisits |
| Integration / third-party seams | Rosén's $20k came from testing **all 80** integrations |
| Non-English / mobile-only / desktop-only | *"other hunters drop off"* at the barrier |

**Payout asymmetry reinforces it [S]:** surface-level findings average $50–$500;
deep-system findings (authn-bypass chains, payment race conditions, multi-tenant
isolation failure, subscription logic abuse) run $5k–$50k+.

### The empirical AI blind spot — exploit it
Wiz's 2026 benchmark **[V]**: agents solved 9/10 challenges but **failed the one
requiring looking *outside* the target** (secrets in a public GitHub repo) —
*"the AI agents didn't consider accessing this public data source when trying to attack
a secured enterprise system."* A human found an exposed `/rabbitmq/` in ~5 minutes that
the AI missed across ~500 tool calls while fixated on deserialization.

Also: with **broad rather than pinpointed scope, cost rose 2–2.5× and fewer challenges
were solved** — *"without a defined entry point, the agents spread their efforts
haphazardly: they jump between subdomains, test surface-level issues, and are less
likely to dig deeply."*

> **Two hard heuristics fall out: hunt the out-of-band data sources agents ignore, and
> aim narrowly — breadth actively degrades agent performance.**

---

## 11.4 The Obviousness Test (a budget gate, run early)

Score every hypothesis **before** spending proof effort.

### Three disqualifying questions
1. **Would a generic agent, handed this target, propose this in its first ten ideas?**
2. **Would an off-the-shelf scanner or nuclei template find it?**
3. **Is it the textbook first move for this surface type?**

### Crowding score

| Signal | Score |
|---|---|
| A scanner/nuclei template would find it | **+3** |
| Textbook first move for this surface | **+3** |
| Reachable **unauthenticated** | **+2** |
| Surface linked from main UI navigation | **+2** |
| This class already appears in the program's public disclosures | **+2** |
| Single observation — one request/response, no state | **+2** |
| Requires **≥2 chained steps** | **−2** |
| Requires knowing **what the business actually does** | **−3** |
| **Post-authentication, deep feature** | **−2** |
| Requires a non-default account state (suspended, mid-migration, invited-not-accepted, former member, SSO-vs-local) | **−2** |
| Requires reading JS/source/mobile binary to know the surface **exists** | **−2** |
| Feature shipped in the **last 90 days** | **−2** |
| Lives at a **seam** between two subsystems | **−2** |
| API-only, never reachable via UI | **−2** |
| Requires **out-of-band** data (GitHub, archives, job ads, app binary) | **−2** |
| Requires a second tenant to observe | **−1** |
| Other hunters would find the work **tedious** | **−2** |

**Negative total → pursue. Zero or positive → you're racing.**

### Counterweight
A confirmed critical that scores +2 is still worth submitting — impact beats elegance and
being first still wins. The score governs **where you spend hunting time**, not whether
you report something real you already proved.

---

## 11.5 The generators

Twenty operations, `G0`–`G18`. `G14`–`G18` came from the private corpus (see
`corpus/README.md`) and are graded **[S]** — single-source, mostly X posts and vendor
writeups — so treat them as leads with a cheap falsification step, not as established
literature.

Operations on the target. Each produces hypotheses that are impossible to write without
having looked at *this* target.

---

### G0 · Pick the surface, not the bug
**The most-repeated insight in the whole corpus, from two researchers independently.**

> Mark Dowd: **"The attack surface *is* the vulnerability — finding a bug there is just
> a detail."** **[V]**
>
> Orange Tsai: **"A good attack surface achieves twice results with half the effort."** **[V]**

Dowd's core claim: researchers miss bugs **not from technical limits but from lacking
the conceptual frameworks that tell them where to look.**

Orange works **from the architectural level** to find *entirely new attack surfaces
nobody has mentioned*, then mines them for many bugs — ProxyLogon came from a surface
early in Exchange's request-processing pipeline; Apache's **module-interaction** surface
yielded 3 new confusion-attack types and 8 CVEs.

**Operation:** before any request, name the architectural surface you are attacking and
*why nobody has named it before*. If you can't, you're hunting someone else's surface.

**Selection question [V, zhero]:** *"What technology/component is often present but
rarely/less discussed, exploited?"* — maximize **(prevalence in scope) × (minus research
attention)**. The target property is *"almost systematically in-scope."*

---

### G1 · Anomaly ledger — the one input no competitor shares
**[V, Kettle]** — and the highest-leverage generator here.

> *"Treat as a lead anything that makes you say **'this makes no sense'**."*

Kettle's entire race-condition class came from a **7-year-old unexplained anomaly** — a
2016 Facebook report where someone *"somehow succeeded to confirm a random email
address"*, which *"confounded every attempt to visualize what might be happening
server-side."* Years later, systematic investigation produced the **sub-state** reframe:
*"Every HTTP request may transition an application through multiple fleeting, hidden
states."*

> **"Spotting anomalies is the single most important skill for finding race
> conditions."** **[V]**

**Operation:** keep `recon/anomalies.md` **forever**. Log every observation you cannot
explain, even when it isn't exploitable today. Then periodically ask: *what have I seen
that I never explained?*

**Why it's duplicate-proof:** your anomaly log is private by construction. Nobody else
has it.

**Companion technique — benchmark-then-deviate [V, Kettle]:** establish normal behaviour
*quantitatively*, then *"look for clues in the form of any deviation from the benchmarked
behavior."* Read the direction: **faster than expected ⇒ threading or a short-circuit
error path; slower ⇒ locking.**

---

### G2 · Mine the changelog, issue tracker and release notes
**[V, joaxcar]** — the cheapest high-yield technique documented anywhere, and it's
*phone-doable*.

> *"Reading through the release blog posts (especially the monthly security release) has
> probably been the most fruitful for me."*
>
> *"My approach here is very haphazard. It is a mix of reading release notes and looking
> at old bugs and random issues on the GitLab issue tracker."*

**Operation:**
1. Read every **monthly security release** note. For each disclosed bug: understand the
   root cause, then **search for edge cases where developers missed the protection in
   similar code.**
2. Read the public **issue tracker** — it reveals features you didn't know existed.
3. Docs pages list issues/epics under **"version history"** → follow to the **merged
   merge request** → read **which files changed** → now you know exactly where the
   feature lives → test there.
4. Read **discussion threads about problems with a previous fix.** joaxcar found an
   access-control bug this way: **the bug had been reintroduced without the developers
   realising.**

**Supporting number [V, Intigriti]:** *"an average of 3% of a program's reported
vulnerabilities had been previously addressed but have since resurfaced"* — up to **8%**
in some programs, caused by fixes documented-but-not-deployed and reintroduction across
weekly deploys.

> **~3–8% of a program's fixed bugs come back. Regression-retesting is a near-duplicate-
> free lane.** → [`regression-sweep`](../skills/regression-sweep/SKILL.md)

---

### G3 · Variant-hunt every disclosed bug
**[V, Project Zero]** — and the numbers are striking.

| Period | Share of in-the-wild 0-days that were **variants** of already-patched bugs |
|---|---|
| 2020 | **25%** — "1 out of every 4 … could potentially have been avoided" |
| H1 2022 | **~50%** — "at least nine of the 0-days are variants of previously patched vulnerabilities" |
| Full 2022 | **17 of 41 (>40%)** |

Named root cause: *"the execution flow that the proof-of-concept exploits took were
patched, but **the root cause issue was not addressed**."* One WebKit bug *"was
originally fixed in 2013, patch was regressed in 2016."*

Project Zero's own framing, from the Big Sleep work:
> *"By providing a starting point – such as the details of a previously fixed
> vulnerability – we remove a lot of ambiguity from vulnerability research, and start
> from a concrete, well-founded theory: **'This was a previous bug; there is probably
> another similar one somewhere'**."*

And: *"fuzzing is not succeeding at catching such variants,"* while *"for attackers,
manual variant analysis is a cost-effective approach."*

**Why this is duplicate-resistant even though the class is public:**
> **The class is public, but the enumeration of its instances is private.** Everyone
> reads the disclosure; almost nobody does the exhaustive second pass.

**The generalization ladder [SYN, built on PZ + Trail of Bits]:**
```
exact string
  → same sink, different file
  → same sink, different language/service in the monorepo
  → same INVARIANT, different sink
  → same invariant at a different LIFECYCLE STAGE (see G5)
  → same invariant in a fork / vendored copy / mobile client / legacy API version
```
Trail of Bits' `variant-analysis` skill does exactly this — *"systematic pattern
generalization using ripgrep, Semgrep, and CodeQL,"* moving **from exact matches to
broader search patterns while tracking false-positive rates** — because manual hunting
*"stops at the original file or uses one-off grep patterns."*

---

### G4 · Build the scanner the paper's author didn't
**[V, Kettle]** — *"the highest-leverage duplicate-avoidance heuristic in the corpus."*

When new research is published, interrogate it rather than applying it:

> *"Did the researcher miss anything? Did they release a scanning tool? If not, can I
> make one? Does it detect every vulnerability mentioned in the paper?"*

**CL.0 desync was *"overlooked by the community"* precisely because no tool was
released.** Kettle ran permutations against a **20GB Burp project file** of bounty
targets.

> **The gap between a published technique and a published *scanner* for it is where
> non-duplicate bugs live.**

Then there is the structural inversion, which almost nobody acts on **[V]**:
> *"You might think the targets you've tested aren't vulnerable due to WAFs, patches and
> other supposed defences … **Your old targets just became a fertile hunting ground for
> critical vulnerabilities.**"*
>
> *"Go back to assets where you ruled out desyncs. Use the latest techniques … You may
> be surprised (and rewarded!) by what you find."* — $200k+ in two weeks.

**So: after a new technique drops, the most-saturated assets become the *best* targets**,
because they were cleared under the old technique and nobody re-tests.

---

### G5 · Lifecycle tracing
**[Partly V — the state half is Kettle's; the six-stage schema is SYN]**

Kettle's **collision prediction**, verbatim in substance: *"identify objects with
security controls, then locate **all** endpoints reading/writing them."*

Extended into a lifecycle:
```
issue → store → transmit → consume → refresh → revoke → rollback → audit → export → delete
```
Everyone tests **consume**. Prioritize:
- **revoke** — the strongest single lever. Does revocation actually terminate live
  sessions, websockets, in-flight jobs, cached permissions? *"You cannot revoke a
  self-contained token; you can only outlive it."*
- **refresh** — does it re-check authorization, or trust the old grant?
- **export** — does it re-apply the ACL, or dump what the query returns?
- **rollback / undo / cancel / reset** — **the inverted stage, and the least tested of
  all.** When a flow is reversed, which *derived* state does it fail to invalidate? Cached
  pointers, queues, schedulers, denormalized counters, cached entitlements, cached ACLs.
  Everyone tests forward transitions. A kernel SCTP use-after-free came from exactly this
  shape: a rollback path freed its tables but left a cached scheduler pointer dangling. **[S]**
- **delete** — soft-delete still readable?

---

### G6 · Hunt seams, not components
**[V — Dowd, Orange, PortSwigger]**

> **Two components can each be individually correct and the seam still be exploitable —
> which is exactly why single-component scanners never see it.**

Every entry in PortSwigger's 2025 Top 10 was a subsystem disagreement. PortSwigger on
desync: vulnerabilities *"live deep in the HTTP stack, between CDNs, load balancers, and
backend servers, and are invisible to most tools."*

Seams: proxy↔origin · CDN↔app · framework↔runtime · **ORM↔DB** (ORM Leaking, #2 of 2025) ·
serializer↔deserializer · **Unicode normalizer↔validator** (#4 of 2025) · auth
service↔resource service · router↔handler · cache↔origin · queue↔consumer.

At each seam: do both sides agree about **encoding · length/truncation · type · case ·
unicode normalization · duplicate keys/headers · ordering · identity · time · units**?

> The question: **what does one side guarantee, and what does the next side assume?**

---

### G7 · Cross-feature composition
**[V — Orange's Apache module-interaction → 3 confusion types + 8 CVEs; rez0's "atoms vs
molecules"; Kettle's multi-endpoint collisions]**

Enumerate feature **pairs**, not features. The bug lives in the *product* of two
features' assumptions: SSO × invite flow · export × templating · cache × personalization ·
impersonation × audit · soft-delete × re-invite · rate-limit × retry.

Strategically important: **a bug requiring two parts seen at once is one that
partitioned agents miss by design** — the prevailing architecture chunks repos to fit a
context window.

---

### G8 · Workflow / order inversion
**[V, Douglas Day]** — verbatim:

> *"Instead of going through the prescribed workflow and pressing this button after
> hitting that switch, **what if I reverse the process?** … What would happen then? What
> would happen if I change some of the data that feeds the engine, and how could I do
> that?"*
>
> *"About 99% of the time I spend hacking is this **reassembly** stage, reassembling
> something in a way that will achieve an action or outcome that was never intended."*

**Operation:** enumerate the intended step order of a multi-step flow, then run it out of
order, skip steps, repeat steps, run two orders concurrently.

Related and also documented **[V, Kettle]**: *"Carry your assumptions lightly and test
them from different angles wherever possible."*

> ⚠️ **Attribution note.** "Assumption inversion" and "threat-model negation" are
> **not** published frameworks under those names. The substance is Day's workflow
> inversion and Kettle's line above. Use the technique; don't cite a literature that
> doesn't exist.

---

### G9 · Model the developer's corner-cutting
**[V, Inti De Ceukelaire]** — a directly runnable generator:

> *"I try to get in the heads of the developer … **what are the things that they may try
> to cut corners on because it's not super relevant to their business?**"*

**Operation:** rank features by **(security consequence) ÷ (business centrality)**. Hunt
the high-consequence / low-centrality quadrant.

Also from Inti **[V]**:
- *"Hacking, in my opinion, is 80% to 90% using your mind, and 10% using the tools."*
- **Context-aware hacking:** read *all* of a company's documentation and API docs,
  repeatedly — **and read their job postings**: *"browsing the job website is a very good
  idea about, okay, where does this actual company put their resources in."*
- **Constraint as creativity:** *"challenge yourself to limit the scope … it will force
  you to be more creative."*
- On book-learning: studying books *"just teaches you to parrot other people."*

**Related [SYN]: "what did they defend, and what does that tell you?"** Treat each
control as a *confession* of what the team believed the attack was — then ask what other
path reaches the same asset without that control on it. Not documented under this name;
closest anchors are Inti's developer-modelling, Kettle's *"armoured by inconvenience"*,
and Haddix's unique-threat-model.

---

### G10 · The boring/hard-stuff filter
**[V — three independent researchers, same rule]**

> Frans Rosén: **"Focus on BORING/HARD STUFF, other hackers won't."**
> zhero: **"Move toward what others avoid. People are often lazy and avoid complexity,
> or what merely appears to be complex."**
> Kettle: *"If a technique has a reputation for being difficult, fiddly, or dangerous,
> that's a topic in dire need of further research."*

Rosén's concrete instance: worked through **all 80 integrations** in the docs → found one
faulty implementation → **$20k.**

**Operation:** rank candidate work by **how much other hunters would hate doing it.**
All 80 integrations. The 93-page spec. The non-English flow. The mobile-only onboarding.
The archive parser.

> **Treat inconvenience as a duplicate-rate discount.**

Rosén's other high-threshold lanes: SDK/API behaviour across languages and platforms ·
legacy API versions via archived documentation (web.archive.org CDX) · third-party
integrations · IPv6 variants · deprecated-but-functional legacy systems.

---

### G11 · Out-of-band sources agents ignore
**[V, Wiz benchmark failure]** — agents *"didn't consider accessing this public data
source."*

Deliberately include: GitHub repos and gists · package registries · archived docs
(Wayback CDX) · **job ads** · Crunchbase acquisitions · CT logs · app-store binaries ·
support forums · status pages · **orphaned git history** (force-push-orphaned commits are
recoverable from GitHub's public events archive in BigQuery — the signal is the
**zero-commit force push** event).

**And the corollary nobody acts on: a source that blocks your fetcher is equally under-read
by your competitors.** Cloudflare 403s, sign-in walls, Akamai denies, and empty
client-rendered SPAs all cause an agent to silently give up — which makes the content behind
them an under-mined corpus. Keep a fallback chain: curl with real headers ·
`raw.githubusercontent.com` · CERT mirrors · CVE aggregators · the site's own JSON API
(a client-rendered leaderboard usually has a `/api/...` endpoint serving the same data).
This is the G10 inconvenience discount applied one layer up, at the *research input*. **[S]**

---

### G12 · Micro-inspiration against spec text
**[V, HTTP Terminator]** — and note the prompting lesson, which applies to how you run
*any* ideation agent:

> Feed **1–3 sentence fragments** of RFCs/specs/standards — not whole documents —
> because *"models aggressively anchor on all context provided, so every extra sentence
> of prompt risks context-contamination."* Success needed *"a concrete, high-value
> question without being too broad"*, with low-value outputs **explicitly excluded**.

Scale achieved: 138 HTTP/SMTP RFCs → ~15,000 fragments → **30,000 candidate vectors** →
tested against 30,000 authorized sites → **~700 vulnerable targets**, plus an Apache
Traffic Server 0-day.

> **A standards document is an un-mined hypothesis source precisely because nobody reads
> it** (see G10).

---

### G13 · Cascade every hit
**[V, HTTP Terminator]** — *"where human judgment beats autonomy by the widest margin."*

After **any** confirmed finding, two mandatory follow-ups:
> **"How can I detect similar behavior elsewhere?"**
> **"Does the origin enable other attacks?"**

Rationale: *"When you make a significant research discovery, it may contain a clue to
something conceptually nearby."* Kettle on the Shared-Parser Confusion finding:
**"Neither of us would have discovered it alone."** And: *"the true value of an
autonomous research system is unlocked by putting a researcher in the loop in exactly
one place — the discovery cascade."*

> **Never submit the first finding unescalated.** Cascade first.

---

### G14 · Signing-oracle enumeration
**[S — PageBreak findings; primary URL gated, recovered via a third-party summary]**

The sharpest idea in the private corpus, and it is absent from everywhere else in this KB:

> **When an exploit needs a signature, hunt sibling endpoints that will sign
> attacker-controlled values with the same key.**

**Operation:** inventory **every endpoint that produces** a signature, HMAC, or signed
token, and **every endpoint that verifies** one. Build the full producer × verifier matrix
and test each signature at each verifier.

> **A multi-endpoint system's weakest signer is an oracle for its strongest verifier.**

**Why it's duplicate-resistant:** it requires inventorying the whole crypto surface rather
than probing one endpoint — and most testers treat "it's signed" as a terminal defence and
stop. It is also the auth-service↔resource-service seam (G6) made concrete.

---

### G15 · Validate/execute index desync
**[S — Searchlight Cyber WordPress RCE writeup, Jul 2026]**

**Operation:** for every endpoint accepting an array or batch, find where **validation**
iterates and where **execution** iterates. Submit a mix of valid and invalid items, then
check whether a rejected item's *slot* gets filled by its neighbour — i.e. whether an error
path pushes to one of two parallel arrays but not the other.

**Why duplicate-resistant:** it needs two observations (the validated set and the executed
set) correlated **by index**. Single-shot agents never do that.

---

### G16 · Scalar / array type asymmetry at a sink
**[S — same source]**

**Operation:** for every sanitized parameter, send it as a **scalar** and as a
**one-element array**, in both directions, and compare whether the sanitizer still fires.
Sinks that sanitize arrays frequently pass scalars straight through, and vice versa.

**Why duplicate-resistant:** it's one extra bracket, and nobody tries it.

---

### G17 · Self-nesting a batch endpoint
**[S — same source]**

**Operation:** ask whether the batch endpoint accepts **itself** as one of its items. Inner
calls inherit the outer call's already-passed validation.

**Why duplicate-resistant:** it's recursive, it feels silly, and per G10 inconvenience is a
duplicate-rate discount.

Two more shapes from the same research, worth testing wherever they apply: **identity-switch
records** — find every place the app temporarily assumes another identity (impersonate,
run-as, cron-as-owner, webhook-as-installer, support-view) and ask whether the structured
record driving the switch is attacker-influenced; and **concatenated handler namespaces** —
event/hook/permission names assembled from fragments (`status` × `type` × `locale`), where
any user-influenced fragment means part of the namespace is attacker-controlled.

---

### G18 · Secondary-surface tenancy
**[S — AWS Athena cross-tenant class]**

Multi-tenant testing almost always means "can tenant A read tenant B's *data*." Invert it:

**Operation:** enumerate every byte a shared service persists that **derives from** a
tenant's input rather than being the tenant's data — **query text** (the literal values in
`WHERE`/`INSERT`), job names, cache keys, metadata, error strings, blob versions, usage
analytics, scheduler state — and test isolation on **each surface separately**.

**Why duplicate-resistant:** everyone gates result sets. The derived surfaces have no owner,
so nobody gated them. Pairs with the related finding that **old blob/storage versions often
retain secrets after the current version is cleaned**.

---

## 11.6 Research-driven beats recon-driven

> **Recon-driven hunting competes on asset discovery — a race with a horizon of hours.
> Research-driven hunting competes on technique possession — a horizon of weeks to
> months, during which nobody else can even see the bug.**

A new *asset* opens one target. A new *technique* re-opens the **entire previously-
exhausted asset universe at once**. Research-driven hunting has **superlinear reach per
unit of novelty**.

Kettle on why it stays unique: hunt **primitives, not payloads** — *"probe, and
experiment with how targets actually parse requests"* rather than firing pre-canned
exploits. **Pre-canned payloads is precisely what every agent does, which is precisely
where duplicates concentrate.**

### Kettle's topic-selection criteria **[V]**
- **Time-to-abandon is the primary criterion:** evaluate topics by *"how much time I'll
  need to invest before I have enough information to decide whether to abandon it or
  continue."* **Build the experiment that kills the idea fastest.**
- **Fear as a selector:** *"Fear is a great indicator of something I don't fully
  understand, and challenges that I don't know how to tackle."*
- Optimize for **transferable technique**, not direct impact.
- Deliberately pick topics **outside your specialism**.
- *"Every time you read a good quality blog post, read the entire archive."*
- *"No idea is too stupid."*
- And: **don't over-think topic choice.**

### The practical blend
Use agents for recon-driven breadth to pay the bills; spend a fixed fraction (20–30%) of
your time going **deep on one technology, protocol or framework your targets share**.
The deep work is what nobody can duplicate.

Sam Curry's version **[V]**: **one program at a time** — *"I love digging deep and am
unable to focus if I'm trying to find vulnerabilities on multiple targets at once"* —
and stay only where there is **active development or large scope**.

Shubs' version **[V]**: *"I was able to come up with a methodology … by having a deep
understanding of their architecture, and development practices. This was absolutely key
to my success."*

---

## 11.7 Timing — prefer the comprehension race

| Window | Evidence | Verdict |
|---|---|---|
| **New program launch** | *"professional hunters will find everything findable within hours of launch"*; HackerOne historically saw the first vuln reported to **77% of customers within 24 hours** | A **speed** race you will lose to a thousand agents |
| **Scope addition** | freshly added assets pay better | Speed race |
| **New product/feature** | joaxcar's release-notes loop; Haddix's "shift left" | Speed race, but cheapest to automate |
| **Newly published technique** | Kettle: **$200k+ in two weeks** post-publication; CL.0 overlooked because no scanner shipped | ✅ **A *comprehension* race — prefer this one** |

> **Comprehension is the thing agents still don't have. Compete there.**

**Program age as a saturation proxy [V, Akgul et al., USENIX Sec '23, n=56/159/24]:**
submission volume shows **power-law decay after launch**; **11 of 24 interviewees used
program age as a proxy for saturation**, expecting younger programs to hold more bugs.
VDPs have far fewer participants and correspondingly lower duplicate rates (no cash → no
crowd) — useful as a low-duplicate training ground.

---

## 11.8 First-principles novelty sources
Ranked by evidence strength **[V unless noted]**:

1. **New features / recent deploys** — fewest eyes by definition. Haddix's "shift left."
2. **Framework internals**, especially newly-popular frameworks. Kettle on Next.js cache
   chains: *"shows how framework internals hide 'scary' overlooked attack vectors."*
   2026 nominations are Next.js-dominated.
3. **New protocols / standards / RFC text** — *"rewards researchers willing to study RFCs
   and build custom tools"*, and *"old flaws resurface in fresh code."*
4. **Recently acquired companies** — inherited then forgotten; acquirees don't hold the
   parent's standards. Mechanics: Crunchbase → Acquisitions → each domain → full recon.
   Real datapoint: **$50,500** for a supply-chain flaw in a newly acquired firm.
5. **Migrated infrastructure / temporal windows** — Shubs: a protection *"accidentally
   disabled … for a short period of time"*, or a sensitive asset spun up without SSO.
   Structurally **duplicate-free, because the window closes.** Requires monitoring, not
   scanning.
6. **Deprecated-but-live code** — `/api/v1` while prod is v3; removed from docs, never
   disabled on the backend.
7. **Undocumented APIs** — mobile/desktop clients and SPA bundles reveal endpoints no web
   user hits.
8. **Bespoke internal tools accidentally exposed** — the `/rabbitmq/` case. (Spring Boot
   actuators are now duplicate-prone; *bespoke* internal tooling is not.)
9. **Non-English / localized, mobile-only, desktop-only** — *"other hunters drop off."*
   Localization also **forks validation logic** (different regex, normalization, date and
   currency parsing) — i.e. a seam.
10. **Orphaned git history** — see G11.

---

## 11.9 Anti-patterns that guarantee duplicates

| Anti-pattern | Why | Source |
|---|---|---|
| **Nuclei against everything in a public scope** | *"to scan what everyone else is scanning — you are merely going to find dupes"* | Haddix **[V]** |
| **Concluding "this program is saturated" from generic nuclei output** | *"produces enormous output, most of which is informational and buries the actual attack surface under noise… Hunters triage for hours, find nothing critical, and conclude the program is 'saturated'."* A false negative masquerading as market analysis | **[S]** |
| **Pointing an agent at the whole scope** | **2–2.5× cost, fewer solves**; *"agents spread their efforts haphazardly … less likely to dig deeply"* | Wiz **[V]** |
| **Testing login/reset first** | most-tested surface in existence | — |
| **Submitting the first thing you find** | the first thing you find is the first thing everyone finds. **Cascade from it and submit the escalated version** | HTTP Terminator **[V]** |
| **Following a popular methodology verbatim** | a published methodology is a *shared* methodology; outputs converge. Inti: it *"just teaches you to parrot other people"* | **[V]** |
| **Hunting whatever programs streamers are on** | attention *is* the duplicate driver | zhero **[V]** |
| **Unauthenticated-only testing** | unauth is where competition concentrates; post-auth yields substantially higher quality | rez0 **[V]** |
| **Pre-canned payloads instead of primitives** | payload libraries are exactly what's shared | Kettle **[V]** |
| **Submitting unvalidated AI output** | 60–80% invalid (Synack); *"polished but technically shallow, and triage teams can identify them quickly"* | **[V]** |
| **Discarding anomalies you couldn't exploit today** | **you just threw away the only thing that was uniquely yours** | Kettle **[V]** |

---

## 11.10 The two moves that actually differentiate in 2026

From the CTBB Ep.187 analysis, and the single most actionable pair in this document:

> **1. "Point the agent at niche surface. The hunters landing more bugs than everyone
> else are running AI on a small part of the scope nobody else is looking at."**
>
> **2. "Seed it with your own expertise. Feed the prompt your past reports and program
> notes so the agent inherits real program-specific knowledge."**

And: *"The general lesson is that trying things got cheap. Anytime you think 'it would be
nice to have this,' build it."*

Corroborating **[V]**:
- **Rhynorater:** his stack is four Claude Code panes, but the differentiator is
  **encoding a personal methodology into the harness**, not the harness — *"Having a
  strong conceptual knowledge really helps at this point because AI can just remove all
  friction to implementing attack vectors."* **The bottleneck moved from execution to
  hypothesis.**
- **rez0 on why their bot beat others using the same models:** *"Most real bugs only
  appear because **a human decides not to give up after the first dead end**."* Their loop
  kept investigating past the point other assessments stop.
  → **Persistence-past-first-dead-end is a configurable parameter, and almost nobody
  turns it up.**
- **aituglo:** *"AI is a multiplier, not a replacement. **If you multiply zero by a
  thousand, it's still zero.**"*
- **Survey:** 58% of researchers say AI misses business logic and chained exploits; only
  12% believe AI could replace them.

---

## 11.11 How this changes the pipeline

```
   SCOPE → RECON → ✦ IDEATE ✦ → ✦ OBVIOUSNESS FILTER ✦ → HUNT → DISPROVE
                        │                  │                        │
              run the generators    kill crowded ideas        ✦ CASCADE ✦
              against this target   BEFORE proof budget    "where else? what else?"
                                                                    │
                                                    RE-VERIFY → HUMAN → REPORT
```

Three rules:
1. **Ideate before hunting.** 15–25 hypotheses, score them all, hunt the best 3–5. The
   first idea you have is definitionally the obvious one.
2. **The obviousness filter is a budget gate**, not a quality gate.
3. **Cascade every confirmed finding** before reporting it.

Implemented as [`hypothesis-forge`](../skills/hypothesis-forge/SKILL.md) and the
[`ideator`](../agents/ideator.md) subagent — kept separate from the hunter because **an
agent that must both invent and prove biases toward hypotheses that are easy to prove,
which are the obvious ones.**

---

## 11.12 The one-page version

> **Obvious ideas are negative-value: full pipeline cost, zero return.** ~40% of the
> one audited agent dataset was duplicates and informatives — and the duplicates were
> *real bugs*, lost to a race.
>
> **Depth stopped being a moat.** Your competition is a generic agent on the same scope.
> So: **aim at niche surface, and seed the context with knowledge nobody else has** —
> your anomaly ledger, your past reports, your program notes.
>
> **Pick the surface, not the bug.** Mine changelogs. Variant-hunt every disclosure.
> Hunt seams, lifecycles (especially *revoke*), feature pairs, post-auth depth, and the
> boring work others skip. Build the scanner the paper's author didn't.
>
> **Score for crowding before spending proof effort. Cascade every hit. Never submit the
> first finding unescalated.**

---

## 11.13 Honest caveats

- Most 2026 duplicate-rate percentages (40%, 50–70%, 30–40%) trace to vendor blogs
  restating each other. The only **audited** figures here are XBOW's self-published
  breakdown, rez0's 126-bug log, and the Chromium/Firefox academic counts.
- HackerOne duplicate counts are structurally **under**-reported.
- **"Assumption inversion"** and **"threat-model negation"** have no published literature
  under those names. **"Defended-treasure inversion"** is likewise my synthesis. The
  substance is attributable (Day, Kettle, Inti, Haddix) — the labels are not.
- The six-stage lifecycle schema is a synthesis; the *state* half of it is Kettle's.
- Not everyone reports a duplicate crisis — Rhynorater explicitly doesn't. Consider that
  evidence for the "hunt where the crowd isn't" thesis rather than against the data.

---

**Next:** [12 — Triage & Report Mechanics](./12-triage-and-report-mechanics.md) ·
[05 — Validation Gates](./05-validation-gates.md) ·
[06 — Target Selection](./06-target-selection.md)
