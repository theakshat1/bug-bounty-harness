# Researcher Lane Extract — 2026-10-02

Bug-bounty knowledge from Researcher lane ONLY (23 items). Educational/authorized methodology. Patterns & hunting ideas only — no exploit PoCs, no weaponized payloads, no step-by-step attacks.

**Counts:** ok=20 · blocked=2 · thin=1

---

## ARTICLES (1–11)

### 1. SubMap.net
- **id:** 1 | **type:** article | **status:** ok
- **source:** https://SubMap.net
- **title:** SubMap — Subdomain Discovery & IP Intelligence Platform
- **vuln_class_technique:** Attack-surface recon; subdomain enum + DNS resolve; subdomain takeover signals; CVE/KEV intel correlation
- **preconditions:** Target org with public DNS/subdomains; optional paid features for auto-resolve + takeover checks
- **generalized_hunting_idea:** Map full subdomain inventory early; cross-reference discovered hosts/products against CVE/KEV feeds; prioritize takeover-prone dangling DNS and unpatched critically scored products before deep app testing.
- **tags:** [recon, subdomain, takeover, CVE-intel, ASM]

### 2. Google PageBreak (blog.google)
- **id:** 2 | **type:** article | **status:** ok
- **source:** https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project/
- **title:** Agentic Hacks, Real Proofs: Inside Google's PageBreak Project
- **vuln_class_technique:** Agentic vuln discovery with deterministic non-AI validators (XSS, SQLi, path traversal, RCE, SSRF); multi-iteration seeded agent runs
- **preconditions:** Running app env for validation; specialized validators per vuln class; source/config access (monorepo-scale helps); auth’d scanning infra
- **generalized_hunting_idea:** Treat LLM hypotheses as untrusted until a separate validator proves impact on a live target. Prefer near-zero-FP pipelines: hypothesize → validate with class-specific oracles → only then report. Unverified candidates seed deeper runs and guide new validator development. Safe-by-design frameworks (eliminate whole bug classes) dramatically shrink findings vs broad codebases. Chain-capable agents benefit from HTTP↔source mapping and repeated identical seeds.
- **tags:** [agentic-AI, validation, XSS, SSRF, SQLi, RCE, PageBreak, false-positives]

### 3. PageBreak real-world findings (Bug Hunters)
- **id:** 3 | **type:** article | **status:** blocked
- **source:** https://bughunters.google.com/blog/pagebreak-real-world-findings
- **title:** PageBreak real-world findings (companion post; primary URL gated)
- **vuln_class_technique:** Cache-key collision → JS cache poisoning; crypto signature bypass via alternate signing endpoint; UXSS via overly-permissive extension messaging
- **preconditions:** Shared CDN/static-cache with incomplete cache key; multi-endpoint signing of attacker-influenced params; browser extension trusting broad origins
- **generalized_hunting_idea:** (Recovered via CyberKendra summary of the gated post.) (1) Audit cache keys for omitted path/query dimensions that let unrelated requests collide and poison shared JS. (2) When an exploit needs a signature, hunt sibling endpoints that will sign attacker-controlled values with the same key. (3) Extension/message-channel trust: any XSS on a broad parent domain can escalate if the extension accepts connections from “any *.google.com”-style scopes without exact sender checks.
- **tags:** [cache-poisoning, XSS, UXSS, signature-bypass, PageBreak]
- **notes:** Original URL returned Google sign-in wall. Ideas from alternate: https://www.cyberkendra.com/2026/09/google-pagebreak-ai-agent-500-xss-flaws.html

