# 08 — Vulnerability Class Playbooks

> **Methodology only** — where to look, why it breaks, what evidence proves it.
> No payloads. Authorized, in-scope testing assumed throughout.
>
> Ordered by **what currently pays**, not by textbook convention. The crowded
> classes are at the bottom for a reason.

---

## 8.1 Business logic & race conditions — top of the payout table

**Why it pays:** unscannable. Requires knowing what the app is *supposed* to do,
and that intent isn't in the code. Also duplicate-resistant — two researchers
rarely construct the same unintended workflow.

Reported ranges: Shopify $25K–$150K (checkout price manipulation), GitLab
$20K–$80K (authorization workflow bypass), Uber $10K–$50K (pricing logic), DeFi
$50K–$500K. Canonical race: **H1 #1717650 (Stripe)** — a `max_redemptions=1` promo
code redeemed 30× in parallel, ~$600K in fee-free transactions.

### Finding candidates
**Heuristic: anything with a limit is a race target.** Map state-altering verbs
(POST/PUT/PATCH/DELETE) whose names contain *redeem, transfer, apply, activate,
claim, vote, follow, invite, purchase, upgrade, withdraw, cancel, refund*.

Then: **call it twice.** If the second call errors, there's a check-then-act window.
Always establish a single-request baseline first and document what changed.

### The enabling concept: the single-packet attack
Multiplex N requests over one HTTP/2 connection, withhold each request's final
bytes, then release them all in **one TCP packet** — eliminating network jitter so
all N arrive at the server's HTTP/2 layer effectively simultaneously. This is what
turned races from "sometimes works" into reliable.

Tooling:
- **Burp Turbo Intruder** — `concurrentConnections=1` with the HTTP/2 engine
- **Caido v0.58.0** (2026-08-24) — **Replay Pipeline with "Last Byte
  Synchronization"**, built for exactly this. HTTP/2 is beta/opt-in — enable it,
  because forcing HTTP/1.1 changes the protocol under test.

### Five race patterns
1. **Limit overrun** — N successes where 1 should occur (coupons, trials, invites, votes)
2. **Double-spend** — concurrent balance deductions exceeding funds
3. **Privilege escalation** — a permission check racing a permission modification
4. **Multi-endpoint races** — two endpoints mutating shared state with no unified
   lock. Hardest to find, **often highest paid.**
5. **Validation-to-processing windows** — upload/scan/convert pipelines where the
   file is readable between validation and rewrite

### Non-race business logic
- **Step skipping** — jump to the final step of checkout/KYC/onboarding/reset
- **Object masking** — act on an object while it exists but isn't fully
  initialized; defaults may be permissive, owner may be unset
- **Sub-states** — a user briefly both "unverified" and "has a session"
- Currency/rounding/negative quantities; discount applied after total; cancel-and-refund ordering

### What makes a race *reliable* (not just firable)
Tooling tells you how to fire a race; it doesn't tell you why one lands. Three mechanics,
from kernel race research: **widen the window** (make the contended operation slower),
**restructure toward cheaper error paths** (a request that short-circuits returns faster and
tightens the collision), and **isolate contending locks** so your two operations don't
serialize on something unrelated. **[S]**

This matters for reporting, not just exploitation: B's own standard is to state a success
rate over ≥5–10 runs, and these three levers are what move that number from 1-in-50 to
near-deterministic — which is the difference between a believable report and an
"intermittent, could not reproduce" close.

### Evidence that gets a race report paid
Triagers need business impact, not speed:
(a) precondition state, (b) **all** request/response pairs with success codes,
(c) post-race application state proving the invariant broke, (d) **success rate
across ≥5–10 runs** (races are probabilistic — say so), (e) quantified impact.

Also name the defense that was absent — `SELECT … FOR UPDATE`, a unique
constraint, an idempotency key, a distributed lock. It makes the report actionable
and signals competence.

---

## 8.2 Authorization: BOLA / BFLA / BOPLA

Still the most productive API family, and the one agents are worst at.

- **BOLA (API1).** Two accounts, swap object identifiers **everywhere** — not just
  the obvious path param, but nested bodies, arrays, and secondary identifiers.
  Watch for UUIDs that are guessable or leaked elsewhere (search results,
  notification emails, public profiles). **"Unguessable ID" is not authorization.**
