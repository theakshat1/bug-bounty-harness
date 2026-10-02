# 01 — The 2026 Landscape (what actually changed)

> Read this before you tune a single prompt. Target selection and evidence
> standards changed more in 2026 than any technique did, and most of what is
> written about it online is wrong in a specific, load-bearing way.

Every claim below is labelled. **[V]** = verified against a primary source
(platform press release, changelog, official blog, arXiv paper). **[S]** =
single-source or secondary, treat as indicative. **[U]** = could not confirm.

---

## 1.1 Correct the record first

Four claims circulate constantly in 2026 bug bounty commentary. Three are
distortions, and believing them leads you to the wrong strategy.

### ❌ "HackerOne paused submissions"
**Wrong.** The pause applied to the **Internet Bug Bounty (IBB)** only — a single
HackerOne-run program that funds *open-source* vulnerability research (Django,
Rails, Apache). Paused to new submissions **2026-03-27**. The main platform never
stopped accepting reports. **[V]**

HackerOne's stated reason was **remediation capacity**, not report quality: the
balance between findings and open-source maintainers' ability to ship fixes
shifted. Then on **2026-05-18**, IBB payouts were cut 76–89% (Critical
$9,250 → $2,257; High $4,429 → $1,009; Medium $1,843 → $297). **[V]**

### ❌ "Volume is up 76% but only 25% are real — it's all slop"
**This is a misreading of HackerOne's own data, and it inverts their meaning.**

What HackerOne actually said (H1 Validation press release, **2026-04-21**): **[V]**
- Submissions grew **76% year over year**, peaking March 2026.
- "About **25% of findings were confirmed exploitable, a rate that has held
  steady** despite the surge."
- Their framing: "the absolute number of real vulnerabilities continues to grow."

A **flat** signal rate against a 76% larger denominator means the number of *real*
bugs grew ~76% too. The surge was not mostly noise.

**Why this matters to you:** the bottleneck is **triage labour**, not researcher
honesty. The market is not short of bugs — it is short of people who can confirm
them. That tells you exactly where to compete: supply confirmation, not volume.

