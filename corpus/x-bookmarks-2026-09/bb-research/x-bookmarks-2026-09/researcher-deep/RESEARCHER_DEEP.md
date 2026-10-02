# Researcher Lane — Deep NON-REPRO Documentation

**Lane:** Researcher only  
**Built from:** `/workspace/researcher-lane-extract-2026-10.md` (2026-10-02 Asia/Calcutta)  
**Constraint:** Educational / authorized bug-bounty framing. Patterns and hunt-planning ideas only — **no** reproduction steps, payloads, PoCs, exploit commands, Intruder setups, or attack walkthroughs. Primary URLs were **not** re-opened for attack detail.  
**Counts:** 23 items · ok=20 · blocked=2 · thin=1

---

## Schema (per item)

| Field | Meaning |
|-------|---------|
| Title | Human-readable name from extract |
| Source URL(s) | Primary link; alternates only when extract already noted them (blocked/thin) |
| Status | `ok` / `blocked` / `thin` + honesty notes |
| Root-cause class | What went wrong at **design/logic** level (not how to exploit) |
| Affected component / surface | Where the issue or method applies |
| Impact | High-level outcome as described in source |
| Conditions / preconditions | Environmental facts called out in extract (not attack steps) |
| Generalized defensive / hunt-planning idea | Non-procedural planning pattern from extract |
| Tags | From extract |
| Lane | Always `Researcher` |

---

## Articles (1–11)

### 01 — SubMap — Subdomain Discovery & IP Intelligence Platform

- **Title:** SubMap — Subdomain Discovery & IP Intelligence Platform
- **Source URL(s):** https://SubMap.net
- **Status:** ok
- **Root-cause class:** Incomplete attack-surface inventory and weak correlation between discovered hosts/products and known vulnerable (CVE/KEV) or takeover-prone DNS states — a visibility/prioritization gap rather than a single application bug.
- **Affected component / surface:** Public DNS and subdomain estate; dangling DNS / takeover-prone records; product fingerprinting correlated to CVE/KEV intel (ASM-style).
- **Impact:** Missed or late discovery of exposed hosts, takeover candidates, and unpatched critically scored products before deeper application testing.
- **Conditions / preconditions:** Target organization with public DNS/subdomains; optional paid features for auto-resolve and takeover checks (as noted by the platform).
- **Generalized defensive / hunt-planning idea:** Map full subdomain inventory early; cross-reference discovered hosts/products against CVE/KEV feeds; prioritize takeover-prone dangling DNS and unpatched critically scored products before deep app testing.
- **Tags:** recon, subdomain, takeover, CVE-intel, ASM
- **Lane:** Researcher

---

### 02 — Agentic Hacks, Real Proofs: Inside Google's PageBreak Project

- **Title:** Agentic Hacks, Real Proofs: Inside Google's PageBreak Project
- **Source URL(s):** https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project/
- **Status:** ok
- **Root-cause class:** Over-trusting LLM vulnerability hypotheses without class-specific, deterministic validators — false positives and unverified “findings” at agentic scale; also, broad codebases without safe-by-design frameworks leave large bug-class surfaces open.
- **Affected component / surface:** Agentic vuln-discovery pipelines targeting classes such as XSS, SQLi, path traversal, RCE, SSRF; monorepo-scale apps with HTTP↔source mapping; validation/oracle layer separate from the hypothesizing agent.
- **Impact:** As framed by Google: agentic discovery can surface real, multi-class flaws when validators prove impact — but unverified candidates are noise; safe-by-design frameworks dramatically shrink findings vs broad codebases.
- **Conditions / preconditions:** Running application environment for validation; specialized validators per vuln class; source/config access (monorepo-scale helps); authenticated scanning infrastructure.
- **Generalized defensive / hunt-planning idea:** Treat LLM hypotheses as untrusted until a separate validator proves impact on a live target. Prefer near-zero-FP pipelines: hypothesize → validate with class-specific oracles → only then report. Unverified candidates seed deeper runs and guide new validator development. Safe-by-design frameworks (eliminate whole bug classes) shrink findings vs broad codebases. Chain-capable agents benefit from HTTP↔source mapping and repeated identical seeds.
- **Tags:** agentic-AI, validation, XSS, SSRF, SQLi, RCE, PageBreak, false-positives
- **Lane:** Researcher

---

### 03 — PageBreak real-world findings (companion post; primary URL gated)

