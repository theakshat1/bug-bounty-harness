# 05 — Validation Gates (the moat)

> **The thesis of this entire knowledge base:** in 2026, finding candidate
> vulnerabilities is cheap and nearly commoditized. *Proving* them is the scarce
> skill. Your competitive advantage is not a better hunting prompt — it is a
> brutal, automated, disprove-first validation pipeline that kills 95% of your
> agent's output before you ever see it.

Every serious system converged on this independently: Google's PageBreak pairs
LLM hypotheses with deterministic non-AI validators; Cloudflare's audit skill runs
fresh verifiers whose job is to *disprove* candidates; Crusader requires confirmed
working impact before triage; Shopify's harness demands a real passing test as
proof. Different teams, same conclusion.

---

## 5.1 Why this is the whole game

A hunting agent pointed at a real target produces findings at roughly this ratio:

```
100 candidates from the hunter
 ├─  60  not real at all (hallucinated sink, misread control flow, imagined param)
 ├─  25  real code pattern but UNREACHABLE (dead code, gated upstream, needs
 │        a precondition that doesn't exist in the deployed config)
 ├─  10  real and reachable but NO IMPACT (self-XSS, info leak of public data,
 │        "vulnerability" the program documents as accepted risk)
 ├─   4  real, reachable, has impact — but DUPLICATE or already known
 └─   1  actually payable
```

Note which bucket is the expensive one. The 60 hallucinations die cheaply at Gate 1.
The **4 duplicates survive every gate** — you pay recon, hunting, reachability, impact
analysis, proof *and* write-up, then collect nothing. In an AI-saturated market that
bucket is much larger than 4: of the ~1,060 reports in the one public agent dataset,
**208 were duplicates and 209 informative.**

That is why this document is only half the system. Validation stops you submitting
what's *wrong*; [11 — Non-Obvious Thinking](./11-non-obvious-thinking.md) stops you
submitting what's *already known*, and it has to run first because it's the one that
governs where the budget goes.

Submitting the 100 destroys your reputation and the program's trust. Submitting
the 1 gets you paid. Everything below is about building the sieve.

**The economic asymmetry:** a false positive costs you triage goodwill, signal
score, and eventually program access. In 2026 those are harder to rebuild than
they used to be — platforms tightened policy specifically in response to
unverified AI submissions. Treat every unverified submission as spending down a
finite, slow-regenerating resource.

---

## 5.2 The core principle: separate DETECT from PROVE

Never let the component that proposes a bug be the component that confirms it.
An LLM asked "is this a vulnerability?" after it just said it was will agree with
itself. This is the single most important architectural rule in the harness.

```
┌───────────┐  candidate   ┌────────────┐  confirmed   ┌────────────┐
│  HUNTER   │ ───────────▶ │  VALIDATOR │ ───────────▶ │   HUMAN    │
│ (creative,│              │ (adversarial│             │  (final    │
│  broad,   │              │  skeptical, │             │   submit   │
│  cheap)   │              │  fresh ctx) │             │  decision) │
└───────────┘              └────────────┘              └────────────┘
     ▲                            │
     │      rejected + reason     │
     └────────────────────────────┘
          (feeds the negative ledger)
```

Three non-negotiable properties:

1. **Fresh context.** The validator must not see the hunter's reasoning — only the
   claim and the raw target. If it sees the hunter's argument, it inherits the
   hunter's errors. In Claude Code this means a *separate subagent invocation*,
   not a follow-up turn.
2. **Inverted incentive.** The validator's instruction is "disprove this," not
   "check this." Asked to check, a model finds reasons to agree. Asked to
   disprove, it finds the gate you missed.
3. **Deterministic where possible.** Prefer a script, a curl, a status-code diff,
   or a test that fails-then-passes over any model judgment. A validator that
   doesn't use an LLM at all cannot hallucinate. This is PageBreak's central
   insight and it is why their FP rate is low enough to be usable.

---

## 5.3 The gate ladder

A candidate must pass **every** rung in order. Failing any rung kills it. Each
rung is cheaper than the next, so order matters for cost.

### Gate 0 — Scope
*Is the asset in scope, and is the technique permitted?*

Mechanical allowlist check. Automated, hard-fail, no LLM judgment. If the host
isn't on the list the candidate dies here regardless of merit.
→ See [09 — Scope](./09-scope-authorization-and-ethics.md).

