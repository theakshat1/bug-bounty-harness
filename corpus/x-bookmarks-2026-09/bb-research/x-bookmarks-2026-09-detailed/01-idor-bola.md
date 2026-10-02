# IDOR / BOLA / Authorization mismatches

**Cluster file:** `01-idor-bola.md`  
**Audience:** Akshat (authorized / in-scope hunting only)  
**Constraint:** Abstract methodology only — **no** reproduction steps, payloads, PoCs, exploit recipes, Intruder setups, or attack procedures.  
**Items in this cluster:** 7

---

### 1.1 Hidden role UUID IDOR → privilege escalation

- **Root-cause class:** **UI allowlist ≠ server allowlist** — role-assignment APIs trust client-supplied role UUIDs and enumerate more role IDs than the UI exposes, enabling IDOR-driven privilege escalation to hidden “internal” roles.
- **Affected component:** Authenticated role/permission APIs and role-change flows; opaque role UUID identifiers.
- **Impact:** Privilege escalation beyond UI-exposed roles (admin → internal employee class outcome as titled); €2000 bounty as reported by author.
- **Conditions called out:** Authenticated user with role-change rights; role APIs returning more role IDs than UI shows; server trusts client-supplied role UUID.
- **What the source teaches (abstract):** Mine Burp history for role/permission enumeration responses that list more IDs than the UI. If role assignment accepts opaque UUIDs, try non-UI values. Diff user counts / new “internal” objects after role swap. Classic: UI allowlist ≠ server allowlist. — Diff/planning framing only; no request recipes.
- **Tags:** IDOR, privilege-escalation, roles, Burp-history, access-control
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://medium.com/@asharm.khan7/2000-bounty-idor-to-privilege-escalation-from-admin-to-internal-employee-a36db23fa10a
- **Notes:** [Researcher:10] ok

---

### 1.2 JS graveyard endpoints → authz differentials

- **Root-cause class:** Dead/historical frontend routes → IDOR/BOLA / broken auth / forgotten admin
- **Affected component:** Historical frontend JS bundles / forgotten API routes
- **Impact:** Authorization failures (IDOR/BOLA, forgotten admin) on reachable historical routes the UI no longer links.
- **Conditions called out:** Readable JS bundles; authenticated and unauthenticated test accounts preferred
- **What the source teaches (abstract):** Mine historical frontend bundles for /api|/admin|/internal routes the UI no longer links, validate reachability, then focus authorization differentials (IDOR/BOLA, broken auth, forgotten admin) rather than status-code alone. Extract note: Strong reusable recon→authz pattern. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** JS-recon, dead-endpoints, IDOR, BOLA, API
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://x.com/whotfbunny/status/2098862073057038746
- **Notes:** [Researchy:P.6] Strong reusable recon→authz pattern.

---

### 1.3 Sourcemap / JS → UUID pivot → IDOR on ticket/ops domains

- **Root-cause class:** IDOR / BOLA; JS/sourcemap recon leading to hidden API surface
- **Affected component:** Ticket/management domain APIs and hidden routes discovered via JS/sourcemap recon
- **Impact:** Unauthorized access to customer PII and order history via object-ID pivots
- **Conditions called out:** In-scope (or accepted) assets under org control, including ticket/management subdomains referenced from JS; Ability to harvest JS/source maps and enumerate backend API routes; Public or weakly gated endpoints that reveal object identifiers (e.g., event creator UUIDs)
- **What the source teaches (abstract):** Bug-bounty writeup where JS bundles and source maps exposed backend route maps and a secondary management domain. A public listing-style endpoint leaked object UUIDs that pivoted into user-scoped order and PII APIs lacking proper object-level authorization. The extract frames the finding as classic IDOR chaining from leaked identifiers, and notes that org-controlled ticket/ops hosts found via assets may still be in bounty scope. Pattern: After subdomain enum, harvest JS and source maps for hidden domains and API route maps; when a public endpoint leaks object IDs, cross-check other routes that accept the same ID for missing authz.
- **Tags:** idor, bola, js-recon, sourcemaps, api-enumeration, pii, bug-bounty
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://medium.com/@4osp3l/leaking-mtn-customer-pii-order-history-via-idor-on-a-ticket-management-domain-cd3306e36e29?postPublishedType=initial
  - https://x.com/i/web/status/2097681915343962113
- **Notes:** [Deep Research:9] Vuln writeup restated at high level only; no repro/payload content.

---

### 1.4 Report-trained IDOR agent skill + live JS analysis

