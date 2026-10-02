---
name: authz-hunt
description: Hunt authorization failures — IDOR/BOLA, BFLA, BOPLA/mass assignment, shadow API versions, tenant isolation. Use when testing an authenticated API or multi-tenant app. This is the highest-yield class family that autonomous scanners are worst at.
argument-hint: "[component-or-endpoint]"
---

# Authorization Hunt

Authorization is the most productive class family in bug bounty and the one
automated tooling is worst at, because **the check that should exist isn't in the
code to be found.** You have to know the role model and the tenancy model, then
find the path that skips them.

## Prerequisites

- Scope cleared (`scope-guard`), rate limit known
- **Two accounts you control**, both yours: `tenant-a` and `tenant-b`
- A **unique canary string** in Tenant B's data (e.g. `CANARY-B-7f3a`) so proof is
  unambiguous and harmless
- Where roles exist, one low-priv and one elevated account in the same tenant

**Never** use a discovered identifier that might belong to a real customer. If
enumeration returns UUIDs, do not "just check one" — that one is someone's data.

## The core principle

> **The UI's allowlist is not the server's allowlist.**

Enumerate what the **API** accepts, not what the UI offers. The gap between those
two lists is where authorization bugs live. Most testers only ever see the UI's list.

## Method

### 1. Build the authorization map
For every route: who can reach it (`anonymous | any-authenticated | tenant-member |
tenant-admin | staff`), and **how that is enforced** — middleware, decorator,
in-handler check, or nothing visible.

Routes with no visible enforcement are your priority queue.

Also enumerate the roles **the API knows about**, not the ones the UI shows. Role
and permission endpoints frequently return more IDs than the UI ever displays; if
role assignment accepts opaque UUIDs, non-UI values are worth testing.

### 2. BOLA / IDOR — object-level
Swap object identifiers **everywhere**, not just the obvious path parameter:
- path params, query params
- **nested bodies and arrays** (most-missed)
- secondary identifiers (`accountId` alongside `invoiceId`)
- identifiers in headers and cookies

Then: is the object authorized against the **session's tenant**, or merely looked up?

Watch for IDs that are guessable, sequential, or leaked elsewhere — search results,
notification emails, public profiles, JS bundles. **"Unguessable ID" is not
authorization**, and saying so in the report pre-empts the "defense in depth"
pushback.

### 3. BFLA — function-level
Enumerate **every route × every method × every role.**
- Methods the router doesn't handle but the framework allows (`PATCH` where only
  `GET`/`PUT` are documented)
- Method-override headers
- Admin routes reachable with a user token because the guard is on the UI, not the API
- Does a **second endpoint reach the same sink** with fewer checks?

### 4. BOPLA — property-level
The API authorizes the *object* but not its *properties*.

- **Read side:** diff the API response against what the UI actually renders. Extra
  fields are disclosure.
- **Write side (mass assignment):** does the request accept fields the UI never
  sends — `role`, `isAdmin`, `isVerified`, `tenantId`, `balance`, `createdAt`,
  internal flags? Harvest candidate names from the object's own GET response, the
  GraphQL schema, or JS bundles.

### 5. Shadow and zombie versions — highest yield
`/api/v2/users/{id}` ships the new ACL. **`/api/v1/users/{id}` still exists with the
old check, or none.**

Enumerate `v1…vN`, plus `/internal/`, `/admin/`, `/beta/`, `/legacy/`,
`/_internal/`, `/api/private/`. **Deprecated endpoints frequently have weaker auth,
not just older features.**

### 6. Path-of-least-resistance checks
- Is the authz check on **every** path to this handler, or only the UI's path?
- Does a **batch/bulk variant** inherit the single-item validation? Error paths in
  batch handlers are a classic desync between validate-loop and execute-loop.
- Is normalization (path, unicode, encoding) done **before or after** the check?
- Do internal library wrappers around storage/filesystem enforce caller authz at
  **every** entrypoint?
- Does a lower-trust API path reach a higher-trust operation?

### 7. Tenant isolation beyond result sets
Multi-tenant boundaries often apply to result sets but not to **metadata, query
text, blob versions, or shared analytics.** Test whether tenant A can observe
tenant B's query strings, object names, counts, or historical versions — not only
their records.

### 8. GraphQL
See `docs/08-vuln-class-playbooks.md` §8.3. Priorities: field-level vs object-level
authz (the dominant real bug), BFLA on mutations at three privilege tiers, mass
assignment via input types, and **exposed Apollo Federation subgraphs** — the router
enforces everything, the subgraph enforces nothing.

## The oracle (Gate 5)

Deterministic, no model judgment:

```
Account A token  →  request B's object
PASS  = HTTP 200 AND response body contains B's canary string
FAIL  = 403/404, or 200 with only A's own data
```

A bare 200 is **not** a pass — many APIs return an empty or filtered 200. The
canary is what makes it proof.

For BFLA: issue the identical request as low-priv and as elevated. Pass = the
responses are equivalent **when they must differ.**

Run it twice. Intermittent means not understood yet.

## Impact sentence

You must be able to complete this with concrete nouns, or you have no finding:

> An attacker with **\<access\>** can **\<read/modify/delete\>** **\<asset\>**
> belonging to **\<victim\>**.

Kill it yourself if: the data is already public, the effect is self-only, or it's on
the program's accepted-risk list.

## Severity honesty

- Cross-tenant **write** > cross-tenant **read** > same-tenant cross-role.
- Requires authentication? Say so and expect a cap.
- One record proven, class clearly generalizes? Say exactly that — "I confirmed one
  object; the missing check appears to apply to the collection" is credible.
  Claiming you dumped the table when you didn't is not.

## Hard limits

- Two accounts you own, always. Never a real customer's identifier.
- **One record is proof. A table is an incident you caused.**
- No writes to objects you don't own unless the program explicitly permits it —
  and if it does, write only to your own second tenant.
- Stop at the minimum proof and report. If the chain could go deeper, ask the
  program in the report rather than continuing.