- **Title:** PageBreak real-world findings (companion post; primary URL gated)
- **Source URL(s):**
  - Primary (gated): https://bughunters.google.com/blog/pagebreak-real-world-findings
  - Alternate already noted: https://www.cyberkendra.com/2026/09/google-pagebreak-ai-agent-500-xss-flaws.html
- **Status:** blocked — Original URL returned a Google sign-in wall. Ideas below recovered **only** from the CyberKendra summary already cited in the extract; primary post body was not fetched.
- **Root-cause class (design/logic):**
  1. **Incomplete cache key** — shared CDN/static cache omits path/query dimensions that should distinguish responses, enabling unrelated requests to collide and poison shared JavaScript.
  2. **Signature trust of attacker-influenced params via sibling endpoints** — multi-endpoint signing where an alternate path will sign values the primary flow should not accept with the same key.
  3. **Overly broad extension message-channel trust** — browser extension accepts connections from wide origin scopes (e.g. parent-domain wildcards) without exact sender checks, so XSS on a broad parent can escalate to UXSS.
- **Affected component / surface:** Shared CDN/static JS cache; crypto/signing endpoints; browser extension messaging (Tag Assistant–class UXSS as summarized by alternate).
- **Impact:** Cache-key collision → JS cache poisoning; crypto signature bypass via alternate signing endpoint; UXSS via permissive extension messaging (per alternate summary of gated post).
- **Conditions / preconditions:** Shared CDN/static-cache with incomplete cache key; multi-endpoint signing of attacker-influenced params; browser extension trusting broad origins.
- **Generalized defensive / hunt-planning idea:** (1) Audit cache keys for omitted path/query dimensions that let unrelated requests collide and poison shared JS. (2) When an exploit needs a signature, hunt sibling endpoints that will sign attacker-controlled values with the same key. (3) Extension/message-channel trust: any XSS on a broad parent domain can escalate if the extension accepts connections from “any \*.google.com”-style scopes without exact sender checks. — Planning/audit language only; no reproduction of original PoCs.
- **Tags:** cache-poisoning, XSS, UXSS, signature-bypass, PageBreak
- **Lane:** Researcher

---

### 04 — Linux-CVE-2026-52924-ubuntu-7.0.0-28 (NebuSec / CyberMeowfia)

- **Title:** Linux-CVE-2026-52924-ubuntu-7.0.0-28 (research folder; no README)
- **Source URL(s):** https://github.com/NebuSec/CyberMeowfia/tree/main/security-research/Linux-CVE-2026-52924-ubuntu-7.0.0-28/
- **Status:** thin — GitHub tree has Makefile/C sources but no README (404). CVE synopsis from Ubuntu/OpenCVE advisories only; **exploit source was not reviewed or summarized as PoC.** Gap: no author narrative, no defensive write-up in-tree.
- **Root-cause class:** Kernel SCTP protocol state-machine flaw: use-after-free arising from stale COOKIE-ECHO rollback that frees stream/session state without invalidating a cached stream-scheduler pointer (and related queue caches). Classic “rollback frees tables but leaves dangling caches.”
- **Affected component / surface:** Linux kernel SCTP association / stream scheduler path; Ubuntu 7.0.0-28–class kernels historically named in the folder.
- **Impact:** Kernel UAF in SCTP path (LPE-research class per extract tags); severity/details limited to advisory-level synopsis in extract — not expanded here.
- **Conditions / preconditions:** Unpatched kernel with SCTP; ability to drive SCTP association state (Stale Cookie ERROR rollback path); Ubuntu 7.0.0-28 class kernels historically listed in folder name.
- **Generalized defensive / hunt-planning idea:** Protocol state-machine rollbacks often free tables without invalidating cached pointers or purging queues. Hunt for “rollback/restart” paths that free/rebuild stream or session state but leave scheduler/outqueue caches dangling. Cross-check n-day kernel advisories against still-live distro versions in scope. **Do not reuse public exploit trees in unauthorized environments.**
- **Tags:** kernel, SCTP, UAF, LPE-research, CVE-2026-52924
- **Lane:** Researcher
- **Honesty / gap:** Thin because in-tree documentation is missing; this entry stays at advisory + pattern level only.

---

### 05 — StrikeAgent_AtkBrain-Flash (Yean-Sec AI pentest agent)