### 4. NebuSec CyberMeowfia — Linux CVE-2026-52924
- **id:** 4 | **type:** article | **status:** thin
- **source:** https://github.com/NebuSec/CyberMeowfia/tree/main/security-research/Linux-CVE-2026-52924-ubuntu-7.0.0-28/
- **title:** Linux-CVE-2026-52924-ubuntu-7.0.0-28 (research folder; no README)
- **vuln_class_technique:** Kernel SCTP use-after-free (stale COOKIE-ECHO rollback; freed stream scheduler pointer)
- **preconditions:** Unpatched kernel with SCTP; ability to drive SCTP association state (Stale Cookie ERROR rollback path); Ubuntu 7.0.0-28 class kernels historically listed in folder name
- **generalized_hunting_idea:** Protocol state-machine rollbacks often free tables without invalidating cached pointers or purging queues. Hunt for “rollback/restart” paths that free/rebuild stream or session state but leave scheduler/outqueue caches dangling. Cross-check n-day kernel advisories against still-live distro versions in scope. Do not reuse public exploit trees in unauthorized environments.
- **tags:** [kernel, SCTP, UAF, LPE-research, CVE-2026-52924]
- **notes:** GitHub tree has Makefile/C sources but no README (404). CVE synopsis from Ubuntu/OpenCVE advisories only — exploit source not reviewed or summarized as PoC.

### 5. StrikeAgent_AtkBrain-Flash
- **id:** 5 | **type:** article | **status:** ok
- **source:** https://github.com/Yean-Sec/StrikeAgent_AtkBrain-Flash
- **title:** StrikeAgent_AtkBrain-Flash (Yean-Sec AI pentest agent)
- **vuln_class_technique:** Agentic external foothold hunting; attack-graph self-loop; red-team re-rate + second verification to cut AI FP/inflation
- **preconditions:** Explicit authorization; console + model config; tools on PATH (Docker image includes probe tooling)
- **generalized_hunting_idea:** Structure agent cycles as: hunt → attack graph → re-rate/verify → distill techniques into memory. Prefer “finish a full round before asking human” with interruptible chat. Separate red-team / SRC / CTF modes. Hardening of the hunter platform itself (random entry paths, no leaked /login|/api, replay/bruteforce controls) is itself a checklist for apps you test.
- **tags:** [agentic-AI, red-team, SRC, attack-graph, FP-reduction, authorized-only]

### 6. Claude-BugHunter skills
- **id:** 6 | **type:** article | **status:** ok
- **source:** https://github.com/elementalsouls/Claude-BugHunter/tree/main/skills
- **title:** Claude-BugHunter skill bundle (83 skills; H1-pattern driven)
- **vuln_class_technique:** Per-class hunt skills (XSS, IDOR, SSRF, JWT, OAuth, GraphQL, cache-poison, enterprise VPN/M365/Okta/vCenter, etc.); 7-Question Gate triage; recon→map→hunt→validate→report
- **preconditions:** Authorized BB/pentest scope; Claude Code / compatible harness; optional Burp MCP
- **generalized_hunting_idea:** Codify disclosed-report patterns into auto-loaded per-class skills. Enforce validation gates before submit (scope, impact acceptance, evidence hygiene). Split external surface skills from internal AD/C2 (deliberate OOS). Extend skill packs with: cache-poison, shadow APIs, cloud IAM post-cred, mid-engagement IR detection, regression of “fixed” bugs.
- **tags:** [skills, methodology, triage, hunt-*, enterprise-platform, reporting]

### 7. quarry-vrc
- **id:** 7 | **type:** article | **status:** ok
- **source:** https://github.com/skraft9/quarry-vrc
- **title:** Quarry — agentic BB console with HackerOne integration
- **vuln_class_technique:** Hunt ops platform: H1 sync/submit; regression retest of shipped fixes; Markdown leads as agent memory; advisory/payload FTS
- **preconditions:** Docker host; H1 API token; local-only / allowlisted deployment
- **generalized_hunting_idea:** Treat resolved reports as high-ROI surfaces (new patch code + known PoC context) — queue every fix for regression/bypass. Store leads as plain Markdown so agents can draft/refine without lock-in. Keep H1 as system of record; local DB is cache. Cross-ref CVE feeds against your program assets.
- **tags:** [HackerOne, regression, agentic-ops, leads, advisories]

