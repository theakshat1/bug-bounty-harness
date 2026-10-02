# 06 — Target Selection (where the money actually is)

> Target selection is now worth more than technique. The same skill applied to a
> saturated surface earns nothing; applied to an under-tested one it earns real
> money. This is the highest-leverage decision you make, and you make it before
> you send a single request.

---

## 6.1 The rule that follows from the 2026 data

From [01 — Landscape](./01-landscape-2026.md), two verified facts set your strategy:

1. **78% of *valid* hackbot findings were XSS.** XBOW topped HackerOne's US
   leaderboard on reputation while earning **under $40,000 total since Feb 2024**.
2. **"70% of critical web vulnerabilities are business logic flaws — no autonomous
   agent reliably detects these."**

> **Do not compete with agents on their strongest class.** Hunt where
> confirmation requires knowing what the application is *supposed* to do, because
> that intent is not in the code, and therefore not in any model's context.

This also makes your findings **duplicate-resistant**. Two scanners find the same
reflected XSS; two researchers rarely construct the same unintended workflow.

---

## 6.2 The payout tiers

### Tier 1 — where the money concentrates (hunt here)
Named explicitly by HackerOne as where "the human edge holds":

| Class | Why it survives automation |
|---|---|
| **Business logic flaws** | Requires knowing intended behavior. Unscannable. Reported ranges: Shopify $25K–$150K (checkout price manipulation), GitLab $20K–$80K (authorization workflow bypass), Uber $10K–$50K (pricing logic), DeFi $50K–$500K. |
| **Broken access control / privilege escalation** | The check that *should* exist isn't in the code to be found. You have to know the role model. |
| **Authentication implementation errors** | Protocol-level reasoning across multiple requests and parties. |
| **MCP OAuth account takeover** | New surface, few testers, real impact. Corroborated as paying by two independent sources. |
| **Agent authorization confusion** | Ditto. The newest well-paid class in the market. |
| **Race conditions / TOCTOU** | Needs multi-request orchestration and an invariant argument. Canonical: H1 #1717650 (Stripe) — `max_redemptions=1` redeemed 30× in parallel, ~$600K in fee-free transactions. |
| **Compositional / multi-commit risk** | **Structurally invisible to the prevailing agent architecture.** HackerOne's own critical RCE (found by Mythos 5) came from *three individually safe commits by different authors over time*. Agents partition repos by file; neither single-diff review nor SAST sees this. |

### Tier 2 — still pays, needs real impact
Cache poisoning/deception, SSRF chained to something internal, request smuggling
(see §6.4 — this re-opened in 2026), subdomain takeover with real context,
GraphQL field-level authz, CI/CD and OIDC misconfiguration, secrets with verified
validity.

### Tier 3 — avoid unless chained
Reflected XSS, missing headers, SPF/DMARC, self-XSS, clickjacking on
non-sensitive pages, rate-limit absence with no demonstrated impact, scanner
output. **These are what the agents flood. You will be duplicate #40.**

---

## 6.3 Under-tested surfaces (the practical heuristic)

Within any target, testers cluster on login, registration, and password reset.
Score **up**:

- **Export / PDF / render / template** endpoints → SSRF, SSTI
- **File upload, preview, thumbnail, parsing** → traversal, SSRF, parser bugs
- **Email / notification / digest generation** → IDOR on recipient IDs, injection
- **Webhooks** and anything making an outbound request on user input → SSRF
- **Batch/bulk variants** of single-item endpoints → inherited-but-broken validation
- **Shadow / zombie API versions** — the highest-yield single item on this list.
  `/api/v2/users/{id}` ships the new ACL; **`/api/v1/users/{id}` still exists with
  the old or no check.** Enumerate `v1…vN`, `/internal/`, `/admin/`, `/beta/`,
  `/legacy/`, `/_internal/`, `/api/private/`. Deprecated endpoints frequently have
  *weaker auth*, not just older features.
- **Anything reachable only via API, never the UI** — the UI's allowlist is the
  only one most testers check
- **Recently shipped features** (read the changelog / release notes)
- **Exposed Apollo Federation subgraphs** — the router enforces JWT validation,
  cost limits and safelisting; the subgraph enforces nothing. Find the subgraph
  directly and you bypass every control at once.

Score **down**: login, registration, password reset, and anything with an existing
public disclosure against it.

### The recon artifacts that reveal them
- **JS bundles and source maps.** Exposed `.js.map` on production builds remains
  common and hands you the entire client codebase — route tables, API base URLs,
  hidden admin paths, feature flags, internal comments. Workflow:
  katana → collect JS → check for `.map` siblings → MapperPlus → jsluice + TruffleHog.
- **Mobile apps.** `strings`/`jadx` on an APK regularly yields endpoints and
  GraphQL operation names unreachable from web.
- **Public Postman workspaces, `openapi.json`, `/.well-known/`.** Then hunt the
  **drift**: endpoints in the spec that aren't publicly documented, and endpoints
  live in the API that the spec omits. Drift is where the missing guard lives.
