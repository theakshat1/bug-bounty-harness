# 07 — Reporting That Gets Paid

> The market stopped paying for *finding* and started paying for *proving*. Your
> report is the proof. Triage will spend ~5 minutes deciding whether it's real,
> and their default is to close as informative.

---

## 7.1 The convergent requirement set

HackerOne, GitHub, Bugcrowd, Intigriti and GitLab independently landed on the same
core. All five, verified:

1. **Working, reproducible PoC.** GitHub: *"Show us the impact, don't just describe
   it. What could an attacker actually achieve?"*
2. **Complete attack chain, all steps connected.** HackerOne's Code of Conduct is
   explicit: *"connect all steps in an attack chain."* **Partial chains are the
   most common AI-report failure.**
3. **Demonstrated impact, not asserted impact.** Shopify's internal bar: business
   impact **beyond a boolean flag**.
4. **Human validation before submission**, regardless of tooling.
5. **Correct severity at submission** — mandatory on HackerOne since 2026-09-21,
   and triage *routes* on it, so mis-severity actively costs you queue position.
6. **Scope awareness.** GitHub names unreviewed scope as a top waste category.
7. **Environment-specific reproduction steps.** Intigriti pushes **short video**.
8. **Verifiable artifacts.** GitLab closes reports lacking them as N/A.

---

## 7.2 The structure

```markdown
## Summary
<One or two sentences. What boundary breaks, who is affected, what the attacker
gains. Concrete nouns. Never the class name as the impact.>

## Impact
An attacker with <access level> can <verb> <asset> belonging to <victim>.

<2-4 sentences on realistic consequence: how many users, what data, read or write,
whether interaction is needed. Specific and honest — understating slightly reads
as credible; overstating reads as noise.>

## Affected asset
- Endpoint/host: <exact>
- Component/version: <exact, if known>
- Discovered / Verified: <dates>

## Preconditions
- <precondition> — DEFAULT / COMMON / UNUSUAL

## Steps to reproduce
1. <Numbered, minimal, deterministic. Name the account used at each step.>

Account A (attacker): acct-a@...
Account B (victim):   acct-b@... containing canary `CANARY-B-7f3a`

## Evidence
<Minimum necessary request/response pairs. Tokens and third-party PII redacted.
"Unredacted copy available to triage on request.">

## Why this is a security issue
<Short. Name the control that should have existed and the layer where it's
missing. This is what distinguishes a researcher from a scanner.>

## Severity
<Proposed + CVSS vector if the program uses it.>
Justification: <tie to impact, not class. State what caps it.>

## Suggested remediation
<2-3 concrete sentences. Name the check and where it belongs.>

## Scope and conduct
- Assets touched: <in-scope only>
- Accounts used: <so the program can remove them>
- Data accessed: <exactly what, and how little>
- Cleanup: <artifacts removed or listed>
- Rate: <within program limits>
```

**The single highest-value sentence is the first one.** Lead with the boundary that
breaks, not the class name.

---

## 7.3 Severity honesty

- Severity comes from **demonstrated impact**, never from the class name. An SSRF
  reaching nothing internal is Low. An IDOR on public data is Informational.
- **The high/medium discriminator:** does the result *fully defeat* an explicit
  control for an action with real consequences, or only weaken it?
- **"If you cannot state the concrete damage, the severity is lower than it feels."**
- If authentication is required, say so. If user interaction is required, say so.
  If it needs a non-default configuration, say so and cap severity.
- Never submit a Critical you cannot defend line by line.

> One inflated severity costs more credibility than three correctly-rated Mediums
> earn. And since triage now routes on your stated severity, inflation actively
> delays your own report.

---

## 7.4 State preconditions you'd rather hide

An unstated precondition that triage discovers reads as **deception**, and sinks
otherwise-good reports. Mark each DEFAULT / COMMON / UNUSUAL and list all of them,
including:

- requires authentication (and at what privilege)
- requires victim interaction (a click, a visit)
- requires a non-default setting
- works only on a specific version or region
- probabilistic (races, injection) — **state the success rate across ≥5–10 runs**

Honesty here is not modesty; it is the thing that makes the rest of your report
believable.

---

## 7.5 Evidence hygiene