### 8. Adobe APSB26-98 (AEM)
- **id:** 8 | **type:** article | **status:** blocked
- **source:** https://helpx.adobe.com/security/products/experience-manager/apsb26-98.html
- **title:** APSB26-98 — Security updates for Adobe Experience Manager
- **vuln_class_technique:** AEM privilege escalation; security-feature bypass; stored XSS / incorrect authorization / improper input validation (multi-CVE bulletin; Priority 2)
- **preconditions:** AEM Cloud Service ≤2026.7.0, 6.5 LTS ≤SP2, or 6.5 ≤SP24 in scope
- **generalized_hunting_idea:** (Recovered via HKCERT/NotCVE/search.) On AEM targets, prioritize authZ flaws (CWE-863) and stored XSS in form fields reachable by low-priv users; map bulletin CVEs to version fingerprints. Upgrade path: CS 2026.8.0 / 6.5 LTS SP3 / 6.5 SP25. When primary vendor pages block scrapers, use CERT mirrors + CVE aggregators for scope triage.
- **tags:** [AEM, Adobe, XSS, priv-esc, n-day, APSB26-98]
- **notes:** helpx returned EdgeSuite Access Denied. Alternates: HKCERT Sep 2026 bulletin; NotCVE APSB26-98 (107 CVEs listed, e.g. CVE-2026-19232 Incorrect Authorization CVSS 9.9).

### 9. Local LLM vuln detection research
- **id:** 9 | **type:** article | **status:** ok
- **source:** https://martinativadar.github.io/posts/llm-vulnerability-research.html?v=2
- **title:** Can Local Open-Weight LLMs Detect Vulnerabilities?
- **vuln_class_technique:** Binary vuln classification on functions; multi-prompt ensemble + ML meta-classifier (Chromium dataset)
- **preconditions:** Function + caller/callee/location/pattern context; local LLM capacity; labeled train/test set
- **generalized_hunting_idea:** Single base LLMs ≈ coin-flip (~50–56%). Gains from: richer context (callers, callees, location, code patterns), fine-tuning, multi-view prompts, and a traditional ML model that learns from ensemble agreement/disagreement + metadata (final ~76.9% acc). For skill extension: don’t trust one model vote — ensemble + meta-decision; feed call-graph context not isolated functions.
- **tags:** [LLM, ensemble, static-analysis, Chromium, ML]

### 10. Medium — IDOR to privilege escalation
- **id:** 10 | **type:** article | **status:** ok
- **source:** https://medium.com/@asharm.khan7/2000-bounty-idor-to-privilege-escalation-from-admin-to-internal-employee-a36db23fa10a
- **title:** €2000 Bounty — IDOR to Privilege Escalation: From Admin to Internal Employee
- **vuln_class_technique:** Hidden role UUID IDOR → privilege escalation beyond UI-exposed roles
- **preconditions:** Authenticated user with role-change rights; role APIs returning more role IDs than UI shows; server trusts client-supplied role UUID
- **generalized_hunting_idea:** Mine Burp history for role/permission enumeration responses that list more IDs than the UI. If role assignment accepts opaque UUIDs, try non-UI values. Diff user counts / new “internal” objects after role swap. Classic: UI allowlist ≠ server allowlist.
- **tags:** [IDOR, privilege-escalation, roles, Burp-history, access-control]

### 11. STAR Labs — When AI Makes 0-Days Feel Like N-Days
- **id:** 11 | **type:** article | **status:** ok
- **source:** https://starlabs.sg/blog/2026/07-when-ai-makes-0-days-feel-like-n-days/
- **title:** When AI Makes 0-Days Feel Like N-Days
- **vuln_class_technique:** Kernel net/sched UAF (lock mismatch: RCU lookup vs non-RCU free); race window widening; similar “raw free with RCU access” pattern hunting; perf/events bugs
- **preconditions:** Unprivileged user namespaces; CONFIG with clsact/flower unlocked paths; local kernel research lab (authorized)
- **generalized_hunting_idea:** AI accelerates discovery of known pattern classes (RCU/UAF lock mismatches) — treat fresh bugs like accelerated n-days. Hunt code that looks up under RCU but frees without grace period. Race reliability comes from window-widening + restructuring to cheaper error paths + isolation of contending locks. Still need deep subsystem judgment for AI blind spots. Pattern search (“raw free with rcu access”) can yield sibling bugs in other subsystems.
- **tags:** [kernel, net/sched, UAF, race, AI-assisted, LPE-research, CVE-2026-53264]