- **Title:** StrikeAgent_AtkBrain-Flash (Yean-Sec AI pentest agent)
- **Source URL(s):** https://github.com/Yean-Sec/StrikeAgent_AtkBrain-Flash
- **Status:** ok
- **Root-cause class (process):** AI pentest agents that skip re-rate / second verification inflate false positives; platforms that leak predictable entry paths (`/login`, `/api`) or lack replay/bruteforce controls recreate the same classes of flaws they hunt for.
- **Affected component / surface:** Agentic external foothold hunting; attack-graph self-loop; red-team / SRC / CTF mode separation; the hunter platform’s own auth and path exposure surface.
- **Impact:** Better FP reduction and technique distillation when verification is mandatory; conversely, unhardened hunter consoles become soft targets themselves.
- **Conditions / preconditions:** Explicit authorization; console + model config; tools on PATH (Docker image includes probe tooling).
- **Generalized defensive / hunt-planning idea:** Structure agent cycles as: hunt → attack graph → re-rate/verify → distill techniques into memory. Prefer “finish a full round before asking human” with interruptible chat. Separate red-team / SRC / CTF modes. Hardening of the hunter platform itself (random entry paths, no leaked `/login`|`/api`, replay/bruteforce controls) is itself a checklist for apps you test.
- **Tags:** agentic-AI, red-team, SRC, attack-graph, FP-reduction, authorized-only
- **Lane:** Researcher

---

### 06 — Claude-BugHunter skill bundle (83 skills; H1-pattern driven)

- **Title:** Claude-BugHunter skill bundle (83 skills; H1-pattern driven)
- **Source URL(s):** https://github.com/elementalsouls/Claude-BugHunter/tree/main/skills
- **Status:** ok
- **Root-cause class (process):** Ad-hoc hunting without per-class skill packs and triage gates leads to out-of-scope work, weak evidence, and missed regression/shadow-API/cloud-IAM classes that disclosed-report patterns already encode.
- **Affected component / surface:** Per-class hunt skills spanning XSS, IDOR, SSRF, JWT, OAuth, GraphQL, cache-poison, enterprise VPN/M365/Okta/vCenter, etc.; 7-Question Gate triage; recon→map→hunt→validate→report pipeline; optional Burp MCP.
- **Impact:** Codified methodology improves consistency and reduces bad submits; deliberate OOS split keeps external BB skills separate from internal AD/C2.
- **Conditions / preconditions:** Authorized BB/pentest scope; Claude Code / compatible harness; optional Burp MCP.
- **Generalized defensive / hunt-planning idea:** Codify disclosed-report patterns into auto-loaded per-class skills. Enforce validation gates before submit (scope, impact acceptance, evidence hygiene). Split external surface skills from internal AD/C2 (deliberate OOS). Extend skill packs with: cache-poison, shadow APIs, cloud IAM post-cred, mid-engagement IR detection, regression of “fixed” bugs.
- **Tags:** skills, methodology, triage, hunt-\*, enterprise-platform, reporting
- **Lane:** Researcher

---

### 07 — Quarry — agentic BB console with HackerOne integration

- **Title:** Quarry — agentic BB console with HackerOne integration
- **Source URL(s):** https://github.com/skraft9/quarry-vrc
- **Status:** ok
- **Root-cause class (ops):** Treating resolved reports as closed forever misses high-ROI regression/bypass surfaces; agent memory locked in proprietary stores reduces portability; ignoring CVE feeds vs program assets leaves n-day gaps.
- **Affected component / surface:** Hunt-ops platform: HackerOne sync/submit; regression retest of shipped fixes; Markdown leads as agent memory; advisory/payload FTS (index/search capability — content not reproduced here).
- **Impact:** Faster regression and lead reuse; H1 remains system of record while local DB is cache.
- **Conditions / preconditions:** Docker host; H1 API token; local-only / allowlisted deployment.
- **Generalized defensive / hunt-planning idea:** Treat resolved reports as high-ROI surfaces (new patch code + known PoC context) — queue every fix for regression/bypass. Store leads as plain Markdown so agents can draft/refine without lock-in. Keep H1 as system of record; local DB is cache. Cross-ref CVE feeds against your program assets.
- **Tags:** HackerOne, regression, agentic-ops, leads, advisories
- **Lane:** Researcher

---

### 08 — APSB26-98 — Security updates for Adobe Experience Manager

- **Title:** APSB26-98 — Security updates for Adobe Experience Manager
- **Source URL(s):**
  - Primary (blocked): https://helpx.adobe.com/security/products/experience-manager/apsb26-98.html
  - Alternates already noted: HKCERT Sep 2026 bulletin; NotCVE APSB26-98 (107 CVEs listed, e.g. CVE-2026-19232 Incorrect Authorization CVSS 9.9)