### Gate 1 — Existence
*Does the code/endpoint/parameter the hunter described actually exist?*

The cheapest and highest-yield gate; it alone kills most of the 60% hallucination
bucket. Re-read the cited file at the cited line. Re-request the cited endpoint.

- The cited line must contain what the hunter claims it contains.
- Grep the symbol independently. If the function doesn't exist, done.
- For web targets: the endpoint must return something other than 404/405 and the
  parameter must be acknowledged.

**Required artifact:** exact `file:line` with a quoted snippet, or a raw HTTP
response. No paraphrase accepted.

### Gate 2 — Reachability
*Can an attacker actually reach this from outside, in the deployed configuration?*

This is where the 25% "real but unreachable" bucket dies, and it's the gate most
hunters skip.

- Trace an unbroken call chain from a **public entrypoint** to the sink. Every
  hop must be named. A chain with a "then somehow reaches" step is a failed gate.
- Identify every guard on the path: auth middleware, feature flag, config default,
  WAF rule, role check. For each, state why it does *not* stop you.
- Non-default configuration is a severity reduction and often a rejection. If the
  bug requires a setting nobody uses, say so explicitly.

**Required artifact:** the named chain, hop by hop, plus the guard analysis.

### Gate 3 — Impact
*What does an attacker actually gain? Name the security boundary that breaks.*

This kills the 10% "real but no impact" bucket.

- Name the boundary: tenant A → tenant B, anonymous → authenticated, user → admin,
  read → write, in-process → host.
- "Information disclosure" is not impact until you name the information and why
  it's sensitive. Leaking a public UUID is not a finding.
- Self-inflicted-only (self-XSS, self-IDOR) is not a finding absent a chain.
- Check the program's explicit **accepted-risk / out-of-scope** list. Many
  perfectly real bugs are documented non-issues, and submitting them anyway is a
  signal-score hit.

**Required artifact:** one sentence of the form
*"An unauthenticated attacker can `<verb>` `<asset>` belonging to `<victim>`."*
If you can't write that sentence, there is no report.

### Gate 4 — Proof
*Demonstrate it on a live, authorized target, safely.*

- Two accounts you both control for any isolation/authz bug.
- Deterministic and repeatable: run it twice, same result. Intermittent means
  you don't understand it yet.
- Minimum necessary blast radius — one record, not the table.
- Capture the request/response pair, redacted.

**Required artifact:** reproducible steps a triager can follow in under 10 minutes,
plus raw evidence.

### Gate 5 — Novelty
*Is this already known?*

- Search the program's public disclosures and changelog.
- Check CVE/advisory feeds for the component and version.
- If it's a known class on a sibling endpoint, that's often still payable — but
  say so up front; it builds credibility and pre-empts a duplicate close.

> ⚠️ **This gate is placed badly on purpose, and you should not rely on it.**
>
> By the time a candidate reaches Gate 5 you have already paid for recon, hunting,
> reachability analysis and proof. Discovering *here* that fifty other agents found the
> same thing means you spent the whole pipeline for nothing — and unlike a false
> positive, a duplicate passes every other gate, because it's real.
>
> The crowding check therefore belongs **before hunting**, as a budget gate, not here
> as a quality gate. Gate 5 is the last-chance backstop; the real filter is the
> **Obviousness Filter** in [11 — Non-Obvious Thinking](./11-non-obvious-thinking.md),
> run at hypothesis time via the `hypothesis-forge` skill.
>
> Keep Gate 5 — a public disclosure you missed is worth catching late. But if Gate 5 is
> where you *usually* learn an idea was crowded, your pipeline is mis-ordered.

### Gate 6 — Human
*Would you defend this in front of the engineer who wrote the code?*

You, personally, reading it. No exceptions, no automation.

### Gate 7 — Cascade (before you report, not after)
*What else does this finding tell you?*

After **any** confirmed finding, two mandatory questions:

> **"How can I detect similar behavior elsewhere?"**
> **"Does the origin enable other attacks?"**

Rationale: *"When you make a significant research discovery, it may contain a clue to
something conceptually nearby."* This is documented as the single place where human
judgment beats autonomy by the widest margin — *"the true value of an autonomous research
system is unlocked by putting a researcher in the loop in exactly one place — the
discovery cascade."*

Practically: run variant analysis on your own finding's root-cause shape before
submitting. **Never submit the first finding unescalated** — the escalated version is
worth more and is far less likely to be a duplicate.
→ [11 §G13](./11-non-obvious-thinking.md)