---

## POSTS (12–23)

### 12. @aacle_ — under-tested features
- **id:** 12 | **type:** post | **status:** ok
- **source:** https://x.com/aacle_/status/2105641477187817799
- **title:** Crowded login pages vs boring features
- **vuln_class_technique:** Low-attention surface hunting (export/PDF, email digests, file previews)
- **preconditions:** Crowded BB program; authenticated feature access
- **generalized_hunting_idea:** Prefer features with few testers: Export/PDF → SSRF/SSTI; email digests → IDOR on recipient IDs; file previews → path traversal via filenames. Crowding on auth ≠ coverage of utilities.
- **tags:** [methodology, SSRF, SSTI, IDOR, path-traversal]

### 13. @crusader_sec — Crusader alpha
- **id:** 13 | **type:** post | **status:** ok
- **source:** https://x.com/crusader_sec/status/2102646171562909924
- **title:** Autonomous bug hunting with PoC confirmation
- **vuln_class_technique:** Agentic hunting with mandatory working-PoC confirmation
- **preconditions:** Tool access; authorized targets
- **generalized_hunting_idea:** Require confirmed PoC before triage — mirrors PageBreak deterministic validation theme; reduces FP load.
- **tags:** [agentic-AI, validation, PoC]

### 14. @adnanthekhan — agent swarm
- **id:** 14 | **type:** post | **status:** ok
- **source:** https://x.com/adnanthekhan/status/2099445532192072048
- **title:** Multi-model agent swarm → SSRF→RCE→K8s takeover (claimed)
- **vuln_class_technique:** Multi-agent orchestration; SSRF chained to RCE / cluster takeover
- **preconditions:** Authorized infra target; long-running agent budget; orchestrator model
- **generalized_hunting_idea:** Heterogeneous model swarms with a clear goal (infra takeover/RCE) and long runtime can surface chains humans miss. Skill extension: multi-agent roles (orchestrator + specialists) + chain focus SSRF→cloud metadata/K8s.
- **tags:** [agent-swarm, SSRF, RCE, Kubernetes, chaining]
- **notes:** Anecdotal claim from post text; not independently verified here.

### 15. @ethical_h4ck3r_ — XSS wordlist tip
- **id:** 15 | **type:** post | **status:** ok
- **source:** https://x.com/ethical_h4ck3r_/status/2099347683987046887
- **title:** XSS filter-bypass wordlist tip (HTML entity / javascript: URI pattern)
- **vuln_class_technique:** XSS filter evasion via HTML numeric entities in scheme strings
- **preconditions:** Reflection into URL/JS contexts with naive blacklist filters
- **generalized_hunting_idea:** When filters ban `javascript:` literally, test alternate encodings (entities, mixed case, whitespace) that the browser still interprets. Maintain encoding-variant wordlists for URL/scheme sinks — do not paste live payloads into unauthorized targets.
- **tags:** [XSS, filter-bypass, wordlist, encoding]

### 16. @aacle_ — Google Cloud RCE chains lessons
- **id:** 16 | **type:** post | **status:** ok
- **source:** https://x.com/aacle_/status/2099070079010754824
- **title:** $148k Google Cloud RCE chains — methodology takeaways
- **vuln_class_technique:** Multi-backend residual risk; auth≠authZ; debug/test endpoints in prod
- **preconditions:** Cloud program scope; permission to continue mid-chain (researcher asked Google)
- **generalized_hunting_idea:** A fix on one backend isn’t a fix if siblings remain. Project awareness ≠ ownership checks. Hunt debug/test endpoints left in production. Ethical chaining: pause and get permission before deepening impact.
- **tags:** [cloud, RCE, authZ, regression, responsible-disclosure]