- **BOPLA (API3).** The API authorizes the *object* but not its *properties*. Two
  directions: **read side** — the response contains fields the UI never renders
  (diff API response vs rendered UI); **write side** — mass assignment of `role`,
  `isAdmin`, `isVerified`, `tenantId`, `balance`, internal flags. Harvest candidate
  field names from the object's own GET response, the GraphQL schema, or JS bundles.
- **BFLA (API5).** Enumerate **every route × every method × every role**. Specific
  wins: methods the router doesn't handle but the framework allows (`PATCH` where
  only `GET`/`PUT` are documented); method-override headers; admin routes reachable
  with a user token because the guard is on the UI, not the API.
- **Shadow / zombie API versions — the highest-yield item here.** `/api/v2/users/{id}`
  ships the new ACL; **`/api/v1/users/{id}` still exists with the old or no check.**
  Enumerate `v1…vN`, `/internal/`, `/admin/`, `/beta/`, `/legacy/`, `/_internal/`,
  `/api/private/`. Deprecated endpoints frequently have *weaker auth*, not just
  older features.
- **Documentation-vs-reality drift.** Pull `openapi.json`, `/.well-known/`, public
  Postman workspaces, GraphQL schemas. Then hunt both directions: spec endpoints
  that aren't publicly documented, and live endpoints the spec omits (find them in
  JS bundles and mobile apps). **Drift is where the missing guard lives.**
- **Rate-limit bypass** — per-request limiters vs batching; limiter keyed on IP
  (rotate), on a client-set header, or on the account but not the
  email/phone being targeted; limits on `/v2` but not `/v1`.

### Batch and bulk endpoints — six concrete shapes
"Batch variants inherit broken validation" is the usual one-liner. The mechanisms, from
research into a WordPress RCE, are more specific and each is independently testable **[S]**:

1. **Validate/execute index desync.** The API validates in one loop and executes in
   another. When an error path pushes to only one of two parallel arrays, the arrays
   desync and a rejected item's *slot* gets filled by its neighbour. Test: submit a mix of
   valid and invalid items; correlate the validated set against the executed set **by index**.
2. **Scalar/array type asymmetry.** A sink sanitizes arrays but passes scalars through
   unsanitized (or the reverse). Test every sanitized parameter as both.
3. **Self-nesting.** Does the batch endpoint accept **itself** as one of its items? Inner
   calls inherit the outer call's already-passed validation.
4. **Cache-vs-DB reconciliation as an escalation gadget.** After any read primitive,
   in-memory object caches plus a feature that reconciles cache against DB can be driven to
   promote attacker-influenced state.
5. **Identity-switch records.** Anywhere the app temporarily assumes another identity
   (impersonate, run-as, cron-as-owner, webhook-as-installer, support-view): is the
   structured record driving that switch attacker-influenced?
6. **Dynamically named hooks/actions.** Handler, event or permission names assembled from
   fragments (`status` × `type` × `locale`). Any user-influenced fragment means part of the
   namespace is attacker-controlled.

### The role-ID cardinality diff
A cheap operation with a deterministic oracle, distinct from mass-assigning `role` **[S]**:

**Count the role/permission IDs the API enumerates, and count the roles the UI renders. The
delta is your target list.** Role and permission endpoints routinely return more IDs than
the UI ever displays; if assignment accepts opaque UUIDs, non-UI values are worth testing.
Then diff user counts, or watch for new "internal" objects appearing, after a role swap.

This is **UI allowlist ≠ server allowlist** reduced to a number you can measure.

### Tenant isolation beyond result sets
Testing "can A read B's data" misses the derived surfaces. A shared service also persists
things that merely *derive* from a tenant's input: **query text** (the literal values in
`WHERE`/`INSERT` clauses), job names, cache keys, metadata, error strings, **blob versions**,
usage analytics, scheduler state. Test each separately — these have no owner, so nobody
gated them. Old storage/blob versions in particular often retain secrets the current version
has been cleaned of. **[S]**

**Oracle:** two owned accounts. A's token requests B's object. Pass = HTTP 200
**and** response body contains B's unique canary string. Not just a 200.

---

## 8.3 GraphQL

### Discovery
Paths: `/graphql`, `/api/graphql`, `/graphiql`, `/v1/graphql`, `/query`, `/gql`,
`/graphql/console` — including on API subdomains REST docs never mention.
**Mobile apps are the best source** — `strings`/`jadx` on an APK regularly yields
endpoints and operation names unreachable from web.