### Gate 8 — Verify the fix (post-resolution, and a first-class stage)
*Did the patch actually hold?*

Most pipelines terminate at "report submitted." Make the loop close **[S]**:

> **Queue every resolved report for a regression retest, automatically, at the moment it
> resolves.**

Why this is a gate and not an afterthought:
- A fix is **new code** written under time pressure, often by someone who didn't write the
  original — and ~**3–8%** of a program's fixed bugs regress.
- You already hold the full context of how the bug worked, which nobody else does.
- Bypasses of shipped fixes are frequently paid in full and are duplicate-resistant.
- The patch may have fixed only **the path your PoC took**, not the root cause — which is
  the single most common variant-bug origin (see [11 §G3](./11-non-obvious-thinking.md)).

Operational shape worth copying: keep **leads as plain Markdown** so they survive tool
changes and agents can draft against them without lock-in; treat the **platform as the system
of record and any local database as a cache**; and cross-reference CVE/advisory feeds against
your program's assets continuously rather than per-campaign.

→ [`regression-sweep`](../skills/regression-sweep/SKILL.md)

---

## 5.4 The disprove prompt

This is the highest-leverage prompt in the harness. The framing is the point.

```markdown
You are a skeptical senior application security engineer. A junior researcher
claims the vulnerability below exists. Your job is to DISPROVE it.

You have NOT seen their reasoning and you should not ask for it. Work only from
the claim and the actual target.

CLAIM:
  Class:      {vuln_class}
  Location:   {file:line | endpoint}
  Assertion:  {one_sentence_claim}

Work through these in order. STOP at the first failure and report it.

1. EXISTENCE   — Read the cited location yourself. Does it contain what is
                 claimed? Quote the actual content. If not: VERDICT=FALSE.
2. REACHABILITY— Build the call chain from a public entrypoint to the sink.
                 Name every hop. Name every guard on the path and why it does
                 not stop the attack. If you cannot complete the chain without
                 an assumption: VERDICT=UNPROVEN and name the missing link.
3. IMPACT      — Name the security boundary crossed. Write the sentence
                 "An attacker with <access> can <verb> <asset> of <victim>."
                 If you cannot: VERDICT=NO_IMPACT.
4. PRECONDITIONS— List every precondition. Mark each as DEFAULT, COMMON, or
                 UNUSUAL in a real deployment. Any UNUSUAL precondition caps
                 severity and must be stated.

Rules:
- Assume the claim is WRONG until the evidence forces you to conclude otherwise.
- A plausible-sounding mechanism is not evidence. Only quoted code, real
  responses, and named call chains are evidence.
- You are rewarded for correctly killing a bad claim, not for confirming.
- Never fill a gap with "likely", "presumably", "an attacker could probably".
  Those words mean VERDICT=UNPROVEN.

Output exactly:
VERDICT: CONFIRMED | UNPROVEN | FALSE | NO_IMPACT
EVIDENCE: <quoted code / raw responses / named chain>
KILL_REASON: <if not CONFIRMED, the specific thing that fails>
SEVERITY_CAP: <if CONFIRMED, max defensible severity and why>
```

**Why it works:** "disprove" inverts the model's agreeableness. Withholding the
hunter's reasoning prevents error inheritance. Forcing `STOP at first failure`
prevents the model from rationalizing past a dead gate. Banning hedge words
closes the gap models use to smuggle in unproven steps.

---

## 5.5 Deterministic validators beat LLM validators

For each class, build a non-AI oracle. A script cannot hallucinate. Invest here
before you invest in better prompts.

| Class | Deterministic oracle |
|---|---|
| IDOR / BOLA | Two owned accounts. Request B's object with A's token. Oracle: HTTP 200 **and** response body contains B's canary string. |
| Authz / BFLA | Same request as low-priv and as high-priv. Oracle: status/body diff is empty when it should differ. |
| SSRF | Target fetches your unique OOB hostname. Oracle: your DNS/HTTP log records the hit with the matching nonce. Binary, no judgment. |
| Reflected XSS | Headless browser loads the URL. Oracle: a JS callback actually fired (not "the string appears in the response"). |
| SQLi | Boolean/time oracle on a value only the DB knows, in a test record you created. |
| Cache poisoning | Second, clean client fetches the resource. Oracle: clean client receives your marker. |
| Secret leak | Validate the credential against the vendor's own token-introspection endpoint. Oracle: "active/valid". Never use the credential for anything else. |
| Subdomain takeover | Oracle: you serve a unique nonce on the dangling host and fetch it back over the victim hostname. |
| Race condition | N parallel attempts. Oracle: final state is arithmetically impossible under correct locking (e.g. balance > sum of deposits). |
| Path traversal | Oracle: response contains content from a file your test account provably does not own. |