- **Root-cause class:** IDOR / BOLA (authorization gap on list/search APIs surfaced via JS analysis)
- **Affected component:** Client-side JS-revealed API shapes; list/search endpoints under low-priv session
- **Impact:** Unauthorized bulk exposure of other users' PII and RBAC metadata under low-priv session while anonymous correctly denied
- **Conditions called out:** Prior personal reports used as training material for a reusable agent 'skill'; Target exposes JS that reveals API shapes; low-priv session available
- **What the source teaches (abstract):** Tip that codifying past IDOR lessons into a reusable agent skill (rules, bypass notes, training docs) then pointing it at live JS/API surfaces can find authorization gaps missed manually. Media indicated a critical list leak (~1.1M elements) with email/phone/RBAC/password-history fields under a low-priv session while anonymous correctly received 403. Skill-pack layout mentioned: idor-hunter with SKILL.md, Rules.md, Bypass-Idor.md, Training.md. Pattern: Codify personal IDOR lessons into a reusable agent skill, then apply it to JS/API surfaces—especially list/search endpoints that return other users' PII/RBAC metadata under low-priv while anon correctly 403s.
- **Tags:** IDOR, BOLA, JS-analysis, AI-skill, access-control, bug-bounty-tips
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://x.com/unknown0x3a/status/2096959661446746168
- **Notes:** [Deep Research:20] Methodology tip with impact theme; no repro payloads.

---

### 1.5 Internal library wrapper missing caller authz

- **Root-cause class:** Broken authorization / internal API privilege boundary
- **Affected component:** Internal library wrappers around storage/filesystem APIs (Google VRP surface as named)
- **Impact:** Lower-trust API paths reaching higher-trust file/storage operations when caller authz is missing at an entrypoint.
- **Conditions called out:** Access to in-scope surfaces with internal library wrappers around storage/filesystem APIs
- **What the source teaches (abstract):** When an internal library wraps storage/filesystem APIs, test whether caller authz is enforced at every entrypoint—or whether a lower-trust API path can reach higher-trust file operations. Extract note: Points to brutecat writeup on GFile / internal filesystems (~$100k). Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** authorization, internal-API, GFile, Google-VRP, writeup
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://x.com/GoogleVRP/status/2099890989775093810
- **Notes:** [Researchy:P.3] Points to brutecat writeup on GFile / internal filesystems (~$100k).

---

### 1.6 JWT header / alg / claim trust gaps

- **Root-cause class:** Incomplete JWT verification — weak alg allowlists, asymmetric **key confusion** (accepting signatures verified with the wrong key material), and blind trust of token claims (`aud`/`iss`/role) without server-side authZ.
- **Affected component:** JWT header/alg handling; claim-based authorization (role/admin); apps that accept crafted/modified tokens.
- **Impact:** Auth bypass / privilege escalation when verification is incomplete (header-only changes can escalate). High-ROI BB class per post framing.
- **Conditions called out:** App uses JWT; attacker can craft/modify tokens; weak verification (alg/none, key confusion, missing aud/iss checks) — environmental weakness facts from extract.
- **What the source teaches (abstract):** Always inspect JWT handling: alg allowlists, asymmetric key confusion, claim authZ (role/admin). Header-only changes can escalate if verification is incomplete. Pair with Claude-BugHunter `hunt-jwt-crypto` class skills. — Inspection checklist only; no forge recipes.
- **Tags:** JWT, auth-bypass, privilege-escalation, crypto
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://x.com/zack0x01_/status/2096216309378027867
- **Notes:** [Researcher:23] ok

---

### 1.7 Auth ≠ authZ; sibling backends; debug endpoints in prod

- **Root-cause class:** Multi-backend **residual risk** after partial fixes; **auth ≠ authZ** (project awareness mistaken for ownership); debug/test endpoints left in production.
- **Affected component:** Cloud program multi-backend surfaces; production debug/test endpoints; ownership vs project-membership checks.
- **Impact:** High-value RCE chain class outcomes as claimed by author ($148k framing); residual risk when one backend is fixed and siblings are not.
- **Conditions called out:** Cloud program scope; permission to continue mid-chain (researcher asked Google) under responsible-disclosure norms.
- **What the source teaches (abstract):** A fix on one backend isn’t a fix if siblings remain. Project awareness ≠ ownership checks. Hunt debug/test endpoints left in production. Ethical chaining: pause and get permission before deepening impact.
- **Tags:** cloud, RCE, authZ, regression, responsible-disclosure
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://x.com/aacle_/status/2099070079010754824
- **Notes:** [Researcher:16] ok