### 17. @ethical_h4ck3r_ — Blind SSRF Burp trick
- **id:** 17 | **type:** post | **status:** ok
- **source:** https://x.com/ethical_h4ck3r_/status/2098744915001786871
- **title:** Blind SSRF via header bruteforce + Collaborator
- **vuln_class_technique:** Blind SSRF discovery through header injection + OOB collaborator
- **preconditions:** Burp Intruder/Collaborator (or similar OOB); request that may honor custom headers
- **generalized_hunting_idea:** Bruteforce header names with OOB callback values; pitchfork numerical prefixes; monitor hits with a collaborator aggregator. Systematic header surface for SSRF often beats guessing `X-Forwarded-*` alone.
- **tags:** [SSRF, blind-SSRF, Burp, OOB, headers]

### 18. @OpenAI — Defense Factory
- **id:** 18 | **type:** post | **status:** ok
- **source:** https://x.com/OpenAI/status/2097786616311840853
- **title:** Defense Factory playbook — find → validate → verify fixes
- **vuln_class_technique:** Continuous AI defense loop (find, validate, verify remediation)
- **preconditions:** Org-scale cyber models + human mobilization
- **generalized_hunting_idea:** Same loop as PageBreak/Quarry: agents find → validate → verify fixes hold. Skill extension: add “verify fix” / regression phase as first-class, not optional.
- **tags:** [defense-factory, agentic-AI, validation, regression]

### 19. @dirtycoder0124 — Android hunt app
- **id:** 19 | **type:** post | **status:** ok
- **source:** https://x.com/dirtycoder0124/status/2097280683924467834
- **title:** Android APK hunt workflow automation
- **vuln_class_technique:** Bulk APK ingest → decompile → exported activities → AI on interesting targets
- **preconditions:** APK/XAPK/ZIP inputs; decompiler; ADB for exported components
- **generalized_hunting_idea:** Automate triage: extract main APK, enumerate exported activities, generate ADB launch commands, then apply AI only to ranked interesting components — mirrors web “map & rank then hunt.”
- **tags:** [Android, APK, exported-activities, mobile, AI-assist]

### 20. @AdamShao — 2026 BB workflow meme/claim
- **id:** 20 | **type:** post | **status:** ok
- **source:** https://x.com/AdamShao/status/2097111709076910081
- **title:** Fully agentized BB workflow (AI → Flounder → Codex report)
- **vuln_class_technique:** End-to-end agentized recon/find/report pipeline
- **preconditions:** Agent stack + program access
- **generalized_hunting_idea:** Trend toward agents owning target selection, finding, and report drafting. For skill packs: ensure human-in-loop for scope ethics and severity; don’t ship unvalidated agent reports.
- **tags:** [agentic-AI, workflow, reporting]
- **notes:** Tone is satirical/boastful; treat as culture signal, not verified case study.

### 21. @three_cube — ADScan / ADPulse
- **id:** 21 | **type:** post | **status:** ok
- **source:** https://x.com/three_cube/status/2096695889259851867
- **title:** Speeding up AD pentests with ADScan and ADPulse
- **vuln_class_technique:** AD baseline automation; risk communication over DA-or-bust
- **preconditions:** Authorized AD engagement
- **generalized_hunting_idea:** Automate repetitive AD checks; success = identifying/communicating chainable risks (exposed data, weak configs), not only Domain Admin. Useful contrast to Claude-BugHunter’s deliberate external-only scope.
- **tags:** [Active-Directory, automation, pentest-methodology]