**Do:**
- Minimum request/response pair that shows the boundary failing
- Your own canary strings so screenshots are unambiguous and harmless
- Redact tokens, cookies, third-party PII; note you hold the unredacted copy
- Timestamp your testing window so triage can correlate logs
- State explicitly what you did *not* do ("I did not enumerate further records")

**Don't:**
- Paste third-party PII
- Paste raw scanner output as "evidence" — it's noise and signals low effort
- Host a loud public PoC. For takeover-style proofs: minimal public artifact
  (blank page, proof in an HTML comment), verification instructions in the private
  report. A flashy public PoC panics real customers and can turn a payout into a
  policy violation.
- Leave PoC infrastructure running after resolution

---

## 7.6 Make the defender able to execute your proof

The highest-leverage move available, and it's the convergent conclusion of
Shopify's test oracle, Immunefi's runnable-PoC rule, and AXE's reproducible
artifacts:

> **If you can submit evidence in a form the defender can execute, you have
> converted an argument into a fact.**

Concretely, in descending order of power:
1. An **integration test** against untouched source that fails before the fix and
   passes after (for source-available targets)
2. A **runnable script** that demonstrates the effect against a test account
3. A **single curl/HTTP pair** a triager can paste
4. A **short video** of the reproduction (what Intigriti explicitly asks for)
5. Prose steps

A proof that runs cannot be hallucinated, and it collapses triage cost to near
zero. Expect this to become an explicit requirement rather than a differentiator.

---

## 7.7 Handle duplicates and known issues up front

If this is the same class on a sibling endpoint, or a bypass of a shipped fix,
**say so in the summary and link the original.**

- It pre-empts the duplicate close.
- Regression bypasses are **often paid in full**.
- It reads as competence, not weakness.

Before submitting, check: program public disclosures, the changelog, CVE/advisory
feeds for the component and version, and your own prior reports (the HackerOne MCP
is read-only and good for this).

Beware the failure mode the academic literature names **"semantically repackaged
bug reports"** — paraphrased duplicates that evade string-match dedup. If your
harness emits these you will look like a farmer even when your bug is real.

---

## 7.8 Identity and history are now part of your evidence

- **IDV is mandatory** on HackerOne Bug Bounty submissions (Aug 2026) and Bugcrowd
  Managed Bug Bounty (May 2026).
- **TriageOne routes on researcher history**, explicitly separating an experienced
  researcher from "a newly created account backed solely by automated tooling."
- **GitHub gates its public program on signal**, with ~4 submissions of runway for
  new researchers.
- HackerOne's penalty ladder puts **loss of private program eligibility** above
  rate limiting.

> A clean account with real signal is a reusable asset: it buys queue priority,
> private invitations, and the benefit of the doubt. Spending it on speculative
> volume is now straightforwardly irrational — the penalty ladders are designed to
> make volume cost more than it earns.

---

## 7.9 AI disclosure

- **Only Intigriti, Django and FFmpeg require you to disclose AI use** (of 53
  programs surveyed). Where required, non-disclosure is a policy violation
  independent of whether the bug is real.
- Everywhere else the requirement is **accountability, not disclosure**: HackerOne
  puts it as *"Community Members remain fully responsible for any submissions
  created with the assistance of AI tools."*
- **Never claim you manually verified something you didn't.** That is the one lie
  that ends a career in this field.

---

## 7.10 Final checklist

```
[ ] First sentence states impact, not class
[ ] Impact sentence has concrete nouns: who, what verb, whose asset
[ ] A stranger could reproduce from the steps alone, first try
[ ] Every precondition stated, including the unflattering ones
[ ] Severity defensible line by line; capped where it should be
[ ] Probabilistic findings state a success rate
[ ] Evidence minimal, redacted, no third-party PII, no raw scanner output
[ ] Duplicate/known-issue status addressed up front, original linked
[ ] Test accounts documented so the program can remove them
[ ] Cleanup done and described
[ ] Program's accepted-risk list checked
[ ] AI disclosure included if this program requires it
[ ] I verified this myself and would defend it to the engineer who wrote the code
```

---

**Next:** [05 — Validation Gates](./05-validation-gates.md) ·
[09 — Scope and Ethics](./09-scope-authorization-and-ethics.md) ·
[06 — Target Selection](./06-target-selection.md)
