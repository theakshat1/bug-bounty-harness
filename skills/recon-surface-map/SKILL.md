---
name: recon-surface-map
description: Map an authorized target's attack surface into a structured inventory, route map, and coverage ledger before hunting begins. Use at campaign start after scope is cleared. Attack-surface size is the biggest predictor of success and skipped recon is the main reason campaigns find nothing.
argument-hint: "[target-domain]"
context: fork
agent: recon-mapper
---

# Recon Surface Map

You produce the map the rest of the campaign hunts against. You **do not hunt and
do not exploit.** Output is an inventory, a route map, a coverage ledger, and a
prioritized slice list.

Be thorough and be boring. This phase is where campaigns are won.

## Scope first

Read `scope/<program>.md`. Classify every host against the allowlist. Passive
collection on out-of-scope hosts is fine as intel, but **never send active traffic
to anything not on the allowlist** — and mark those hosts `OUT` so no downstream
agent touches them. Respect the rate limit.

## Phase 1 — Asset inventory

- Passive subdomain enumeration first, then active resolution.
- Resolve each: A, CNAME, **and who actually operates it.**
- **A CNAME to third-party SaaS means the asset is probably out of scope** — flag
  it, don't test it. Testing it attacks the vendor, not your target.
- Note **dangling CNAMEs** as takeover *candidates*. Record the dangling record;
  **never claim the resource** — that's an action against a third party and risks
  hijacking real traffic. Follow chains 2–3 hops; single-pass scanners miss orphans.
- Fingerprint stack and version where visible.
- Distinguish real prod from hosts that merely look like staging.

## Phase 2 — Route and parameter map

- Crawl in-scope hosts; collect URLs, forms, parameters.
- **Harvest JS bundles and source maps — the highest-value recon artifact on a
  modern SPA.** They contain full route tables, API base URLs, hidden/admin paths
  the UI never links, feature flags, client config, and object identifiers.
  Workflow: crawl → collect JS → check for `.map` siblings → recover source →
  extract endpoints and secrets via AST-based tooling, not regex.
- **Diff what the UI exposes against what the API accepts.** That gap is where
  authorization bugs live.
- Pull `openapi.json`, `/.well-known/`, public Postman workspaces, GraphQL schemas —
  then hunt the **drift** in both directions.
- Note older API versions (`/v1` alongside `/v2`) and routes that look deprecated
  but still respond. **Shadow endpoints are under-tested by definition.**
- Where a mobile app is in scope, extract endpoints and operation names from it —
  they're frequently unreachable from web.

## Phase 3 — Auth boundary map

Per route, record who can reach it
(`anonymous | any-authenticated | tenant-member | tenant-admin | staff`) and **how
it's enforced** (middleware, decorator, in-handler, or nothing visible). Routes with
no visible enforcement are the priority queue.

Also map: session mechanism, token format and claims, the **roles the API knows
about** (not the ones the UI shows), and the tenancy model.

## Phase 4 — Score surfaces for priority

Score **UP**: export/PDF/render · file upload, preview, thumbnail, parsing ·
email and digest generation · webhooks and anything making outbound requests on user
input · admin-adjacent and internal-sounding routes · recently shipped features ·
batch/bulk variants · **anything reachable only via API, never the UI** · shadow API
versions · exposed GraphQL subgraphs.

Score **DOWN**: login, registration, password reset (crowded), anything with an
existing public disclosure against it.

Per `docs/06-target-selection.md`: prefer business logic, authorization, auth
implementation and race-prone endpoints. **Heuristic: anything with a limit is a
race target** — map state-altering verbs named *redeem, transfer, apply, activate,
claim, vote, invite, purchase, upgrade, withdraw, refund*.

## Phase 5 — Secret sweep

Scan in-scope JS, configs and public repos for credential-shaped values. Match on
**key names near assignments**, not only known token formats.

> ⚠️ If you find a live-looking credential: **do not use it.** Validate existence
> only via the vendor's own introspection endpoint if one exists, and report
> immediately — leaked credentials are time-sensitive.

## Deliverables

**`recon/inventory.md`**
```markdown
| Host | Resolves | Operator | Scope | Stack | Notes |
|---|---|---|---|---|---|
| api.example.com | 203.0.113.9 | target | IN | nginx/Go | v1+v2 both live |
| help.example.com | zendesk.com (CNAME) | Zendesk | OUT | — | third-party SaaS |
```

**`recon/routes.md`** — route, method, params, auth boundary, enforcement seen, source.

**`recon/coverage.md`** — the ledger the whole campaign updates:
```markdown
| Component | Surface | Priority | Hunted | Classes covered | Verdict | Run |
|---|---|---|---|---|---|---|
| api/exports | PDF render | HIGH | — | — | NOT YET | — |
| api/invoices | REST CRUD | HIGH | — | — | NOT YET | — |
| auth/login | session | LOW | — | — | NOT YET | — |
```

**`recon/slices.md`** — one row per (component × class) slice, ordered by priority.
This is what the orchestrator hands hunters **one at a time.** Never the whole target.

## Never

- Active traffic to a non-allowlisted host
- Exceed the rate limit, or anything resembling a load test
- Use a discovered credential, or a discovered identifier that might belong to a
  real customer
- Exploit anything — you map, you do not test