Fingerprint the engine first with **graphw00f** (actively maintained, 35+ engines).
Engine identity tells you which defaults are missing.

### Schema recovery when introspection is off
- **Field suggestions** ("Did you mean 'userByEmail'?") leak the schema even with
  introspection disabled — an Apollo/graphql-js default many deployments forget.
  **Clairvoyance** reconstructs schemas from them.
- Introspection disabled on prod but **enabled on staging/`-dev`** is extremely
  common. Grab the schema there, use it against prod.

### The authz bugs that pay
1. **Field-level vs object-level authz — the dominant real bug.** Authorization is
   enforced at the root resolver, then a nested or aliased field resolves without a
   check. Method: take a query you *are* authorized for and append restricted
   sibling fields (`licenseKey`, `email`, `internalNotes`, `stripeCustomerId`).
   Schemas grow to hundreds of types; coverage gaps are the norm.
2. **BFLA on mutations.** Enumerate every mutation from the schema, replay each at
   three tiers (unauth / low-priv / cross-tenant). Mutations are frequently added
   without the role guard the equivalent REST route had.
3. **Mass assignment via input types.** Input objects commonly accept privileged
   properties the UI never sends. Diff the input type's fields against what the
   client actually submits.
4. **GraphQL-specific IDOR.** One request can carry N aliased operations, so
   enumeration is ~N× cheaper than REST. Also: Relay global `node(id:)` IDs are
   often base64 of `Type:id` — decode, re-encode for another type, and object-type
   confusion sometimes bypasses the resolver's ownership check.
5. **Exposed Apollo Federation subgraphs — high impact, under-tested.** The router
   enforces JWT validation, cost limits and safelisting; the **subgraph usually
   enforces nothing.** Find it directly (separate host/port, internal-ish naming)
   and you bypass every control at once.

### Batching / aliasing
Rate limits, WAFs and anti-automation are overwhelmingly **per-HTTP-request**. One
request with N aliases = 1 against the limit, N resolver executions.

Test matrix: is array batching accepted? What's the alias ceiling? Does the limiter
count operations or requests? **Does it apply to `login` / OTP-verify /
password-reset / 2FA-verify mutations?**

Impact framing that gets paid: **credential or OTP brute force**, not "I sent 500
queries." Tooling: BatchQL, GraphQLmap.

### Persisted queries
**APQ (Automatic Persisted Queries) is not a security control** — any operation
registers itself at runtime via its hash. If a program believes APQ is an
allowlist, *that belief is the bug.* The real control is a CI-built **Trusted
Persisted Query List**. Test: does the server still accept full query text when a
hash is absent? Does a GET variant skip the check? Does the multipart/upload path?

### CSRF and transport
GET-accepted mutations; `application/x-www-form-urlencoded` or `multipart/form-data`
accepted (→ HTML-form CSRF); **CSRF validation applied to the JSON path but not the
multipart upload path** is recurring. **WebSocket subscriptions:** credentials go in
`connection_init`, not upgrade headers, so resolver-level checks are often skipped;
revoked permissions frequently don't terminate live streams (authorization drift);
missing Origin validation gives CSWSH.

### Nested query DoS — ⚠️ check policy first
Cyclic type relationships (`User → posts → author → posts …`) without depth limiting
(7–10 recommended) or cost analysis. **Many programs treat resource exhaustion as
out of scope by default.** The reportable framing is usually *"no depth/cost limit
configured"* demonstrated by **cost measurement**, not actual degradation.
**Do not degrade a production service.**

### Tooling status
**graphw00f** — maintained, use it. **Clairvoyance** — works. **InQL** (Burp) — the
practical workhorse. **graphql-cop** — *unmaintained since 2022*; fine as a fast
first pass but absence of findings means nothing. **GraphQL Armor** is the defensive
library — its config knobs (max-aliases, max-depth, cost) are a checklist of what to
test for the absence of.

---

## 8.4 Modern authentication

### OAuth / OIDC — the five-condition matrix
**Core insight: the redirect is not the exploit; the code exchange is.** An open
redirect alone is a Low. You need a captured code to become a token.

Chain condition 1 with at least one of 2–5 for a High/Critical:

1. **`redirect_uri` not exact-matched** — the entry condition. Test path traversal,
   encoded separators, subdomain wildcards, parameter pollution, appended
   paths/fragments.