- **Staging/dev subdomains** with introspection or debug enabled — grab the schema
  there, use it against prod.

---

## 6.4 What's newly open in 2026

Two developments genuinely re-opened closed doors:

### Desync is not dead — it was under-explored
**HTTP Terminator** (James Kettle, Black Hat USA 2026,
https://portswigger.net/research/http-terminator): an AI-assisted research system
explored ~30,000 candidate desync vectors against 30,000 authorized sites and
found **~700 vulnerable targets** — including banks, government infrastructure,
security products, and an airport. **Source and a reusable blueprint are published.**

New triggers worth testing: `Content-Type: multipart/byteranges` (CL.0 desync,
hit 200+ sites), `Transfer-Encoding: gzip` with HTTP/1.0, dual matching
`Content-Length` headers, CONNECT variations over HTTP/2, and the "dangling byte"
technique that makes response-queue poisoning far more reliable.

The generalizable concept — **Shared-Parser Confusion**: response-processing rules
misapplied to requests wherever parsing code is shared. Use it as a hypothesis
generator.

### The 2025 Top 10 (published Feb 2026) is a map of live seams
https://portswigger.net/research/top-10-web-hacking-techniques-of-2025

| # | Technique | Where to look |
|---|---|---|
| 1 | **Successful Errors: Code Injection & SSTI** | Any template render point. Verbose engine errors become an oracle — apply full SQLi methodology (error → boolean-blind → time) to SSTI. |
| 2 | **ORM Leaking** ([elttam](https://www.elttam.com/blog/leaking-more-than-you-joined-for/)) | **Highest-signal new class for API hunters.** Filter/search/sort APIs over an ORM. User-controlled filter expressions reach fields the API never meant to expose (`password`, `api_key`, `reset_token`). Comparison operators turn it into server-side binary-search exfiltration. |
| 3 | **SSRF via HTTP redirect loops** | Different redirect-depth counts produce distinguishable error states — **turns unreportable blind SSRF into readable impact.** |
| 4 | **Unicode normalization** | Any check that runs *before* normalization: overlong encodings, byte truncation, confusables, casing (dotless ı → I), combining diacritics. |
| 5 | **SOAPwn** (.NET HTTP client proxies) | URI-type confusion where scheme isn't filtered before casting. |
| 6 | **Cross-site ETag length leak** | ETags encoding response size, reflected into `If-None-Match`. |
| 7 | **Next.js cache chains** | `__nextDataReq` / `x-now-route-matches` change response *format* without being part of the cache key → internal cache poisoning. |
| 8 | **XS-Leak via cross-origin redirects** | Chrome connection-pool exhaustion + lexicographic host priority → timing oracle to binary-search a redirect target (tenant name, role). |
| 9 | **HTTP/2 CONNECT** | 200 vs 503 distinction = free internal port-scan primitive. **Cheap to check.** |
| 10 | **Parser differentials** | Duplicate JSON keys (Erlang takes first, JS takes last), duplicate headers, YAML/JSON mismatch. Classic shape: **auth layer validates one copy, app reads the other.** |

> **The common thread: every single entry exploits disagreement between
> subsystems about parsing, caching, or normalizing.** That is the hunting
> heuristic for 2026. Kettle's own framing of 2025 was "the rise of side-channels
> as a core exploitation primitive."

Note also: Top-10 nominations **dropped to 63 from 121** — community attention
moved to AI. Fewer eyes on classical web research is an opportunity.

---

## 6.5 AI/LLM application surfaces — new money, narrow rules

AI features are in scope on **1,100+ HackerOne programs (270% YoY increase)**.
Prompt injection is the fastest-growing finding category *and* the most-rejected.

### The rule that determines whether you get paid
> **Reframe the finding as a classical bug class.** Prompt injection is a
> *delivery mechanism*, not the vulnerability. Report it as SSRF, authorization
> violation, or cross-tenant data disclosure, with injection as the entry vector.
>
> "AI jailbreak" gets closed. "Unauthenticated SSRF via document-processing
> pipeline" gets paid.

**What pays** (highest first): agent tool abuse reaching infrastructure (the LLM
controls a tool that makes HTTP requests, runs code, reads files → SSRF to
metadata, sandbox RCE); cross-tenant/cross-user exfiltration; indirect prompt
injection via a channel the victim trusts (email the agent reads, a document it
processes, a repo it indexes — Google pays premium here, $15K+ observed for
indirect chains achieving ATO); system-prompt extraction **that reveals secrets**;
cross-session memory leakage; **LLM-app IDOR** (conversation histories, uploaded
files, vector-store namespaces — often a plain BOLA in the app's API, which is the
easier and more reliable bug than anything model-level); **RAG data leakage** where
retrieval ignores per-document ACLs.

**What gets rejected near-universally:** direct jailbreaks with no onward impact,
single-context injection, hallucinations without attacker control, content-policy
violations. **Google's AI VRP explicitly excludes prompt injection, jailbreaks and
alignment as a category.** **OpenAI treats base-model prompt injection as a "known
limitation"** — payable only when chained to exfiltration, privilege escalation, or
cross-user effect.

| Program | Realistic median | Top |
|---|---|---|
| Anthropic (H1, public since May 2026) | $1.5K–5K | stated max $15K |
| OpenAI (Bugcrowd) | $500–3K | $20K std, $100K exceptional |
| Google AI VRP | $500–3K | $20K base / $30K with bonuses |
| Microsoft Copilot | — | $250–$30K |
| H1 long tail | $100–2K | program-dependent |

> ⚠️ **Agent tool scope is the #1 policy ambiguity of 2026.** Programs often fail
> to say whether coercing a `send_email` tool to an attacker address is in-bounds.
> **If the policy doesn't enumerate in-scope tools, ask before testing**, and never
> trigger a destructive tool action outside a named test tenant with explicit safe
> harbor. The most common wasted report of 2026 is a prompt-injection finding sent
> to a program that explicitly excludes them.

---

## 6.6 Program selection

### Verified signals
- **GitHub's VIP ladder** is the clearest published path to premium rates:
  **1 critical, OR 2 highs, OR 4 mediums, OR 7 lows** → VIP, where Critical goes
  from $10K to $30K+. A concrete, achievable target.
- **Intigriti explicitly architects two tiers**: *volume reporting programs* (lower
  pay, automation-tolerant) vs *expert programs* (higher pay, low volume,
  collaborative). Know which you're in.
- **HackerOne's penalty ladder puts "loss of private program eligibility" above
  rate limiting.** Platforms now treat private-program access as the primary
  economic reward for signal quality.

> **Reputation stopped being cosmetic. It is the gate on the only tier where
> payouts held up.** Burning it on speculative volume is straightforwardly
> irrational — the penalty ladders are built to make volume cost more than it earns.

### Unverified folklore (test it, don't trust it)
These circulate widely with **no primary data** behind them. Flagged honestly:
- "Private programs pay 20–40% more" — plausible (GitHub's VIP tier is a verified
  2–3× premium) but the specific percentage is unsourced.
- "Hall-of-Fame size as saturation proxy: 200+ names = saturated, 10–50 = room."
- "YesWeHack / Bugcrowd less crowded than HackerOne."
- "Fintech criticals $15K–50K; crypto $20K–100K" — the crypto range is
  directionally consistent with Immunefi's published maximums.

### Practical program-selection checklist
- [ ] Read the **accepted-risk / out-of-scope** list *first* — it tells you what
      not to waste a week on
- [ ] Check the **AI policy** (only Intigriti, Django and FFmpeg require
      disclosure, but 13 of 16 AI-addressing programs require human verification)
- [ ] Check response SLA and recent activity — a program that doesn't triage is a
      program that doesn't pay
- [ ] Prefer scopes with **API surface, multi-tenancy, and a role model** — that's
      where Tier 1 classes live
- [ ] Prefer programs whose scope recently **expanded** (newly added assets have
      had fewer eyes)
- [ ] Note whether the **GitHub org / CI-CD is in scope** — it usually isn't, and
      testing it anyway is a policy violation

---

## 6.7 Regression: the highest-ROI surface of all

Resolved reports are your best lead source, and almost nobody works them:

- A **fix is new code** written under time pressure, often by someone who didn't
  write the original.
- You already have the **full context** of how the bug worked.
- **A fix on one backend is not a fix if siblings remain.** The same class on a
  sibling endpoint, a different API version, or a parallel service is extremely
  common.
- Bypasses of shipped fixes are **often paid in full**, and they are
  duplicate-resistant because they require the original context.

Queue **every** resolved report for a regression retest. Use the HackerOne MCP
(read-only) to pull your own and the program's public disclosures. Say up front in
the report that it's a bypass of a known issue, and link the original — it
pre-empts the duplicate close and reads as competence.

→ See the `regression-sweep` skill.

---

## 6.8 The automation meta-point

> Hunters consistently landing P1/P2 on competitive targets are **not** running
> broader automation — they're running **narrower** automation against **more
> carefully selected** attack surface, combined with manual analysis that generic
> pipelines skip. Fewer tools, right sequence, better notes, better validation.
>
> A big stack gives you the illusion of coverage without understanding.

This is the same finding as the focused-vs-broad prompt result in
[03 §3.5](./03-skills-and-plugins.md) and the partitioning result in
[04 — Harness Architecture](./04-harness-architecture.md). Three independent
sources, one conclusion: **narrow and deliberate beats broad and automated.**

---

**Next:** [08 — Vuln Class Playbooks](./08-vuln-class-playbooks.md) ·
[05 — Validation Gates](./05-validation-gates.md) ·
[07 — Reporting](./07-reporting-that-gets-paid.md)