(Separately, HackerOne reported a **100%+** volume spike after February 2026
model releases. Different window, different metric — don't conflate the two. **[V]**)

### ❌ "Project Glasswing gives researchers a super-model"
**No.** Glasswing is **Anthropic's** invite-only access program for **Claude
Mythos**, a frontier model never publicly released specifically because of its
vulnerability-finding capability — the first time a frontier lab withheld a model
on offensive-cyber grounds. **[V]**

Access is organizational, security-vetted, and prioritizes operators where an
attack could affect >100M people (AWS, Apple, Cisco, Google, Microsoft, NVIDIA,
Linux Foundation, HackerOne, and ~150 more orgs as of 2026-06-02). It found
**>10,000 high/critical flaws** across partners. **[V]**

**It is not available to independent researchers.** Don't plan around it.

### ✅ What IS true: the cost asymmetry
The real mechanism, well put by researcher Jakub Ciolek: finding plausible bugs
got much cheaper and report generation scales trivially; but *verifying impact,
deduplicating, deciding whether a boundary actually breaks, and shipping a safe
fix* remain expensive and human. **[V]**

Every policy change below is an attempt to reprice that asymmetry.

---

## 1.2 Platform policy, as of October 2026

The best dataset is the **Stingrai census** (2026-07-28, 53 programs across 4
platforms, 20 vendors, 29 OSS projects, fixed-date retrieval with a coding
rubric): **[V]**

- **0 of 53 ban AI-assisted submissions.**
- **Only 3 require you to disclose AI use: Intigriti, Django, FFmpeg.**
- 16 (30%) address AI at all → 13 require human verification, 11 require working
  reproductions, 8 reject fully autonomous submission.
- **36 (68%) have no stated AI policy** — including Microsoft, Meta, AWS, Shopify,
  Kubernetes, Node.js, PostgreSQL, Rust.
- All four coordination platforms impose human-in-the-loop via code of conduct,
  which binds every program they host.

> **The industry standard is human accountability, not tool restriction.**
> Disclosing AI use is almost never required. *Proving the bug* always is.

### Per-platform specifics

| Platform | What changed | Date | **[V]** |
|---|---|---|---|
| **HackerOne** | AI explicitly "permitted and encouraged" across the whole workflow. No AI disclosure required. But: "The use of AI does not change the requirement to **validate findings, connect all steps in an attack chain, and provide a clear, reproducible proof-of-concept demonstrating a real vulnerability and its impact**." | CoC, updated May 2026 | V |
| HackerOne | **Mandatory identity verification** for all Bug Bounty submissions (web, Report Assistant, API). VDPs stay open without IDV. | phased 2026-08-05 → 08-17 | V |
| HackerOne | **Severity mandatory at submission** (BBP, VDP, Challenge). Triage routes on it — mis-severity now costs you queue position. | 2026-09-21 | V |
| HackerOne | TriageOne smart routing separates "a highly experienced, trusted researcher from a newly created account backed solely by automated tooling." | 2026 | V |
| HackerOne | Penalty ladder: reputation hit → rate limiting → **loss of private program eligibility** → extra verification → suspension → removal. Automated delivery from scanners/scripts/browser automation = full ban. | — | V |
| **Bugcrowd** | Four measures (their term for the problem: *"sloptimism"*): submission-farming bans at **≥10 invalid reports**; **mandatory IDV** for all Managed Bug Bounty; **submission throttling** (caps on concurrent open reports for low-quality accounts); **CAPTCHA on all submissions**. | 2026-05-18 | V |
| Bugcrowd | 30-day suspension for AI-attributed submissions without manual validation at ≥10 invalid. No AI disclosure required. | Nov 2025 CoC | V |
| **Intigriti** | **The one platform that requires AI disclosure:** "Be open and transparent about the use of AI." Unverified AI output may be **closed without response**. Also bans placeholder reports filed to claim duplicates. Sanctions include **payment restriction** (keep access, forfeit all rewards). | 2026-03-09 | V |
| Intigriti | Strategy of **"intelligent friction"**: higher per-category PoC standards, reproduction standards, evidence expectations including **short video**. Explicitly splits the market into *volume reporting programs* (lower pay, automation-tolerant) vs *expert programs* (higher pay, low volume, collaborative). | upd. 2026-08-08 | V |
| **GitHub** | Program restructured. Public payouts roughly halved; top rates moved to an invite-only VIP tier. Signal threshold on the public program, with ~4 submissions of runway for new researchers. | 2026-07-22, effective 07-27 | V |
| GitHub | Earlier bar-raising: **working PoC** ("Show us the impact, don't just describe it"), scope awareness, tool validation. Low-impact findings now get **swag instead of bounty**. | 2026-05-15 | V |
| **GitLab** | New reproduction-artifact requirement attributed directly to AI-generated submissions; reports lacking verifiable evidence closed as N/A. | 2026 | V |
| **Immunefi** (web3) | Strictest PoC bar in the industry, and it predates the AI wave: a valid PoC must be **runnable attack code** (Foundry/Hardhat test, or a contract whose functions trigger the exploit). Structurally slop-proof. | ongoing | V (no dated 2026 AI policy found — **[U]**) |
| Others that retrenched | Intel suspended a program paying up to $100K → moved to Intigriti **rewardless** disclosure (~Sept 2026, Intel gave no public reason **[U]**). curl ended bounty payments. Nextcloud suspended paid rewards citing AI volume. Linux kernel security list called "almost entirely unmanageable" by Torvalds. | 2026 | V/S |

### GitHub's VIP ladder — the clearest published path to premium tiers **[V]**

| Severity | Public | VIP (invite-only) |
|---|---|---|
| Low | $250 | $1,000 |
| Medium | $2,000 | $7,500 |
| High | $5,000 | $20,000 |
| Critical | **$10,000** | **$30,000+** |

**Qualification: 1 critical, OR 2 highs, OR 4 mediums, OR 7 lows.**

GitHub's thesis, verbatim: *"you don't earn more by submitting more. You earn more
by submitting better."*

**Strategic read:** across platforms, **private/VIP program access is now the
primary economic reward for signal quality**. HackerOne's penalty ladder puts
"loss of private program eligibility" *above* rate limiting. Intigriti
deliberately architects a two-tier market. Reputation stopped being cosmetic and
became the gate on the only tier where payouts held up.

---

## 1.3 What autonomous agents are actually good at (and what that means for you)

The single most honest signal in the market is **XBOW's** public record: **[V]**

- Reached **#1 on HackerOne's US leaderboard** (~1,060 reports in ~90 days, Aug 2025).
- Topped it on **reputation, not earnings**.
- Outcome split: 132 confirmed/resolved, 303 triaged, 125 under review,
  **208 duplicates, 209 informative**.
- **Has earned under $40,000 total since Feb 2024.**
- Across all hackbots: 1,100+ submissions, ~half valid — and **78% of *valid*
  hackbot findings were XSS.**

> **Autonomous agents are, at scale, XSS machines.** XSS is the most crowded and
> least paid class there is. The leaderboard rewards volume; your bank account
> rewards scarcity.

**Competing with agents on their strongest class is the worst target-selection
decision available in 2026.** See [06 — Target Selection](./06-target-selection.md).

### The lab-to-real gap **[V]**
- GPT-4-class models exploit **87%** of one-day CVEs *when handed the advisory
  description* — but agents solved only **13%** of real CVEs in CVE-Bench
  (25% when given vulnerability descriptions). Hard HackTheBox: near zero.
- Multi-agent hierarchical beats single-agent **4.3×** (HPTSA).
- Fine-tuned mid-scale beats bigger general models: xOffense (Qwen3-32B) 79.17%
  sub-task completion over GPT-4 and Llama 3.
- **"70% of critical web vulnerabilities are business logic flaws — no autonomous
  agent reliably detects these."**
- Agents are reliable on: known CVEs in unpatched services, SSRF, injection,
  misconfiguration, default credentials, standard SQLi/XSS/traversal.
- Agents consistently miss: business logic, multi-step chains, GUI-dependent
  bugs, genuinely novel issues.
- **ARTEMIS** placed highly against professional pentesters on a live 8,000-host
  network but produced **higher false-positive rates than every human
  participant**. Cost near parity with human testers. **[S]** — two sources give
  contradictory figures ($18/hr beating 9 of 10 humans vs $59/hr placing 2nd);
  **don't cite either number.**

> *"Every headline success included human review before submission."*

---

## 1.4 Why companies are retrenching: the in-house economics

**Shopify's "Dispatch" harness** is the clearest published data point, and it
explains the payout cuts better than any AI-slop narrative: **[V]**

> 6 weeks · thousands of scans · 80+ applications → **300+ findings**,
> conservatively valued at **$400,000+** in equivalent bounty payouts, including
> 2 criticals. Cost: **$50–300 per full scan, $5–50 incremental.**

That is roughly three orders of magnitude of gross margin on in-house scanning
versus external bounty prices — **for the commoditized classes**.

**This is the actual driver behind the retrenchment in §1.2.** Companies worked
out it is cheaper to find these bugs themselves. Bounties survive precisely where
in-house agents still fail: business logic, authorization intent, and compositional
risk. Plan your hunting accordingly.

See [04 — Harness Architecture](./04-harness-architecture.md) for what to copy
from Dispatch's design.

---

## 1.5 The structural reason slop exists (and won't be prompted away)

From *"AI Slop and Hallucinations in Vulnerability Assessment"* (arXiv
**2608.25667**, Aug 2026, SiMLA 2026): **[V]**

- Defines AI slop precisely: **hallucinated vulnerabilities, plausible but
  incorrect patches, and semantically repackaged bug reports** — and frames the
  burden on human triage as *functionally a denial of service*.
- **Root cause:** security experts reason **deductively**; LLMs generate
  **autoregressively/probabilistically**. The gap is **structural, not a
  prompting problem**.
- Chain-of-thought and tool-use help but **do not close it**.
- Prescription: **active neuro-symbolic verification** over passive slop
  detection — don't try to classify slop, make the pipeline *prove* things.

Note **"semantically repackaged bug reports"** as a named failure mode:
paraphrased duplicates that evade string-match deduplication. If your harness
emits these you will look like a farmer even when your bug is real.

**The engineering conclusion is the same one Shopify reached empirically and the
one this whole knowledge base is built on: you cannot prompt your way out of
hallucination. You have to build an oracle outside the model.**

---

## 1.6 The one-paragraph synthesis

The market stopped paying for **finding** and started paying for **proving**.
Discovery is commoditized — agents do it cheaply and companies now do it in-house
at ~1/1000th of bounty prices. Confirmation is not commoditized: the best
published automated exploit-confirmation result caps around **30%** (AXE), 70% of
true positives still resist automation, and the signal rate across the whole
HackerOne platform has sat flat at 25% through a 76% volume surge. The money that
remains is concentrated in classes where confirmation requires understanding what
the application is *supposed* to do — business logic, authentication and
authorization implementation, agentic/MCP authorization, and compositional
multi-commit risk — because that intent is not in the code, and therefore not in
any model's context.

---

## 1.7 Source discipline

This topic has an unusually bad secondary-source problem. A large volume of 2026
content recycles the same handful of numbers while **inverting HackerOne's
meaning** — turning "25% exploitable, rate held steady" into "only 25% are real,
so the growth is noise." The second does not follow from the first and HackerOne
never said it.

**Anchor on primary sources only:**
`hackerone.com` press releases · `docs.hackerone.com` changelogs ·
`bugcrowd.com/blog` · `kb.intigriti.com` · `github.blog` ·
`shopify.engineering` · `anthropic.com` · `arxiv.org` · `theregister.com`

Treat everything else as commentary.

---

**Next:** [06 — Target Selection](./06-target-selection.md) ·
[05 — Validation Gates](./05-validation-gates.md) ·
[04 — Harness Architecture](./04-harness-architecture.md)