2. **Authorization codes are multi-use** — replay the same code at the token
   endpoint. A second success means interception alone is sufficient.
3. **Token endpoint doesn't revalidate `redirect_uri`** — submit a code with a
   different `redirect_uri` than authorized. Violates RFC 6749 §4.1.3 **MUST**. Any
   URI that captured the code can redeem it.
4. **PKCE not enforced** — request without `code_challenge`, exchange without
   `code_verifier`. If both paths work for the same client, that's a **PKCE
   downgrade** (cf. CVE-2025-4144).
5. **Implicit flow still active** — `response_type=token` puts tokens in the
   fragment; third-party resources on the callback page see them via Referer.

Also: **missing or unbound `state`** on "Connect account" / social-link features =
CSRF-to-ATO, reliably a P2. Check whether `state` is merely *present* vs actually
*bound to the session* (state fixation).

### SSO / SAML / tenant confusion
- **Tenant confusion (B2B SaaS) is the live money class.** IdP config stored
  globally rather than per-tenant; the tenant is resolved during *discovery* then
  trusted, instead of re-verified on the authenticated callback. **Test:** start
  login as tenant A, complete the callback asserting tenant B's identity. Also test
  whether assertions are validated against *that tenant's* certificate specifically.
  This is the confused-deputy shape.
- Real 2026 examples: **Sentry** SAML SSO identity-linking bypass (GHSA-ggmg-cqg6-j45g,
  fixed 2026-02-18) — linking an identity you don't own; **miniOrange SAML 2.0 SSO
  for WordPress** — two CVSS 9.8 unauthenticated assertion-forgery bypasses across
  seven editions (July 2026).
- Classics still worth running: signature not verified, signature wrapping (XSW),
  comment truncation in NameID, unsigned assertion inside a signed response,
  `samlify`-class library CVEs.

### Structured-field → mail-layer seam
A clean example of a G6 seam, and absent from most checklists **[S]**: an auth flow accepts
an email address inside a **JSON string**. The JSON parser guarantees "a string"; the mail
layer assumes "one address". **Control characters — especially newlines — inside that string
can cause the mailer or an intermediate parser to treat it as multiple recipients**, so reset
material reaches an inbox that was never intended.

Test it anywhere a structured field feeds a delivery layer: password reset, email change,
invites, notification preferences. Per the two-owned-accounts rule, confirm **only** by
observing whether material arrives at a second inbox **you control** — never by broadcasting
tokens.

The generalization is worth more than the instance: *what does the encoding layer guarantee,
and what does the consuming layer assume about structure?*

### Magic link / OTP
Link or OTP not invalidated on use or on re-issue; prior unproven credentials not
revoked at sign-in; OTP brute force where the limiter is per-HTTP-request
(**chain with GraphQL/JSON batching**, §8.3); link leakage via Referer or
third-party analytics; email-change + magic-link race; **link bound to email but
not to the requesting session/device** → interception = ATO.

### Session
Does the session ID **rotate on privilege change** (login, MFA completion, role
elevation)? Still a live finding, especially around SSO callbacks. Are sessions
invalidated on password change, email change, MFA enrollment, logout-all?

### JWT — the easy ones are gone, one still pays
`alg:none` and RS256→HS256 confusion still work but pay small ($600–$1.2K) and are
mostly library bugs now (CVE-2026-22817 Hono, CVE-2026-29000 pac4j-jwt CVSS 10.0).

**The one that still pays well is `kid` injection** (reported $15K). `kid` is
attacker-controlled and often used as a **filesystem path, a DB lookup key, or a
URL** — so it's path traversal / SQLi / SSRF *in a JWT context*. There's no CVE
class for it because it isn't a library bug. Also check `jku`/`x5u` pointing at an
attacker-controlled JWKS.

---

## 8.5 Parser, cache and protocol disagreement

> **The unifying 2026 heuristic: every entry in PortSwigger's 2025 Top 10 exploits
> disagreement between subsystems about parsing, caching, or normalizing.** Hunt
> handoffs, not endpoints.

### Desync is re-opened, not closed
**HTTP Terminator** (Kettle, Black Hat USA 2026) explored ~30,000 candidate vectors
against 30,000 authorized sites and found **~700 vulnerable targets** — banks,
government infrastructure, security products, an airport. **Source and blueprint
published.**