- **Status:** blocked — helpx returned EdgeSuite Access Denied. Ideas recovered via HKCERT/NotCVE/search already cited in extract; vendor HTML body not scraped.
- **Root-cause class:** AEM privilege escalation; security-feature bypass; stored XSS / incorrect authorization (CWE-863) / improper input validation — multi-CVE Priority 2 bulletin (design/authorization and input-validation failures across AEM surfaces).
- **Affected component / surface:** Adobe Experience Manager — Cloud Service, 6.5 LTS, and 6.5 classic lines as versioned in the bulletin.
- **Impact:** Multi-CVE bulletin (Priority 2); NotCVE lists e.g. Incorrect Authorization at CVSS 9.9 among 107 CVEs — high authorization and XSS risk on outdated AEM.
- **Conditions / preconditions:** AEM Cloud Service ≤2026.7.0, 6.5 LTS ≤SP2, or 6.5 ≤SP24 in scope (per extract). Upgrade path noted: CS 2026.8.0 / 6.5 LTS SP3 / 6.5 SP25.
- **Generalized defensive / hunt-planning idea:** On AEM targets, prioritize authZ flaws (CWE-863) and stored XSS in form fields reachable by low-priv users; map bulletin CVEs to version fingerprints. When primary vendor pages block scrapers, use CERT mirrors + CVE aggregators for scope triage. — Version triage only; no exploit procedures.
- **Tags:** AEM, Adobe, XSS, priv-esc, n-day, APSB26-98
- **Lane:** Researcher

---

### 09 — Can Local Open-Weight LLMs Detect Vulnerabilities?

- **Title:** Can Local Open-Weight LLMs Detect Vulnerabilities?
- **Source URL(s):** https://martinativadar.github.io/posts/llm-vulnerability-research.html?v=2
- **Status:** ok
- **Root-cause class (method):** Single-model binary vuln classification on isolated functions is near coin-flip; missing call-graph context and lack of ensemble/meta-decision logic cause false confidence.
- **Affected component / surface:** Static analysis of functions (Chromium dataset); multi-prompt ensemble + ML meta-classifier over agreement/disagreement + metadata.
- **Impact:** Single base LLMs ≈ 50–56% accuracy; with richer context, fine-tuning, multi-view prompts, and a traditional ML meta-model on ensemble signals, final ≈ 76.9% accuracy (per extract).
- **Conditions / preconditions:** Function + caller/callee/location/pattern context; local LLM capacity; labeled train/test set.
- **Generalized defensive / hunt-planning idea:** Don’t trust one model vote — ensemble + meta-decision; feed call-graph context not isolated functions. Gains from richer context (callers, callees, location, code patterns), fine-tuning, multi-view prompts, and ML that learns from ensemble agreement/disagreement + metadata.
- **Tags:** LLM, ensemble, static-analysis, Chromium, ML
- **Lane:** Researcher

---

### 10 — €2000 Bounty — IDOR to Privilege Escalation: From Admin to Internal Employee

- **Title:** €2000 Bounty — IDOR to Privilege Escalation: From Admin to Internal Employee
- **Source URL(s):** https://medium.com/@asharm.khan7/2000-bounty-idor-to-privilege-escalation-from-admin-to-internal-employee-a36db23fa10a
- **Status:** ok
- **Root-cause class:** **UI allowlist ≠ server allowlist** — role-assignment APIs trust client-supplied role UUIDs and enumerate more role IDs than the UI exposes, enabling IDOR-driven privilege escalation to hidden “internal” roles.
- **Affected component / surface:** Authenticated role/permission APIs and role-change flows; opaque role UUID identifiers.
- **Impact:** Privilege escalation beyond UI-exposed roles (admin → internal employee class outcome as titled); €2000 bounty as reported by author.
- **Conditions / preconditions:** Authenticated user with role-change rights; role APIs returning more role IDs than UI shows; server trusts client-supplied role UUID.
- **Generalized defensive / hunt-planning idea:** Mine Burp history for role/permission enumeration responses that list more IDs than the UI. If role assignment accepts opaque UUIDs, try non-UI values. Diff user counts / new “internal” objects after role swap. Classic: UI allowlist ≠ server allowlist. — Diff/planning framing only; no request recipes.
- **Tags:** IDOR, privilege-escalation, roles, Burp-history, access-control
- **Lane:** Researcher