### 22. @n0aziXss — regex bypass XSS snippets
- **id:** 22 | **type:** post | **status:** ok
- **source:** https://x.com/n0aziXss/status/2096524472601768217
- **title:** XSS regex-bypass payload gallery
- **vuln_class_technique:** XSS regex WAF bypass via alternate event handlers, data: URIs, unicode escapes, broken-attribute parsing
- **preconditions:** HTML sink with regex-based filter/WAF
- **generalized_hunting_idea:** Maintain a catalog of parser/WAF mismatch classes (event-handler variety, `data:` documents, unicode in identifiers, malformed tags the browser still accepts). Test methodology: classify filter type → pick mismatch family — without dumping live weaponized strings into out-of-scope apps.
- **tags:** [XSS, WAF-bypass, regex, filter-mismatch]

### 23. @zack0x01_ — JWT underrated
- **id:** 23 | **type:** post | **status:** ok
- **source:** https://x.com/zack0x01_/status/2096216309378027867
- **title:** JWT attacks as high-ROI BB class
- **vuln_class_technique:** JWT header/alg confusion; key confusion (signing with public key); blind trust of token claims
- **preconditions:** App uses JWT; attacker can craft/modify tokens; weak verification (alg/none, key confusion, missing aud/iss checks)
- **generalized_hunting_idea:** Always inspect JWT handling: alg allowlists, asymmetric key confusion, claim authZ (role/admin). Header-only changes can escalate if verification is incomplete. Pair with Claude-BugHunter `hunt-jwt-crypto` class skills.
- **tags:** [JWT, auth-bypass, privilege-escalation, crypto]

---

## BLOCKED

| # | URL | Reason | Alternate tried |
|---|-----|--------|-----------------|
| 3 | https://bughunters.google.com/blog/pagebreak-real-world-findings | Sign-in wall (Google login gate) | CyberKendra summary of companion findings (cache poison, signature bypass, Tag Assistant UXSS) |
| 8 | https://helpx.adobe.com/security/products/experience-manager/apsb26-98.html | EdgeSuite Access Denied (403) | WebSearch + HKCERT Sep 2026 bulletin + NotCVE APSB26-98 |

**Thin (not fully blocked):**
| 4 | GitHub CVE-2026-52924 research folder | No README (404); tree lists exploit sources only | Ubuntu/OpenCVE CVE synopsis (SCTP UAF); exploit sources not used for PoC extraction |

---

## SYNTHESIS — cross-cutting patterns for skill extension

1. **Validate before report** — PageBreak, Crusader, StrikeAgent, OpenAI Defense Factory, Claude-BugHunter’s 7-Question Gate: LLM hypotheses are noise until live oracles / second verification prove impact.
2. **Regression is a first-class hunt** — Quarry regression tab + aacle_ “fix isn’t a fix if another backend still vulnerable”: retest shipped patches and sibling backends.
3. **Under-tested utility surfaces** — Export/PDF, digests, previews, debug/test endpoints, header-driven SSRF: leave login page to the crowd.
4. **UI allowlist ≠ server allowlist** — Hidden role UUIDs (IDOR→PE), JWT header trust, signature endpoints that sign attacker values: always diff UI options vs API enumerations.
5. **Cache & trust-boundary collisions** — Incomplete cache keys (JS poison), extension message scopes, CDN/shared-static routing: design mistakes that agents uniquely chain.
6. **Agent ops scaffolding** — Attack graphs, Markdown leads, multi-model swarms, ensemble+ML meta-classifiers, skill bundles from disclosed reports — memory + routing beat one-shot prompts.
7. **Pattern-class kernel/n-day acceleration** — AI finds “raw free under RCU” / protocol rollback UAF families fast; humans still own race hardening and subsystem judgment; map n-day CVEs (AEM, SCTP) to live asset fingerprints.
8. **Encoding / filter mismatch catalogs** — XSS and SSRF wordlists should be organized by *mismatch class* (entity encoding, regex gaps, header name space), not payload spam — for authorized testing only.

---

*Extracted 2026-10-02 (Asia/Calcutta). Researcher lane only. No invented findings.*