New triggers: `Content-Type: multipart/byteranges` (CL.0 desync — hit 200+ sites,
because servers reuse *response*-parsing logic for requests); `Transfer-Encoding:
gzip` with HTTP/1.0; **dual matching `Content-Length` headers**; CONNECT variations
over HTTP/2; the **"dangling byte"** (leave the smuggled request one byte short so
the victim's first byte completes it) which makes response-queue poisoning far more
reliable.

The generalizable concept — **Shared-Parser Confusion**: response-processing rules
misapplied to requests wherever parsing code is shared. Use it as a hypothesis
generator.

Still findable: **HTTP/2 downgrade** (front end speaks H2, upstream H1.1 — explicit
length vs framing mismatch, and header sanitization during downgrade is frequently
incomplete); classic CL.TE / TE.CL on legacy stacks and appliances; H2 request
tunnelling → cache poisoning.

### Cache poisoning
Unkeyed inputs: headers, query params, and especially **format-switching params not
in the cache key** — Next.js `__nextDataReq` and `x-now-route-matches` change
response *format* without being keyed, giving internal-cache poisoning where JSON
is reflected as HTML. **Internal/framework-level caches (Next.js, Nuxt, CDN+SSR)
are much less picked-over than CDN edge caches — that's where 2026 findings are.**
Param Miner for unkeyed-input discovery.

### Web cache deception
**Why it breaks:** the cache classifies static-vs-dynamic by extension or path
prefix; the origin routes by *normalized* path. Different normalization = the cache
stores an authenticated response under a "static" key.

Method: find an endpoint returning dynamic, sensitive, per-user data (`/api/me`,
account page, token endpoint). Then probe normalization discrepancies: path
delimiters (`;` `?` `#` `@` `!` and encoded forms), encoded slashes, traversal
tokens, appended static extensions. Goal: a URL the cache reads as `/thing.css` and
the origin reads as `/account`.

**Evidence:** fetch the crafted URL as victim, then fetch it unauthenticated from a
clean context and show the victim's data, plus cache-hit headers (`X-Cache`,
`CF-Cache-Status`, `Age`).

> ⚠️ **Demonstrate against your own test account only.** Poisoning a shared cache
> with another user's data is real harm. Many programs require a cache-busting
> prefix.

### Other handoff classes from the Top 10
- **ORM leaking** — *the highest-signal new class for API hunters.* Filter/search/
  sort APIs over an ORM where user-controlled filter expressions reach fields the
  API never meant to expose (`password`, `api_key`, `reset_token`). Comparison
  operators turn it into server-side binary-search exfiltration.
- **Successful errors / SSTI** — apply full SQLi methodology (error-based →
  boolean-blind → time-based) to template engines. Verbose engine errors are an
  oracle; you don't need output reflection.
- **Unicode normalization** — any check that runs *before* normalization: overlong
  encodings, byte truncation, confusables, casing (dotless ı → I), combining
  diacritics.
- **Parser differentials** — duplicate JSON keys (Erlang takes first, JS takes
  last), duplicate headers, YAML/JSON mismatch. Classic shape: **the auth layer
  validates one copy, the app reads the other.**
- **HTTP/2 CONNECT** — 200 vs 503 is a free internal port-scan primitive. Cheap to check.
- **Path traversal filter classes** — early string termination, single-pass `../`
  strip, incomplete multi-layer decoding, fixed-buffer truncation that drops the
  filter suffix. Map each to how the runtime *and* the reverse proxy normalize before
  the access check.

---

## 8.6 SSRF and cloud

### SSRF → metadata in the IMDSv2 era
IMDSv2 requires a PUT for a token, rejects certain headers, and enforces a hop
limit — which kills naive SSRF. What still works conceptually:

- **IMDSv1 still enabled.** Backward compatible, and large fleets predate
  IMDSv2-by-default. **Always test v1 first.**
- **Method control (can issue PUT) + header control (can set the token-TTL header)**
  satisfies v2's requirements.
- **Redirect-following SSRF** bypasses some v2 protections.
- **IMDSv2 does nothing for every other internal target:** Kubernetes API server,
  kubelet (:10250), Redis, etcd, Consul, internal admin panels, ECS task metadata
  (`169.254.170.2`), GCP metadata (needs `Metadata-Flavor: Google` — header control
  again), Azure IMDS (needs `Metadata: true`).