---

### 11 — When AI Makes 0-Days Feel Like N-Days (STAR Labs)

- **Title:** When AI Makes 0-Days Feel Like N-Days
- **Source URL(s):** https://starlabs.sg/blog/2026/07-when-ai-makes-0-days-feel-like-n-days/
- **Status:** ok
- **Root-cause class:** Kernel `net/sched` use-after-free from **lock mismatch**: lookup under RCU vs free without RCU grace period (“raw free with RCU access”); race windows widened by error-path structure and contending locks; similar pattern class also seen around perf/events.
- **Affected component / surface:** Linux kernel networking traffic-control (`clsact`/`flower` unlocked paths); related subsystems searchable by the same RCU/free mismatch pattern; local LPE-research lab context.
- **Impact:** Kernel UAF / LPE-research class (CVE-2026-53264 tagged in extract); AI accelerates finding siblings of known pattern classes so fresh bugs behave like accelerated n-days.
- **Conditions / preconditions:** Unprivileged user namespaces; CONFIG with clsact/flower unlocked paths; local kernel research lab (**authorized**).
- **Generalized defensive / hunt-planning idea:** AI accelerates discovery of known pattern classes (RCU/UAF lock mismatches) — treat fresh bugs like accelerated n-days. Hunt code that looks up under RCU but frees without grace period. Race reliability comes from window-widening + restructuring to cheaper error paths + isolation of contending locks (analysis of *why* races become reliable — not reproduction steps). Still need deep subsystem judgment for AI blind spots. Pattern search (“raw free with rcu access”) can yield sibling bugs in other subsystems.
- **Tags:** kernel, net/sched, UAF, race, AI-assisted, LPE-research, CVE-2026-53264
- **Lane:** Researcher

---

## Posts (12–23)

### 12 — Crowded login pages vs boring features (@aacle_)

- **Title:** Crowded login pages vs boring features
- **Source URL(s):** https://x.com/aacle_/status/2105641477187817799
- **Status:** ok
- **Root-cause class:** Coverage bias — programs over-test auth entrypoints while utility features (export/PDF, digests, previews) retain classic SSRF/SSTI/IDOR/path issues due to low tester attention.
- **Affected component / surface:** Export/PDF generation; email digests; file preview / filename handling; other low-attention authenticated utilities.
- **Impact:** Findings concentration on under-tested utilities rather than crowded login flows (methodology claim).
- **Conditions / preconditions:** Crowded BB program; authenticated feature access.
- **Generalized defensive / hunt-planning idea:** Prefer features with few testers: Export/PDF → SSRF/SSTI; email digests → IDOR on recipient IDs; file previews → path traversal via filenames. Crowding on auth ≠ coverage of utilities. — Class mapping only; no how-to.
- **Tags:** methodology, SSRF, SSTI, IDOR, path-traversal
- **Lane:** Researcher

---

### 13 — Autonomous bug hunting with PoC confirmation (@crusader_sec)

- **Title:** Autonomous bug hunting with PoC confirmation
- **Source URL(s):** https://x.com/crusader_sec/status/2102646171562909924
- **Status:** ok
- **Root-cause class (process):** Autonomous hunters that triage on hypothesis alone flood queues with false positives; missing mandatory working-PoC confirmation.
- **Affected component / surface:** Agentic hunting pipelines (Crusader alpha framing); triage/validation gate before human review.
- **Impact:** Reduced FP load when confirmed PoC is required before triage (mirrors PageBreak deterministic validation theme).
- **Conditions / preconditions:** Tool access; authorized targets.
- **Generalized defensive / hunt-planning idea:** Require confirmed PoC before triage — mirrors PageBreak deterministic validation theme; reduces FP load. — Process rule only; no PoC contents.
- **Tags:** agentic-AI, validation, PoC
- **Lane:** Researcher

---

### 14 — Multi-model agent swarm → SSRF→RCE→K8s takeover (claimed) (@adnanthekhan)