### Make the oracle expectation-free

The sharpest oracle-design idea from 2026 research, and the one worth generalizing:

> *"This system has no expectations about what the poisoned response should look like,
> which means it can detect **any kind** of cross-request contamination."*
> — HTTP Terminator

**Assert that a boundary was crossed, not that the response contains a particular
string.** An oracle that checks `response contains "<marker>"` finds only what you
predicted. An oracle that checks *"this response belongs to a different request than the
one I sent"* finds classes you never hypothesized.

Applied to the table above: for IDOR, assert *"the body contains data not owned by this
token"* rather than matching one canary field. For cache poisoning, assert *"a clean
client received content it should never see"* rather than matching your specific marker.
For races, assert *"the final state is arithmetically impossible"* rather than counting
successes.

This is described as *"the single most transferable AI-era design pattern"* — because it
is the one oracle shape that detects bugs the hypothesis-generator didn't imagine.

### When a class has no deterministic oracle: the ensemble rung

Between "one model's judgment" and "a human reads it" there is a middle rung that is still
not an LLM vote **[S]**:

Research on classifying vulnerable functions found **a single base LLM scores roughly
50–56% — near coin-flip.** Adding richer context (callers, callees, location, code
patterns), fine-tuning, **multiple different prompt views of the same question**, and then a
**traditional ML meta-classifier over the ensemble's agreement/disagreement plus metadata**
reached **~76.9%**.

Two things to take from that:

1. **The 50–56% figure is the sharpest available argument for this document's central
   rule.** A single model asked "is this a vulnerability?" is barely better than chance — so
   never let the component that proposes a finding also confirm it, and never treat one
   model's confidence as evidence.
2. **The decision rule over N views can itself be deterministic.** Run the same question as
   several genuinely different prompts, then apply a *fixed rule* to the spread — e.g. unanimous
   confirm required, or any dissent forces `UNPROVEN`. The arbiter is code, so it cannot
   hallucinate, even though its inputs are model outputs.

Also from the same work: **feed call-graph context, not isolated functions.** An isolated
function is the condition under which models perform worst.

**Rule:** if a class has no deterministic oracle, use the ensemble rung, give it stronger
human review before submit, and say **"manually verified"** rather than "validated" —
the words should not overclaim the method.

---

## 5.6 The negative ledger

Most harnesses throw away rejections. That's the most valuable data you have.

Every killed candidate gets appended to `findings/rejected.jsonl`:

```json
{
  "date": "2026-10-02",
  "target": "api.example.com",
  "class": "idor",
  "location": "GET /v2/invoices/{id}",
  "verdict": "NO_IMPACT",
  "kill_reason": "Returns only the requesting tenant's rows; {id} is validated against session tenant at middleware/tenant.go:88",
  "gate_failed": 3,
  "cost_usd": 0.42
}
```

What this buys you:

- **No re-litigation.** Load the ledger into the hunter's context so it stops
  re-proposing the same dead idea every run. This alone cuts cost substantially
  across repeated campaigns.
- **Hardened-area map.** Many rejections clustered in one component means the
  team defends it well — go elsewhere. Clustered rejections are a *negative*
  signal about that surface and a positive signal about the rest.
- **Calibration.** Track which gate kills most of your candidates. Gate 1 heavy
  means your hunter hallucinates — give it less context and more grounding.
  Gate 2 heavy means it doesn't understand the architecture — feed it the call
  graph. Gate 3 heavy means it doesn't understand the threat model — give it the
  program's accepted-risk list.
- **ROI.** `cost_usd` summed against bounties earned tells you whether a campaign
  shape is actually profitable. Technical success at negative ROI is failure.

---

## 5.7 The coverage ledger (the positive twin)

The negative ledger tracks what you killed. The coverage ledger tracks what you
*looked at*, so repeated runs are additive instead of random.