- **Escalate blind → readable** with the 2026 redirect-loop technique: different
  redirect-depth counts produce distinguishable error states. This turns
  unreportable blind SSRF into impact.

**Evidence:** the credential's *identity* (`sts:GetCallerIdentity` output, the role
name) is the proof. **Do not enumerate or touch data with obtained credentials**
unless the program explicitly permits it, and state in the report that you stopped.

**Discovery:** systematic header-name bruteforce with OOB callback values beats
guessing `X-Forwarded-*`. **Oracle:** your DNS/HTTP log records a hit with the
matching nonce. Binary, no judgment.

### Subdomain takeover — still paying
Pipeline: `subfinder -dL` + amass → **dnsx filtering for CNAME only** (A/AAAA
can't be taken over) → httpx for status/title → nuclei takeover templates.

**The edges that matter:**
- **Follow CNAME chains 2–3 hops deep.** Single-pass scanners miss orphaned chains.
- Nuclei covers ~80 services; **the money is in services it doesn't** — Render,
  Fly.dev, Bubble, Replit, Cloudflare Pages, GitLab Pages, StatusPage, Zendesk,
  `*.myshopify.com`, `*.readthedocs.io`.
- **Post-acquisition orphans are the best source in 2026.** A vendor gets acquired,
  retires its wildcard, and every customer CNAME dangles. Documented $4,500 payout
  from exactly this. **Build a list of acquired SaaS vendors and reverse-search
  their CNAME targets.**
- Historical discovery: Wayback, CommonCrawl, CT logs for CNAMEs that used to exist.

**False-positive discipline:** a dangling CNAME is **not** a takeover. Confirm
NXDOMAIN at the destination and compare sibling subdomains. Many providers reserve
names or require ownership verification.

> ⚠️ **Scope nuance:** report the dangling record. Claiming a third-party resource
> to "prove" it is an action against that third party and risks hijacking real
> traffic. If the program requires a claim-proof, ask first.

**Severity depends entirely on context — state it:** OAuth/SSO callback allowlist =
critical; parent-domain cookie scope = high/critical; MX or SPF include = high
(email spoofing); static marketing page = medium/low.

### Object storage
Start **passive**: GrayhatWarfare indexes ~318,000 buckets and ~4B files across
S3/GCS/Azure, searchable without auth. Then permutation enumeration on naming
conventions (`-prod`, `-assets`, `-backup`, `-staging`, `-logs`, `-dev`, `-uploads`)
with `cloud_enum` / `s3enum`.

Beyond "public bucket": **authenticated-but-any-AWS-principal read** (common and
often missed — not publicly listable, but any authenticated AWS account can
GetObject); over-broad IAM granting `s3:GetObject` to `*`; **writable buckets** —
highest impact, because JS/asset overwrite gives stored XSS on the main app;
pre-signed URL generators with absurd expiry; **bucket namespace hijacking** after a
bucket is deleted (re-register the name, inherit trust from hardcoded references).

### CI/CD and GitHub Actions — very active in 2026
⚠️ **Whether a target's GitHub org is in scope varies enormously.** Confirm before
touching workflows, and **never actually publish a package or push to a branch.**

- **Pwn requests.** `pull_request_target` checks out fork-controlled code and runs
  it with the base repo's secrets. GitHub hardened this — **as of 2026-06-18
  `actions/checkout` refuses common pwn-request patterns by default.** So look for
  **pinned old versions** of `actions/checkout`, forks of it, manual `git fetch` of
  the PR ref, or `workflow_run` used as a workaround.
- **Actions cache poisoning.** A low-privilege job writes into a cache namespace a
  privileged job restores from. ~15,000 repos affected. **TanStack (2026-05-11):**
  fork PR → `pull_request_target` ran attacker code → poisoned cache → publish
  workflow restored it → lifted the runner's OIDC token from memory → **84
  malicious versions across 42 `@tanstack/*` packages.** Same pattern hit mistralai
  and guardrails-ai. GitHub's mitigation is **`cache-mode`** (added Sept 2026:
  `read`/`write`/`write-only`/`none`) — **absence of least-privilege `cache-mode` on
  a repo with a privileged publish workflow is the finding.**