- **Title:** Multi-model agent swarm → SSRF→RCE→K8s takeover (claimed)
- **Source URL(s):** https://x.com/adnanthekhan/status/2099445532192072048
- **Status:** ok — **Honesty:** Anecdotal claim from post text; **not independently verified** in the extract.
- **Root-cause class (chain pattern, claimed):** Multi-stage trust failures allowing SSRF to reach RCE and then cluster-control planes — plus orchestration that keeps heterogeneous agents on a single long-running goal humans may abandon early.
- **Affected component / surface:** Authorized infra targets; SSRF-reachable internal/metadata paths; Kubernetes control plane (as claimed); multi-agent orchestrator + specialist roles.
- **Impact:** Claimed SSRF → RCE → K8s takeover chain via multi-model swarm (unverified anecdote).
- **Conditions / preconditions:** Authorized infra target; long-running agent budget; orchestrator model.
- **Generalized defensive / hunt-planning idea:** Heterogeneous model swarms with a clear goal (infra takeover/RCE) and long runtime can surface chains humans miss. Skill extension: multi-agent roles (orchestrator + specialists) + chain focus SSRF→cloud metadata/K8s. — Planning pattern only; no chain reproduction.
- **Tags:** agent-swarm, SSRF, RCE, Kubernetes, chaining
- **Lane:** Researcher

---

### 15 — XSS filter-bypass wordlist tip (HTML entity / javascript: URI pattern) (@ethical_h4ck3r_)

- **Title:** XSS filter-bypass wordlist tip (HTML entity / javascript: URI pattern)
- **Source URL(s):** https://x.com/ethical_h4ck3r_/status/2099347683987046887
- **Status:** ok
- **Root-cause class:** Naive blacklist filters that ban literal scheme strings (e.g. `javascript:`) but still accept alternate encodings the browser interprets — **filter/parser mismatch**, not a novel XSS sink class.
- **Affected component / surface:** Reflection into URL/JS contexts protected by naive blacklist filters.
- **Impact:** Filter evasion enabling XSS where literal-string bans were assumed sufficient (class-level; no payload gallery reproduced).
- **Conditions / preconditions:** Reflection into URL/JS contexts with naive blacklist filters.
- **Generalized defensive / hunt-planning idea:** When filters ban `javascript:` literally, test alternate encodings (entities, mixed case, whitespace) that the browser still interprets. Maintain encoding-variant wordlists for URL/scheme sinks — **do not paste live payloads into unauthorized targets.** Prefer mismatch-class catalogs over payload spam. **No wordlist contents or weaponized strings included here.**
- **Tags:** XSS, filter-bypass, wordlist, encoding
- **Lane:** Researcher

---

### 16 — $148k Google Cloud RCE chains — methodology takeaways (@aacle_)

- **Title:** $148k Google Cloud RCE chains — methodology takeaways
- **Source URL(s):** https://x.com/aacle_/status/2099070079010754824
- **Status:** ok
- **Root-cause class:** Multi-backend **residual risk** after partial fixes; **auth ≠ authZ** (project awareness mistaken for ownership); debug/test endpoints left in production.
- **Affected component / surface:** Cloud program multi-backend surfaces; production debug/test endpoints; ownership vs project-membership checks.
- **Impact:** High-value RCE chain class outcomes as claimed by author ($148k framing); residual risk when one backend is fixed and siblings are not.
- **Conditions / preconditions:** Cloud program scope; permission to continue mid-chain (researcher asked Google) under responsible-disclosure norms.
- **Generalized defensive / hunt-planning idea:** A fix on one backend isn’t a fix if siblings remain. Project awareness ≠ ownership checks. Hunt debug/test endpoints left in production. Ethical chaining: pause and get permission before deepening impact.
- **Tags:** cloud, RCE, authZ, regression, responsible-disclosure
- **Lane:** Researcher

---

### 17 — Blind SSRF via header bruteforce + Collaborator (@ethical_h4ck3r_)

- **Title:** Blind SSRF via header bruteforce + Collaborator
- **Source URL(s):** https://x.com/ethical_h4ck3r_/status/2098744915001786871
- **Status:** ok
- **Root-cause class:** Applications honor unexpected or custom HTTP headers that influence outbound fetch/resolve behavior without adequate allowlisting — blind SSRF via **header trust surface**, not only classic `X-Forwarded-*` guesses.
- **Affected component / surface:** HTTP request header handling that can trigger server-side requests; OOB collaborator / callback monitoring.
- **Impact:** Blind SSRF discovery when header-influenced outbound requests hit OOB listeners (class-level).
- **Conditions / preconditions:** Burp Intruder/Collaborator (or similar OOB); request that may honor custom headers. — Tools named as environmental facts only.
- **Generalized defensive / hunt-planning idea:** Bruteforce header names with OOB callback values; pitchfork numerical prefixes; monitor hits with a collaborator aggregator. Systematic header surface for SSRF often beats guessing `X-Forwarded-*` alone. — **Methodology language only; no Intruder payloads, wordlists, or attack scripts reproduced.**
- **Tags:** SSRF, blind-SSRF, Burp, OOB, headers
- **Lane:** Researcher