```markdown
| Component | Surface | Hunted | Classes covered | Verdict | Run |
|---|---|---|---|---|---|
| auth/session.go | cookie issuance | 2026-09-28 | fixation, scope, flags | clean | r1 |
| api/invoices | REST CRUD | 2026-09-29 | idor, bfla, mass-assign | 1 confirmed | r1 |
| api/exports | PDF render | — | — | NOT YET | — |
| graphql/schema | mutations | 2026-10-01 | field-authz | 2 unproven | r2 |
```

Without this, run 2 re-covers run 1's ground and never reaches the export
endpoint — which, per [06 — Target Selection](./06-target-selection.md), is
exactly where the under-tested bugs live. The ledger is what converts many cheap
runs into real coverage.

---

## 5.8 Enforcing gates mechanically, not by prompting

A prompt is a request; a hook is a control. Put the gates where the model cannot
talk its way past them.

- **`PreToolUse` hook** on network tools: hard-deny any host not in
  `scope/allowlist.txt`. Exit non-zero to block. This is your Gate 0 and the only
  reliable one.
- **Structured output schema** for findings: a candidate with empty `evidence` or
  missing `call_chain` is rejected by a validator script before it reaches you.
- **Separate subagent** for validation, so fresh context is structural rather
  than something you remembered to do.
- **`Stop` hook** that refuses to end a hunt run if `findings/confirmed.jsonl`
  contains an entry whose `gate_6_human_reviewed` is false — so nothing reaches a
  submission draft unreviewed.

See [04 — Harness Architecture](./04-harness-architecture.md) for the wiring.

---

## 5.8b The schema is the gate

Doctrine that lives only in a prompt is a request. This repo ships the contract as code:

- **`schema/finding.schema.md`** — the three-verdict record shape, with distinct required
  *and forbidden* fields per verdict. The load-bearing property: a `needs_validation`
  record **cannot** carry a severity, so a speculative lead can't be laundered into a
  finding by attaching a number to it.
- **`scripts/validate-findings.py`** — stdlib-only validator. Closed field set, trace
  integrity (first hop `entrypoint`, last `sink`), fingerprint stability, `gate_failed`
  on rejections, and it **rejects hedged impact sentences** on confirmed records.
- **`scripts/stop-gate.py`** — a `Stop` hook refusing to end a session on malformed
  findings, or when a report draft exists for a finding no human has reviewed.

```bash
python3 scripts/validate-findings.py     # validate findings/*.jsonl
bash scripts/test-all.sh                 # whole harness, including hook tests
```

## 5.9 Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| "Check if this is exploitable" | Agreeable framing. Use "disprove". |
| Validator in the same context as hunter | Inherits the hunter's errors and sunk-cost reasoning. |
| LLM as the only oracle | Hallucinates confirmation. Add a deterministic check. |
| Pattern match = finding | Grep hits are candidates, never findings. |
| "Likely exploitable" in a report | Unproven. Triage reads this as "didn't verify". |
| Severity from class, not impact | A "critical" SSRF to a closed internal port is low. Impact sets severity. |
| Submitting the raw scanner report | Low effort, instant signal damage. |
| Discarding rejections | Throws away your cheapest future speedup. |
| Automated submission | Bans accounts; poisons the well for everyone. |

---

## 5.10 The one-page checklist

Print this. A finding ships only when every box is checked.

```
[ ] GN Crowding scored BEFORE proof effort (docs/11) — not obvious, not scanner-findable
[ ] G0 Asset in scope; technique permitted; rate limits respected
[ ] G1 Cited location verified by independent read — snippet quoted
[ ] G2 Unbroken call chain from public entrypoint; every guard accounted for
[ ] G3 Impact sentence written: "An attacker with X can VERB ASSET of VICTIM"
[ ] G4 Reproduced twice on authorized target, two owned accounts, minimum data
[ ] G5 Checked against public disclosures / CVEs / program changelog
[ ] G6 I read this myself and would defend it to the author
[ ] G7 Cascaded: variants searched, escalation attempted before reporting
[ ] G8 Queued for regression retest once resolved (the loop closes, ~3-8% regress)
[ ] Evidence redacted; no third-party PII
[ ] Severity justified by impact, not by class name
[ ] Preconditions stated honestly, including the inconvenient ones
[ ] Cleanup done; test artifacts listed
```

---

**Next:** [04 — Harness Architecture](./04-harness-architecture.md) ·
[07 — Reporting](./07-reporting-that-gets-paid.md) ·
[06 — Target Selection](./06-target-selection.md)