- **OIDC trust policy misconfiguration.** The classic: the IAM trust policy
  validates `aud` but **not `sub`**, so *any* GitHub repo can assume the role.
  Datadog found **500+ misconfigured AWS roles** this way in early 2026. Also
  wildcarded `sub` (`repo:org/*:*`), or a `sub` matching a branch an attacker can
  create. GitHub now issues **immutable subject claims** (owner/repo *IDs*) for new
  repos as of 2026-04-23 — **which means older trust policies keyed on *names* are
  vulnerable to repo-rename/recreate attacks.**
- **Secrets in artifacts and logs** — artifacts containing `.git`, `.env`,
  kubeconfigs, source maps; secrets echoed in public workflow-run logs; artifacts
  from public repos downloadable without auth.
- Also: self-hosted runners on public repos; unpinned third-party actions (`@main`);
  script injection via `${{ github.event.* }}` interpolated into `run:` blocks (PR
  titles, branch names, issue bodies).

---

## 8.7 Secrets

Hunt by matching high-signal **key names near assignment operators** (`api_key`,
`aws_secret`, `client_secret`), not only known token formats — name-based patterns
catch misnamed and vendor-specific secrets that format-only detectors miss. A widely-forked
reference list of credential-ish identifier names:
https://gist.github.com/h4x0r-dz/be69c7533075ab0d3f0c9b97f7c93a59

**Tooling:** **TruffleHog** for reporting — the **`--only-verified` flag actually
validates whether a credential is live**, and a verified-live key is undeniable
impact where an unverified string is noise. **Gitleaks** for fast repo sweeps and
pre-commit. **jsluice** (BishopFox) extracts URLs, paths and secrets from JS via
**AST rather than regex** — the quality tool. **js-snitch** runs remote JS through
TruffleHog + Semgrep. **MapperPlus** bulk-recovers source from exposed `.js.map`.

Workflow: katana → collect JS → check for `.map` siblings → MapperPlus →
jsluice + TruffleHog over recovered source.

### Client config that is not itself a secret, but mints one
Secret scanning looks for credentials. This class is different and is missed by
`--only-verified` workflows entirely **[S]**:

Mine SPA and dev-subdomain JS — and reconstructed source maps — for **cloud identity client
config**: Cognito `userPoolId`, `clientId`, `identityPoolId`, and the equivalents on other
providers. A client ID on its own is common and usually not a finding. **The impact appears
when an identity pool will mint usable temporary cloud credentials through an
over-permissioned IAM role**, especially where signup or unauthenticated identities are
enabled.

**Severity lives in the IAM role, not in the leak.** So the finding to report is the
*over-permissioned identity*, and the evidence is the credential's **identity**
(`sts:GetCallerIdentity`, the role name) — not anything you did with it. Misconfigurations
of this kind cluster across sibling subdomains, so check the whole family once you find one.

> ⚠️ **Report a found secret; do not use it.** Validate existence via the vendor's
> own introspection endpoint if one exists. Verification-by-use beyond proving
> validity is usually outside safe harbor. Leaked credentials are time-sensitive —
> report immediately.

---

## 8.8 AI / LLM application surfaces

See [06 §6.5](./06-target-selection.md) for payouts and scope rules. The one rule
that determines whether you get paid:

> **Reframe the finding as a classical bug class.** Prompt injection is a *delivery
> mechanism*, not the vulnerability. "AI jailbreak" gets closed; "unauthenticated
> SSRF via document-processing pipeline" gets paid.

And Cloudflare's framing, which is the sharpest statement of the bar:
> **"Prompt injection alone is not a finding."** Require a code-level boundary
> failure: content reaches another principal's context, invokes authority the
> requester lacks, discloses data they cannot read, or drives a sink they cannot
> reach directly.
>
> **"A guardrail prompt is not a security boundary."** Count only deterministic
> checks, resource-scoped authorization, isolation, binding, and constrained
> credentials.
>
> Model output, memory, tool descriptions and MCP responses are **untrusted inputs**.

Highest-paying first: **agent tool abuse reaching infrastructure** (SSRF/RCE with a
weird trigger) → **cross-tenant exfiltration** → **indirect injection** via a
channel the victim trusts → **system-prompt extraction that reveals secrets** →
**cross-session memory leakage** → **LLM-app IDOR** (often a plain BOLA in the app's
API around the AI feature — the easier and more reliable bug) → **RAG leakage**
where retrieval ignores per-document ACLs.