---

### 18 — Defense Factory playbook — find → validate → verify fixes (@OpenAI)

- **Title:** Defense Factory playbook — find → validate → verify fixes
- **Source URL(s):** https://x.com/OpenAI/status/2097786616311840853
- **Status:** ok
- **Root-cause class (defense process):** Find-only loops without validate and verify-fix phases leave remediations unverified and regressions undetected.
- **Affected component / surface:** Org-scale continuous AI defense loop; human mobilization alongside cyber models.
- **Impact:** Stronger remediation confidence when verify-fix is first-class (defense framing).
- **Conditions / preconditions:** Org-scale cyber models + human mobilization.
- **Generalized defensive / hunt-planning idea:** Same loop as PageBreak/Quarry: agents find → validate → verify fixes hold. Skill extension: add “verify fix” / regression phase as first-class, not optional.
- **Tags:** defense-factory, agentic-AI, validation, regression
- **Lane:** Researcher

---

### 19 — Android APK hunt workflow automation (@dirtycoder0124)

- **Title:** Android APK hunt workflow automation
- **Source URL(s):** https://x.com/dirtycoder0124/status/2097280683924467834
- **Status:** ok
- **Root-cause class (process):** Manual APK triage wastes effort on low-interest components; exported activities and related surfaces benefit from map-and-rank before deep analysis.
- **Affected component / surface:** Android APK/XAPK/ZIP ingest; decompile; exported activities; ADB launch of ranked components; AI applied only after ranking.
- **Impact:** Faster mobile surface triage analogous to web “map & rank then hunt.”
- **Conditions / preconditions:** APK/XAPK/ZIP inputs; decompiler; ADB for exported components.
- **Generalized defensive / hunt-planning idea:** Automate triage: extract main APK, enumerate exported activities, generate ADB launch commands, then apply AI only to ranked interesting components — mirrors web “map & rank then hunt.” — Workflow shape only; no exploit recipes for exported components.
- **Tags:** Android, APK, exported-activities, mobile, AI-assist
- **Lane:** Researcher

---

### 20 — Fully agentized BB workflow (AI → Flounder → Codex report) (@AdamShao)

- **Title:** Fully agentized BB workflow (AI → Flounder → Codex report)
- **Source URL(s):** https://x.com/AdamShao/status/2097111709076910081
- **Status:** ok — **Honesty:** Tone is satirical/boastful; treat as **culture signal**, not a verified case study.
- **Root-cause class (ops trend):** End-to-end agent ownership of recon/find/report without human-in-loop for scope ethics and severity risks shipping unvalidated agent reports.
- **Affected component / surface:** Agent stack spanning target selection, finding, and report drafting; program access.
- **Impact:** Cultural push toward fully agentized BB workflows; quality risk if validation gates are skipped.
- **Conditions / preconditions:** Agent stack + program access.
- **Generalized defensive / hunt-planning idea:** Trend toward agents owning target selection, finding, and report drafting. For skill packs: ensure human-in-loop for scope ethics and severity; don’t ship unvalidated agent reports.
- **Tags:** agentic-AI, workflow, reporting
- **Lane:** Researcher

---

### 21 — Speeding up AD pentests with ADScan and ADPulse (@three_cube)

- **Title:** Speeding up AD pentests with ADScan and ADPulse
- **Source URL(s):** https://x.com/three_cube/status/2096695889259851867
- **Status:** ok
- **Root-cause class (engagement framing):** “DA-or-bust” success metrics miss chainable risks (exposed data, weak configs); repetitive AD checks without automation slow communication of real risk.
- **Affected component / surface:** Authorized Active Directory engagements; baseline automation (ADScan / ADPulse as named tools).
- **Impact:** Faster AD baseline and better risk communication beyond Domain Admin as sole success criterion. Useful contrast to Claude-BugHunter’s deliberate external-only scope.
- **Conditions / preconditions:** Authorized AD engagement.
- **Generalized defensive / hunt-planning idea:** Automate repetitive AD checks; success = identifying/communicating chainable risks (exposed data, weak configs), not only Domain Admin. Useful contrast to Claude-BugHunter’s deliberate external-only scope.
- **Tags:** Active-Directory, automation, pentest-methodology
- **Lane:** Researcher

---

### 22 — XSS regex-bypass payload gallery (@n0aziXss)

- **Title:** XSS regex-bypass payload gallery
- **Source URL(s):** https://x.com/n0aziXss/status/2096524472601768217
- **Status:** ok
- **Root-cause class:** Regex-based WAF/filter **parser mismatch** — filters miss alternate event handlers, `data:` documents, unicode escapes in identifiers, and malformed tags the browser still accepts.
- **Affected component / surface:** HTML sinks guarded by regex-based filters/WAFs.
- **Impact:** XSS where regex filters were assumed sufficient (class-level). **No payload gallery or weaponized strings reproduced.**
- **Conditions / preconditions:** HTML sink with regex-based filter/WAF.
- **Generalized defensive / hunt-planning idea:** Maintain a catalog of parser/WAF mismatch classes (event-handler variety, `data:` documents, unicode in identifiers, malformed tags the browser still accepts). Test methodology: classify filter type → pick mismatch family — **without dumping live weaponized strings into out-of-scope apps.**
- **Tags:** XSS, WAF-bypass, regex, filter-mismatch
- **Lane:** Researcher

---

### 23 — JWT attacks as high-ROI BB class (@zack0x01_)

- **Title:** JWT attacks as high-ROI BB class
- **Source URL(s):** https://x.com/zack0x01_/status/2096216309378027867
- **Status:** ok
- **Root-cause class:** Incomplete JWT verification — weak alg allowlists, asymmetric **key confusion** (accepting signatures verified with the wrong key material), and blind trust of token claims (`aud`/`iss`/role) without server-side authZ.
- **Affected component / surface:** JWT header/alg handling; claim-based authorization (role/admin); apps that accept crafted/modified tokens.
- **Impact:** Auth bypass / privilege escalation when verification is incomplete (header-only changes can escalate). High-ROI BB class per post framing.
- **Conditions / preconditions:** App uses JWT; attacker can craft/modify tokens; weak verification (alg/none, key confusion, missing aud/iss checks) — environmental weakness facts from extract.
- **Generalized defensive / hunt-planning idea:** Always inspect JWT handling: alg allowlists, asymmetric key confusion, claim authZ (role/admin). Header-only changes can escalate if verification is incomplete. Pair with Claude-BugHunter `hunt-jwt-crypto` class skills. — Inspection checklist only; no forge recipes.
- **Tags:** JWT, auth-bypass, privilege-escalation, crypto
- **Lane:** Researcher

---

## Blocked / thin register (from extract)

| # | Status | Primary URL | Reason | Alternate / gap |
|---|--------|-------------|--------|-----------------|
| 03 | blocked | bughunters.google.com/blog/pagebreak-real-world-findings | Sign-in wall | CyberKendra summary (cache poison, signature bypass, Tag Assistant UXSS) |
| 08 | blocked | helpx.adobe.com/.../apsb26-98.html | EdgeSuite Access Denied (403) | HKCERT Sep 2026 + NotCVE APSB26-98 |
| 04 | thin | GitHub NebuSec CVE-2026-52924 folder | No README (404); exploit sources present but unused | Ubuntu/OpenCVE synopsis only |

---

## Cross-cutting patterns (Researcher extract synthesis only)

1. **Validate before report** — PageBreak, Crusader, StrikeAgent, OpenAI Defense Factory, Claude-BugHunter 7-Question Gate.
2. **Regression is first-class** — Quarry + multi-backend “fix isn’t a fix if siblings remain.”
3. **Under-tested utility surfaces** — Export/PDF, digests, previews, debug/test endpoints, header-driven SSRF.
4. **UI allowlist ≠ server allowlist** — Hidden role UUIDs, JWT claim trust, signature sibling endpoints.
5. **Cache & trust-boundary collisions** — Incomplete cache keys, extension message scopes, CDN/shared-static routing.
6. **Agent ops scaffolding** — Attack graphs, Markdown leads, multi-model swarms, ensemble+ML meta-classifiers, skill bundles.
7. **Pattern-class kernel/n-day acceleration** — RCU/free mismatches, protocol rollback UAF; map n-day CVEs (AEM, SCTP) to live fingerprints.
8. **Encoding / filter mismatch catalogs** — Organize by mismatch class, not payload spam — authorized testing only.

---

*Rebuilt 2026-10-02 (Asia/Calcutta) from Researcher lane extract only. No invented findings. No attack procedures or payloads.*