Exfiltration channels worth checking: markdown image rendering to an attacker URL,
link auto-unfurling, agent-initiated requests, rendered HTML.

---

## 8.8b Mobile: exported components
Harvesting endpoints and GraphQL operation names from an APK (§6.3) is recon. The **IPC
trust boundary** is a separate, under-tested surface **[S]**.

Triage it the same way you triage web: **map and rank, then hunt.** Extract the main APK,
enumerate **exported activities** (and the other exported components — services, receivers,
providers), generate launch commands for them, and only then spend expensive analysis on the
components that rank interesting.

Why it's worth the setup cost: per [11 §G10](./11-non-obvious-thinking.md), other hunters
drop off at the mobile toolchain barrier — which makes it a low-competition surface by
construction.

## 8.9 The crowded classes (Tier 3)

**XSS, missing headers, SPF/DMARC, self-XSS, clickjacking on non-sensitive pages,
rate-limit absence without impact.**

**78% of valid hackbot findings were XSS.** You will be duplicate #40. Hunt these
only when they **chain** — XSS on a broad parent domain escalating through an
extension or `postMessage` channel that trusts wide origins; stored XSS via a
writable asset bucket; XSS whose impact is session theft on a sensitive subdomain.

If you do report XSS: the oracle is **actual JS execution in a headless browser**,
never "the string appears in the response."

---

## 8.10 Out-of-scope-by-default checklist

Verify per program, every time:

- **DoS / resource exhaustion** — including GraphQL nested-query and batching DoS.
  Demonstrate *missing limits*, not actual degradation.
- Rate-limit absence without demonstrated impact
- Self-XSS, clickjacking on non-sensitive pages, missing headers, SPF/DMARC absent
- Social engineering, physical, anything touching a real third party's account
- **Model-level AI issues** — jailbreaks, alignment, hallucination, bias, content
  policy (unless an explicit model-safety track exists). Google's AI VRP excludes
  these as a *category*; OpenAI treats base-model injection as a known limitation.
- Automated scanner output without manual validation — increasingly auto-closed
- **Third-party-hosted assets, including GitHub orgs and CI/CD**, unless explicitly listed
- **Destructive actions:** publishing a package, pushing to a branch, poisoning a
  shared cache with real users' data, using a discovered credential beyond validity
  verification, triggering an agent's destructive tool outside a named test tenant

---

## 8.11 Recon stack (late 2026)

**ProjectDiscovery** remains the core pipeline — manage via `pdtm`:
`subfinder → alterx → dnsx → naabu → httpx → katana → nuclei`

- **nuclei** actively developed; 2026 releases added 226 templates / 123 CVEs, with
  a notable push into **AI/LLM attack surface** (Flowise, Langflow, LiteLLM,
  ComfyUI-Manager, Marimo, NocoBase).
- **nuclei-templates-ai** — AI-generated templates for uncovered CVEs. Faster
  coverage, lower precision: **treat hits as leads.**
- **dnsx is the underrated one** — CNAME filtering for takeover work, wildcard
  detection, bruteforce with alterx permutations.
- **amass is not deprecated.** Division of labor: subfinder for breadth on a first
  pass, amass for depth and asset *relationships* once a target proves worth it.

**Proxy:** **Burp Pro** ($475/yr) is still the control plane for serious work and
is **required** for desync, cache poisoning and smuggling — that tooling (Turbo
Intruder, Param Miner, HTTP Request Smuggler, ActiveScan++, InQL) only exists there.
**Caido** (free Basic, $200/yr Individual) wins on speed and memory over long
sessions, and **v0.58.0 made it viable for races** (Replay Pipeline with Last Byte
Synchronization, HTTP/2 beta). **YesWeCaido** pulls YesWeHack programs and scopes in
automatically. Practical consensus: Caido for day-to-day manual testing, Burp Pro
for edge cases. Many run both.

### The meta-point
> Hunters consistently landing P1/P2 on competitive targets are **not** running
> broader automation — they're running **narrower** automation against **more
> carefully selected** attack surface, combined with manual analysis generic
> pipelines skip. Fewer tools, right sequence, better notes, better validation.
>
> A big stack gives you the illusion of coverage without understanding.

---

**Next:** [05 — Validation Gates](./05-validation-gates.md) ·
[06 — Target Selection](./06-target-selection.md) ·
[07 — Reporting](./07-reporting-that-gets-paid.md)
