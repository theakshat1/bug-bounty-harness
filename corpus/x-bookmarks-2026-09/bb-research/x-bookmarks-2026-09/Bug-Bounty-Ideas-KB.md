# Bug Bounty Ideas Knowledge Base

**Audience:** Akshat (authorized / in-scope hunting only)  
**Scope:** Methodology and reusable idea patterns — **no** exploit recipes, payloads, PoCs, or reproduction steps.  
**Merged:** 2026-10-02 (Asia/Calcutta) from three exclusive X-bookmark extract lanes.  
**Constraint:** Built only from lane extracts; original article URLs were not re-scraped.

---

## High-diversity reusable patterns

Generalized hunting ideas you can reuse across targets (abstract / defensive framing):

- **Validate before report.** Treat LLM or scanner hypotheses as untrusted until a separate oracle, second agent, or live impact check proves them (PageBreak, Cloudflare audit skill, Crusader, StrikeAgent, Jenny hallucination→promote, Xalgorix detect-then-prove, OpenAI Defense Factory, Claude-BugHunter 7-Question Gate).
- **UI allowlist ≠ server allowlist.** Diff what the UI exposes vs what APIs enumerate (hidden role UUIDs, JWT claims, signature sibling endpoints, dead `/api|/admin` routes in JS).
- **JS / sourcemap recon as surface map.** Harvest bundles and source maps for hidden domains, full route maps, Cognito/AWS client config, and object IDs that pivot into IDOR/BOLA.
- **Authz at every entrypoint.** Internal library wrappers, filter-vs-dispatcher path normalization, and caller trust boundaries often miss one path.
- **Regression is first-class.** Retest shipped fixes, sibling backends, and the same bug class after vendor patches (Quarry, Google Cloud multi-backend lessons, Papercut-style n-day sweeps).
- **Under-tested utility surfaces.** Prefer export/PDF, email digests, file previews, debug/test endpoints, and header-driven SSRF over crowded login pages.
- **Multi-tenant isolation beyond results.** Query text, metadata, blob versions, and shared analytics often leak across tenants when only result sets are gated.
- **Filter mismatch catalogs, not payload spam.** Organize XSS/SSRF/path tests by mismatch class (encoding depth, strip order, truncation, entity/scheme variants, header namespace).
- **Orchestration > model choice.** Scoped stages, coverage ledgers, adversarial disprove verifiers, call-graph context compression, and token budgets beat dumping whole repos into prompts.
- **Program intel + ROI.** Prioritize by public payout/activity signals; track token burn vs bounty outcome; feed negatives into RAG so campaigns skip hardened dead-ends.
- **PoC hygiene for takeovers.** Minimal public proof surface; evidence in private report; platform handle to deter claim-theft.
- **Codify past wins into skills.** Turn personal IDOR/authz lessons into reusable agent skills pointed at live JS/API surfaces.

---

## Cluster index

1. [IDOR / BOLA / Authorization mismatches](#1-idor--bola--authorization-mismatches)
2. [JS / Sourcemap recon & client secrets](#2-js--sourcemap-recon--client-secrets)
3. [Cloud / Multi-tenant / Storage misconfig](#3-cloud--multi-tenant--storage-misconfig)
4. [LLM & agent hunting process](#4-llm--agent-hunting-process)
5. [MCP / Agent tooling meta](#5-mcp--agent-tooling-meta)
6. [Path normalization / Password-reset / Filter mismatches](#6-path-normalization--password-reset--filter-mismatches)
7. [XSS / Encoding / WAF filter catalogs](#7-xss--encoding--waf-filter-catalogs)
8. [SSRF / Header trust / 403 bypass](#8-ssrf--header-trust--403-bypass)
9. [Classic recon → hunt workflows](#9-classic-recon--hunt-workflows)
10. [N-day / Patch-diff / Kernel & enterprise patterns](#10-n-day--patch-diff--kernel--enterprise-patterns)
11. [Web3 audit corpora](#11-web3-audit-corpora)
12. [PoC hygiene & responsible disclosure](#12-poc-hygiene--responsible-disclosure)
13. [Program intel / Prioritization / Ops](#13-program-intel--prioritization--ops)
14. [Thin / Outcome-only / Tangential](#14-thin--outcome-only--tangential)

---

## 1. IDOR / BOLA / Authorization mismatches

### 1.1 Hidden role UUID IDOR → privilege escalation
- **Vuln class / technique:** Hidden role UUID IDOR → privilege escalation beyond UI-exposed roles
- **Preconditions:** Authenticated user with role-change rights; role APIs return more IDs than UI; server trusts client-supplied role UUID
- **Generalized hunting idea:** Mine proxy history for role/permission enumerations that list more IDs than the UI. If role assignment accepts opaque UUIDs, try non-UI values. Diff user counts / new “internal” objects after role swap. Classic: UI allowlist ≠ server allowlist.
- **Tags:** IDOR, privilege-escalation, roles, Burp-history, access-control
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://medium.com/@asharm.khan7/2000-bounty-idor-to-privilege-escalation-from-admin-to-internal-employee-a36db23fa10a

### 1.2 JS graveyard endpoints → authz differentials
- **Vuln class / technique:** Dead/historical frontend routes → IDOR/BOLA / broken auth / forgotten admin
- **Preconditions:** Readable JS bundles; authenticated and unauthenticated test accounts preferred
- **Generalized hunting idea:** Mine historical frontend bundles for `/api|/admin|/internal` routes the UI no longer links, validate reachability, then focus authorization differentials rather than status-code alone.
- **Tags:** JS-recon, dead-endpoints, IDOR, BOLA, API
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://x.com/whotfbunny/status/2098862073057038746

### 1.3 Sourcemap / JS → UUID pivot → IDOR on ticket/ops domains
- **Vuln class / technique:** IDOR / BOLA; JS/sourcemap recon leading to hidden API surface
- **Preconditions:** In-scope org assets including ticket/management hosts referenced from JS; ability to harvest JS/source maps; public or weakly gated endpoints that reveal object IDs
- **Generalized hunting idea:** After subdomain enum, recursively harvest JS and source maps for hidden domains and full API route maps; when a “public” endpoint leaks object IDs (UUIDs), cross-check other routes that take the same ID for missing authz. Expand surface to org-managed ticket/ops domains that may still be in bounty scope.
- **Tags:** idor, bola, js-recon, sourcemaps, api-enumeration, pii
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://medium.com/@4osp3l/leaking-mtn-customer-pii-order-history-via-idor-on-a-ticket-management-domain-cd3306e36e29?postPublishedType=initial

### 1.4 Report-trained IDOR agent skill + live JS analysis
- **Vuln class / technique:** IDOR / BOLA via reusable skill + client-side JS analysis
- **Preconditions:** Prior personal reports as training material; target exposes JS API shapes; low-priv session available
- **Generalized hunting idea:** Codify past IDOR lessons into a reusable agent skill (rules, bypass notes, training docs), then point it at live JS/API surfaces. Especially check list/search endpoints that return other users’ PII/RBAC metadata under a low-priv session while anon correctly 403s.
- **Tags:** IDOR, BOLA, JS-analysis, AI-skill, access-control
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://x.com/unknown0x3a/status/2096959661446746168

### 1.5 Internal library wrapper missing caller authz
- **Vuln class / technique:** Broken authorization / internal API privilege boundary
- **Preconditions:** Access to in-scope surfaces with internal library wrappers around storage/filesystem APIs
- **Generalized hunting idea:** When an internal library wraps storage/filesystem APIs, test whether caller authz is enforced at every entrypoint—or whether a lower-trust API path can reach higher-trust file operations.
- **Tags:** authorization, internal-API, Google-VRP
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://x.com/GoogleVRP/status/2099890989775093810

### 1.6 JWT header / alg / claim trust gaps
- **Vuln class / technique:** JWT alg confusion; key confusion; blind trust of token claims
- **Preconditions:** App uses JWT; attacker can craft/modify tokens; weak verification (alg allowlists, key confusion, missing aud/iss)
- **Generalized hunting idea:** Always inspect JWT handling: alg allowlists, asymmetric key confusion, claim authZ (role/admin). Header-only changes can escalate if verification is incomplete. Pair with per-class JWT hunt skills.
- **Tags:** JWT, auth-bypass, privilege-escalation, crypto
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://x.com/zack0x01_/status/2096216309378027867

### 1.7 Auth ≠ authZ; sibling backends; debug endpoints in prod
- **Vuln class / technique:** Multi-backend residual risk; project awareness ≠ ownership; debug/test endpoints left in production
- **Preconditions:** Cloud/program scope; permission to continue mid-chain under responsible disclosure norms
- **Generalized hunting idea:** A fix on one backend isn’t a fix if siblings remain. Project awareness ≠ ownership checks. Hunt debug/test endpoints left in production. Ethical chaining: pause and get permission before deepening impact.
- **Tags:** cloud, RCE, authZ, regression, responsible-disclosure
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://x.com/aacle_/status/2099070079010754824

---

## 2. JS / Sourcemap recon & client secrets

### 2.1 Secret hunting by key *names* near assignments
- **Vuln class / technique:** Static secret / credential pattern matching
- **Preconditions:** Readable source, configs, CI env dumps, JS bundles, or public repos in scope
- **Generalized hunting idea:** Hunt leaked credentials by matching high-signal key *names* (api_key, aws_secret, client_secret, etc.) near assignment operators rather than only known token formats. Broad name-based regexes catch misnamed or vendor-specific secrets that format-only detectors miss; combine with entropy/format validators and rotate-on-find hygiene.
- **Tags:** secrets, regex, credential-leak, recon, static-analysis
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://gist.github.com/h4x0r-dz/be69c7533075ab0d3f0c9b97f7c93a59

### 2.2 Cognito / Identity Pool client config in JS & source maps
- **Vuln class / technique:** Client-side secret exposure; Cognito User/Identity Pool misconfiguration → temporary cloud credentials
- **Preconditions:** JS bundles (esp. source maps) exposing Cognito pool/client/identity IDs; flows that allow signup/auth with usable IAM roles; authorized testing
- **Generalized hunting idea:** On SPA/dev subdomains, mine JS and reconstructed source maps for cloud identity config. Assess whether exposed client config plus open signup/auth can obtain temporary cloud credentials and what IAM permissions those roles grant—report exposure and over-permissioned identity pools; do not use obtained access beyond authorized proof. Repeat across sibling subdomains.
- **Tags:** aws, cognito, js-secrets, sourcemaps, credential-exposure, misconfiguration
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://medium.com/@mohameddiv77/how-i-got-aws-secret-keys-from-exposed-variables-in-js-file-c67f61039da6

---

## 3. Cloud / Multi-tenant / Storage misconfig

### 3.1 Google dork → S3 listing + unsigned object serve
- **Vuln class / technique:** Cloud storage misconfiguration / sensitive data exposure via public listing + unsigned object serving
- **Preconditions:** In-scope web app using object storage; indexed public files revealing bucket naming; authorized probe of listing/ACL
- **Generalized hunting idea:** Start large scopes with lightweight dorks for indexed PDFs/uploads to surface CDN/S3 path patterns. When path segments look like bucket names, check whether listing is open and whether the app’s download/API path serves objects without time-limited signed URLs or auth. Chain: public listing (filename oracle) + unauthenticated content fetch. Prefer signed URLs, least-privilege bucket policies, and separate sensitive exports from public assets.
- **Tags:** s3, misconfiguration, google-dork, sensitive-data, cloud
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://medium.com/@Seek404/when-a-simple-google-dork-led-to-an-s3-misconfiguration-and-sensitive-data-exposure-4d7d86f54b16

### 3.2 Multi-tenant query/analytics isolation (metadata & query text)
- **Vuln class / technique:** Cloud multi-tenant isolation failure (shared analytics/query services)
- **Preconditions:** Authorized cloud research scope; shared analytics/query platforms
- **Generalized hunting idea:** For multi-tenant query/analytics platforms, test whether tenant boundaries apply to metadata and query text (INSERT/WHERE values), not only result sets—cross-customer isolation bugs often hide in secondary surfaces.
- **Tags:** AWS, Athena, multi-tenant, data-exfiltration, cloud
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://x.com/orenyomtov/status/2097366728321749080

### 3.3 Azure / Entra residue & vault loot paths
- **Vuln class / technique:** Azure / Entra recon and secret residue hunting
- **Preconditions:** Authorized Azure assessment scope
- **Generalized hunting idea:** Approach Azure holistically: unauthenticated blob/version residue checks, external Entra/tenant recon, then conditional-access/role/grant enum and vault/app/AKS loot paths—old storage versions often retain secrets.
- **Tags:** Azure, Entra, blob, Key-Vault, BloodHound
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://x.com/Hac10101/status/2097134370775818604

---

## 4. LLM & agent hunting process

### 4.1 Orchestration layer over raw model choice (recon→hunt→validate→trace→report)
- **Vuln class / technique:** LLM orchestration / AI security research harness design
- **Preconditions:** Coding agents + optional MCPs; authorized codebase/binary targets; ability to stage prompts and artefacts
- **Generalized hunting idea:** Invest in the orchestration layer more than raw model choice: split work into recon→hunt→validate→trace→report with per-stage prompts and structured artefacts; give each stage only scoped context; use adversarial/validate agents that try to disprove findings; route cheap models for classify/summarize and strong models for validation/trace; add RAG memory of prior notes and a post-run feedback loop. Context budget discipline beats dumping full repos into prompts.
- **Tags:** llm-harness, orchestration, validation-gates, rag, token-budget
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://blog.zsec.uk/harnessing-harnesses/

### 4.2 MCP-wrapped campaigns with hallucination→validated promotion
- **Vuln class / technique:** LLM/MCP-orchestrated vuln hunting; grammar-based fuzzing; patch-diff campaigns (methodology)
- **Preconditions:** Isolated research lab; MCP-wrapped RE/fuzz/debug/reporting tools; human validation gates before disclosure
- **Generalized hunting idea:** Wrap the research toolchain as MCP tools, organize work as campaigns, force every LLM finding through a hallucination→validated promotion pipeline (existence, clean-snapshot reproduce, exploitability, low-priv reachability), and feed crashes/defenses/bounty ROI back into RAG so later hunts skip hardened dead-ends and favor under-scrutinized high-ROI targets.
- **Tags:** mcp, autonomous-hunting, hallucination-gates, rag-feedback, patch-diff, bounty-roi
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://blog.zsec.uk/bullyingllms/

### 4.3 Minimal threat-model scaffolding (avoid context rot)
- **Vuln class / technique:** LLM-assisted code audit methodology; authz/JWT/CI slice hunting (pattern-level)
- **Preconditions:** Readable target source; prior CVE/advisory history or architectural threat model; verifier loop
- **Generalized hunting idea:** Avoid bloated AGENT.md scaffolds and “find all vulns” prompts (context rot). Use minimal scaffolding: derive a one-page threat model from past CVEs and trust boundaries, audit thin slices (auth, JWT, cookies, sandbox egress), demand call-chain evidence, and spend most tokens on slice exploration + verification—not prompt bureaucracy.
- **Tags:** llm-audit, threat-model, context-rot, minimal-scaffolding, authz, jwt
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://devansh.bearblog.dev/needle-in-the-haystack/

### 4.4 Coverage-led AI code audit with adversarial disprove verifiers
- **Vuln class / technique:** Coverage-led AI code audit / adversarial finding verification
- **Preconditions:** Coding agent with tool-use + parallel sub-agents; sandbox for any target-code execution
- **Generalized hunting idea:** Run audits as gated phases: recon → architecture + coverage ledger → coverage-led hunting with isolated hunters + critics → fresh verifiers that try to *disprove* candidates → structured findings → independent re-verification → target-neutral reports. Confirm only established boundary failures with source traces; severity needs impact. Repeat runs are additive against the ledger.
- **Tags:** cloudflare, agent-skill, code-audit, coverage-ledger, adversarial-validation
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://github.com/cloudflare/security-audit-skill

### 4.5 PageBreak: deterministic non-AI validators for agent hypotheses
- **Vuln class / technique:** Agentic vuln discovery with class-specific validators; multi-iteration seeded agent runs
- **Preconditions:** Running app env for validation; specialized validators per vuln class; authorized scanning infra
- **Generalized hunting idea:** Treat LLM hypotheses as untrusted until a separate validator proves impact on a live target. Prefer near-zero-FP pipelines: hypothesize → validate with class-specific oracles → only then report. Unverified candidates seed deeper runs. Safe-by-design frameworks shrink findings vs broad codebases. Chain-capable agents benefit from HTTP↔source mapping and repeated identical seeds.
- **Tags:** agentic-AI, validation, PageBreak, false-positives
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project/

### 4.6 PageBreak real-world finding themes (cache / signature / UXSS)
- **Vuln class / technique:** Cache-key collision → JS cache poisoning; crypto signature bypass via alternate signing endpoint; UXSS via overly-permissive extension messaging
- **Preconditions:** Shared CDN/static-cache with incomplete cache key; multi-endpoint signing of attacker-influenced params; browser extension trusting broad origins
- **Generalized hunting idea:** (1) Audit cache keys for omitted path/query dimensions that let unrelated requests collide and poison shared JS. (2) When an exploit needs a signature, hunt sibling endpoints that will sign attacker-controlled values with the same key. (3) Extension/message-channel trust: XSS on a broad parent domain can escalate if the extension accepts connections from wide scopes without exact sender checks.
- **Tags:** cache-poisoning, XSS, UXSS, signature-bypass, PageBreak
- **Lane provenance:** Researcher
- **Quality:** blocked-recovered (primary Google Bug Hunters URL sign-in gated; ideas recovered via CyberKendra summary)
- **Sources:** https://bughunters.google.com/blog/pagebreak-real-world-findings · alternate https://www.cyberkendra.com/2026/09/google-pagebreak-ai-agent-500-xss-flaws.html

### 4.7 StrikeAgent: hunt → attack graph → re-rate/verify → memory
- **Vuln class / technique:** Agentic external foothold hunting; attack-graph self-loop; red-team re-rate + second verification
- **Preconditions:** Explicit authorization; console + model config; tools on PATH
- **Generalized hunting idea:** Structure agent cycles as: hunt → attack graph → re-rate/verify → distill techniques into memory. Prefer “finish a full round before asking human” with interruptible chat. Separate red-team / SRC / CTF modes. Hardening of the hunter platform itself (no leaked `/login|/api`, replay/bruteforce controls) is itself a checklist for apps you test.
- **Tags:** agentic-AI, red-team, attack-graph, FP-reduction, authorized-only
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://github.com/Yean-Sec/StrikeAgent_AtkBrain-Flash

### 4.8 Claude-BugHunter: per-class skills + 7-Question Gate
- **Vuln class / technique:** Per-class hunt skills; triage gate; recon→map→hunt→validate→report
- **Preconditions:** Authorized BB/pentest scope; compatible harness; optional Burp MCP
- **Generalized hunting idea:** Codify disclosed-report patterns into auto-loaded per-class skills. Enforce validation gates before submit (scope, impact acceptance, evidence hygiene). Split external surface skills from internal AD/C2 (deliberate OOS). Extend skill packs with: cache-poison, shadow APIs, cloud IAM post-cred, mid-engagement IR detection, regression of “fixed” bugs.
- **Tags:** skills, methodology, triage, enterprise-platform, reporting
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://github.com/elementalsouls/Claude-BugHunter/tree/main/skills

### 4.9 Quarry: H1 sync + regression retest of shipped fixes
- **Vuln class / technique:** Hunt ops platform; regression retest; Markdown leads as agent memory
- **Preconditions:** Docker host; H1 API token; local-only / allowlisted deployment
- **Generalized hunting idea:** Treat resolved reports as high-ROI surfaces (new patch code + known context) — queue every fix for regression/bypass. Store leads as plain Markdown so agents can draft/refine without lock-in. Keep H1 as system of record; local DB is cache. Cross-ref CVE feeds against program assets.
- **Tags:** HackerOne, regression, agentic-ops, leads, advisories
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://github.com/skraft9/quarry-vrc

### 4.10 Detect-then-prove autonomous scanner pattern (Xalgorix)
- **Vuln class / technique:** Autonomous AI pentest tooling with independent verification loop
- **Preconditions:** Self-hosted environment; BYO-LLM; authorized scope
- **Generalized hunting idea:** Prefer scanners/agents that separate “detect” from “prove”: an autonomous hunter plus an independent verifier that re-checks findings before reporting reduces false-positive triage load.
- **Tags:** AI-pentester, tooling, verification, false-positives
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://x.com/bountywriteups/status/2099143734369690104

### 4.11 Mandatory working-PoC confirmation before triage (Crusader)
- **Vuln class / technique:** Agentic hunting with mandatory confirmed-impact gate
- **Preconditions:** Tool access; authorized targets
- **Generalized hunting idea:** Require confirmed impact evidence before triage — mirrors PageBreak deterministic validation; reduces FP load.
- **Tags:** agentic-AI, validation
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://x.com/crusader_sec/status/2102646171562909924

### 4.12 Continuous find → validate → verify-fixes loop (Defense Factory)
- **Vuln class / technique:** Continuous AI defense loop
- **Preconditions:** Org-scale cyber models + human mobilization
- **Generalized hunting idea:** Same loop as PageBreak/Quarry: agents find → validate → verify fixes hold. Add “verify fix” / regression phase as first-class, not optional.
- **Tags:** defense-factory, agentic-AI, validation, regression
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://x.com/OpenAI/status/2097786616311840853

### 4.13 Multi-program orchestration needs triage quality
- **Vuln class / technique:** Multi-program automated hunting orchestration
- **Preconditions:** Authorized programs; compute for parallel agent runs; triage capacity for duplicates
- **Generalized hunting idea:** Orchestrate parallel hunt agents across several programs, then invest in dedupe/triage quality—scale helps only if duplicate rate and false positives are managed.
- **Tags:** automation, orchestration
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://x.com/adnanthekhan/status/2099136955250352428

### 4.14 Heterogeneous model swarms for chain focus (anecdotal)
- **Vuln class / technique:** Multi-agent orchestration; SSRF chained toward infra impact (claimed)
- **Preconditions:** Authorized infra target; long-running agent budget; orchestrator model
- **Generalized hunting idea:** Heterogeneous model swarms with a clear goal and long runtime can surface chains humans miss. Skill extension: multi-agent roles (orchestrator + specialists) + chain focus toward cloud metadata/K8s-class impact. **Note:** anecdotal claim from post text; not independently verified in lane.
- **Tags:** agent-swarm, SSRF, RCE, Kubernetes, chaining
- **Lane provenance:** Researcher
- **Quality:** ok (anecdotal)
- **Sources:** https://x.com/adnanthekhan/status/2099445532192072048

### 4.15 Agentic ROI: token burn vs bounty outcome
- **Vuln class / technique:** Economics of autonomous exploit agents
- **Preconditions:** Interest in agentic hunting ROI
- **Generalized hunting idea:** When evaluating autonomous exploit agents, track token/cost burn against bounty outcome—technical success can still be negative ROI.
- **Tags:** agentic-hunting, ROI
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://x.com/payloadartist/status/2098056402954580039

### 4.16 Cyber-tuned LLM APIs as analysis aids (Adverserial / CyberKimi)
- **Vuln class / technique:** AI-assisted security workflows / offensive-tuned LLM API integration
- **Preconditions:** Prepaid wallet / API key; client that speaks OpenAI or Anthropic dialect
- **Generalized hunting idea:** Wire a security-specialized model into existing agent/CLI harnesses via a shim base URL rather than rebuilding tooling. Use model routing (cheap classify/summarize vs strong deep analysis). Treat cyber-tuned models as assistants for triage, rule drafting, IR/threat-hunt hypotheses, and code review inside authorized scopes—not as autonomous exploit engines. Keep secrets out of client-side/shared images; verify vendor eval claims independently.
- **Tags:** llm, cyberkimi, api, agent-tooling, detection-engineering, privacy
- **Lane provenance:** Researchy | Deep Research *(deduped)*
- **Quality:** ok
- **Sources:** https://adverserial.ai/docs.html · https://adverserial.ai

### 4.17 Local LLM ensemble + ML meta-classifier for vuln classification
- **Vuln class / technique:** Binary vuln classification on functions; multi-prompt ensemble + ML meta-classifier
- **Preconditions:** Function + caller/callee/location/pattern context; local LLM capacity; labeled train/test set
- **Generalized hunting idea:** Single base LLMs ≈ coin-flip. Gains from richer context (callers, callees, location, code patterns), fine-tuning, multi-view prompts, and a traditional ML model that learns from ensemble agreement/disagreement + metadata. Don’t trust one model vote — ensemble + meta-decision; feed call-graph context not isolated functions.
- **Tags:** LLM, ensemble, static-analysis, ML
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://martinativadar.github.io/posts/llm-vulnerability-research.html?v=2

### 4.18 Local security-tuned models need human verify + scope
- **Vuln class / technique:** Local cyber-offense LLM for vuln discovery (tooling)
- **Preconditions:** Hardware for large MoE; authorized use only
- **Generalized hunting idea:** Local security-tuned models can assist recon/hypotheses, but findings still need human verification and must stay within authorized scope—benchmarks ≠ production validity.
- **Tags:** LLM, local-models, tooling
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://x.com/0x0SojalSec/status/2096639626706649149

### 4.19 Calibrate harnesses via public offensive-AI benchmarks
- **Vuln class / technique:** Offensive-AI / automated red-team agent capability benchmarking
- **Preconditions:** Public SPA/API access; agents submitted under platform rules
- **Generalized hunting idea:** Use public offensive-AI benchmarks (Tsecbench, related XBOW/Cybench sets) to compare agent harnesses across capability domains rather than chasing single demos. Track leaderboard + cheat-disclosures to calibrate which multi-agent strategies generalize; treat benchmarks as evaluation of hunting workflows, not attack manuals.
- **Tags:** tsecbench, benchmark, offensive-ai, leaderboard, agentic
- **Lane provenance:** Researchy
- **Quality:** ok (SPA empty via WebFetch; recovered via API)
- **Sources:** https://tsecbench.zc.tencent.com/#leaderboard

### 4.20 Proxy agentic CLIs to cheaper backends
- **Vuln class / technique:** Agentic coding CLI routing (tooling economics)
- **Preconditions:** Desire to run coding CLIs against alternate model backends
- **Generalized hunting idea:** Proxy agentic coding CLIs to free/local model backends to lower iteration cost for research tooling—orthogonal to vuln classes but affects hunt throughput.
- **Tags:** Claude-Code, proxy, local-LLM, tooling
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://x.com/7h3h4ckv157/status/2096488638456717430

### 4.21 Fully agentized BB workflow culture signal
- **Vuln class / technique:** End-to-end agentized recon/find/report pipeline
- **Preconditions:** Agent stack + program access
- **Generalized hunting idea:** Trend toward agents owning target selection, finding, and report drafting. Ensure human-in-loop for scope ethics and severity; don’t ship unvalidated agent reports. **Note:** tone in source is satirical/boastful; treat as culture signal, not verified case study.
- **Tags:** agentic-AI, workflow, reporting
- **Lane provenance:** Researcher
- **Quality:** ok (culture signal)
- **Sources:** https://x.com/AdamShao/status/2097111709076910081

### 4.22 Immunefi-style process interviews over tool hype
- **Vuln class / technique:** Research methodology / AI-assisted hunting (career + process)
- **Preconditions:** Active program access; willingness to systematize hunting with AI as force multiplier
- **Generalized hunting idea:** Study high-earning researchers’ process: how they onboard to a program, where AI helps surface candidates, and how they validate/report. Prefer methodology interviews over tool hype; treat AI as triage and pattern-matching aid that still needs human confirmation of impact.
- **Tags:** methodology, AI-assisted-hunting, immunefi, career
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://x.com/immunefi/status/2102010814442181024

### 4.23 LLM-assisted code-audit patterns (batch desync, sanitizer gaps, privilege gadgets)
- **Vuln class / technique:** LLM-assisted 0-day discovery; batch-API validate/execute desync; type-confused sanitization; privilege-escalation gadget chaining (patterns only)
- **Preconditions:** Authorized source-code audit; multi-agent coding model; hard constraints (pre-auth, default config, no fabricated preconditions)
- **Generalized hunting idea:** Orchestrate multi-agent code audits with diverse approach portfolios, adversarial double-checks, and hard constraints. High-level bug patterns to hunt—without reproducing PoCs: (1) APIs that validate in one loop and execute in another can desync when error paths push only one of two parallel arrays; (2) sinks that sanitize arrays but pass scalars through unsanitized; (3) nested/self-calls of batch endpoints that inherit broken validation assumptions; (4) after a read primitive, in-memory object caches + features that reconcile cache vs DB can become escalation gadgets; (5) temporary identity switches driven by attacker-influenced structured records; (6) dynamically named hooks/actions built from status×type strings. Meta: as models do more chain-building, human value shifts to target selection, prompt heuristics, and steering.
- **Tags:** wordpress, llm-research, batch-api, desync, gadget-chain, agentic
- **Lane provenance:** Researchy
- **Quality:** ok (methodology only; PoCs stripped at extract)
- **Sources:** https://slcyber.io/research-center/exploit-brokers-pay-500000-for-a-wordpress-rce-i-found-one-with-gpt5-6/

---

## 5. MCP / Agent tooling meta

### 5.1 OWASP MCP Security Taxonomy
- **Vuln class / technique:** n/a-meta (shared vocabulary for MCP threat modeling)
- **Preconditions:** Building, reviewing, or threat-modeling MCP hosts/clients/servers/gateways
- **Generalized hunting idea:** Use a vendor-neutral MCP risk taxonomy (relationship map, OWASP MCP Top 10 mapping, root-cause tags like INJ-CMD/SSRF/AUTH-BYPASS/X-TENANT) to structure reviews of agent tools, transport, and backend trust boundaries instead of ad-hoc checklists.
- **Tags:** owasp, mcp, taxonomy, threat-modeling, ai-security
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://github.com/OWASP/MCP-Taxonomy

### 5.2 Ripwire: call-graph / blast-radius before dumping context
- **Vuln class / technique:** Agent context compression / blast-radius & quality-delta tooling
- **Preconditions:** Local repo; optional MCP/agent skill install
- **Generalized hunting idea:** Before agents dump whole files into context, give them a ranked deterministic map: callers/callees, edit blast radius, tests-to-run, quality deltas, forgotten co-changes—using signatures far smaller than bodies. For multi-agent audits, lead with orientation/recall and close with edit-check + quality gates.
- **Tags:** ripwire, mcp, call-graph, context-compression, multi-agent
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://github.com/redhat-et/ripwire

### 5.3 Awesome Agent Orchestrators catalog
- **Vuln class / technique:** n/a-tooling (harness selection meta)
- **Preconditions:** Need to run/supervise multiple coding or research agents
- **Generalized hunting idea:** Curated catalog of agent orchestrators helps researchers pick harnesses for multi-agent security workflows—isolation via worktrees/sandboxes, verification gates, and human approval inboxes matter more than raw agent count.
- **Tags:** awesome-list, agent-orchestrators, multi-agent, harness, tooling
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://github.com/andyrewlee/awesome-agent-orchestrators

### 5.4 Local MCP + chat companion permission scoping
- **Vuln class / technique:** n/a-tooling (local MCP capabilities for chat models)
- **Preconditions:** Chat account with MCP capability; local desktop install; reviewed tool permissions
- **Generalized hunting idea:** Local MCP + browser companion patterns let chat models operate on real files/terminals/workers—for security research tooling, emphasize permission scoping, provider rule compliance, and human supervision; do not use local tools to override safety refusals.
- **Tags:** mcp, chatgpt, local-tools, multi-agent, tooling
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://github.com/totec448-spec/chat-on-steroids

### 5.5 Burp Montoya re-exported as localhost OpenAPI for agents
- **Vuln class / technique:** Tooling bridge (Burp Suite ↔ AI agents)
- **Preconditions:** Burp Suite with extension support; local AI agents that can call REST/OpenAPI
- **Generalized hunting idea:** When vendor MCP/APIs underserve UI power, a thin extension that re-exports internal APIs over localhost can let agents drive scans, sitemap walks, websocket tooling, and other extensions under authorized scope.
- **Tags:** burp, reburp, AI-agents, MCP, tooling, openapi
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://x.com/forefy/status/2098160999719211488

### 5.6 Agentic SAST pass on AI-written code (plain-language + re-verify)
- **Vuln class / technique:** Agentic SAST / secure-coding feedback for AI-generated code (defensive)
- **Preconditions:** Codebase or AI-agent-produced patches available locally
- **Generalized hunting idea:** Pair code-writing agents with a second agentic security pass that explains issues in plain English, estimates dollar impact, and re-verifies fixes before writing to disk. Useful for defending AI-written code and for remediation language in reports.
- **Tags:** agentic-security, SAST, AI-code, verification, tooling
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://x.com/7h3h4ckv157/status/2096654287162245122

### 5.7 DAST: crawl + JS + API + replay evidence in one workflow
- **Vuln class / technique:** DAST / crawl-assisted recon tooling
- **Preconditions:** Authorized target; ability to run local CLI scanner
- **Generalized hunting idea:** Combine HTTP + browser-assisted crawling, JS analysis, API import, and replayable evidence into one workflow so findings stay evidence-oriented instead of one-off scans.
- **Tags:** DAST, crawling, JS-analysis, tooling
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://x.com/bountywriteups/status/2103890018670616715

---

## 6. Path normalization / Password-reset / Filter mismatches

### 6.1 Path traversal filter mistake classes
- **Vuln class / technique:** Path traversal filter bypass classes (termination, strip-evasion, nested decoding, truncation)
- **Preconditions:** App accepts user-controlled file/path parameters with naive blacklist/normalization; downstream may stop early, re-decode, strip once, or truncate
- **Generalized hunting idea:** When path or file upload/download params are filtered, probe classes of filter mistakes: early string termination, single-pass strip of `../`, incomplete multi-layer URL decoding, and fixed-buffer truncation that drops the filter suffix while leaving a dangerous prefix. Map each class to how the language/runtime and reverse proxy normalize paths before access checks. Treat as a normalization mismatch problem across proxy, app, and OS.
- **Tags:** path-traversal, lfi, filter-bypass, encoding, truncation
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://x.com/BRuteLogic/status/2105307679640223925

### 6.2 Password-reset JSON email control-character / newline injection
- **Vuln class / technique:** Newline / control-character injection in JSON email fields (multi-recipient logic flaw)
- **Preconditions:** Password-reset (or similar) API accepts JSON with an email string; backend or mail layer may split on newlines/control chars without validating a single address
- **Generalized hunting idea:** On auth flows that take an email in JSON, test whether control characters (especially newlines) inside the string cause the mailer or parser to treat multiple addresses as recipients. Confirm impact only by observing whether reset material reaches an unintended inbox you control under program rules—not by broadcasting tokens.
- **Tags:** password-reset, JSON-injection, newline-injection, ATO, input-validation
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://x.com/wtf_yodhha/status/2099388849772466557

### 6.3 Authz filter vs dispatcher path-normalization mismatches (n-day / patch-diff)
- **Vuln class / technique:** N-day / patch-diff research with LLM harness; authz filter vs dispatcher path-normalization mismatches
- **Preconditions:** Public advisory/IoCs and access to vulnerable vs patched builds for authorized lab analysis; isolated lab; human skepticism of agent assumptions
- **Generalized hunting idea:** For freshly patched, actively exploited products: stand up vulnerable and patched labs, patch-diff from IoC strings to changed auth/SQL sinks, hunt systematic auth-check mismatches (filter normalization vs router semantics; page/service context confusion), and keep pushing the model when a chain is incomplete. After vendor patches, re-sweep the same bug classes for residual bypasses—without publishing exploit recipes.
- **Tags:** n-day, patch-diff, llm-harness, auth-bypass-patterns, enterprise-software
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://techanarchy.net/from-patch-to-exploit-using-claude-code-to-reverse-engineer-a-zero-day-in-papercut-ng/

---

## 7. XSS / Encoding / WAF filter catalogs

### 7.1 Encoding-variant catalogs for scheme/URL sinks
- **Vuln class / technique:** XSS filter evasion via alternate encodings in scheme strings
- **Preconditions:** Reflection into URL/JS contexts with naive blacklist filters
- **Generalized hunting idea:** When filters ban a scheme literally, test alternate encodings (entities, mixed case, whitespace) that the browser still interprets. Maintain encoding-variant wordlists for URL/scheme sinks — do not paste live payloads into unauthorized targets.
- **Tags:** XSS, filter-bypass, wordlist, encoding
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://x.com/ethical_h4ck3r_/status/2099347683987046887

### 7.2 XSS regex/WAF mismatch family catalog
- **Vuln class / technique:** XSS regex WAF bypass via alternate handlers, data: URIs, unicode escapes, broken-attribute parsing
- **Preconditions:** HTML sink with regex-based filter/WAF
- **Generalized hunting idea:** Maintain a catalog of parser/WAF mismatch classes (event-handler variety, `data:` documents, unicode in identifiers, malformed tags the browser still accepts). Test methodology: classify filter type → pick mismatch family — without dumping live weaponized strings into out-of-scope apps.
- **Tags:** XSS, WAF-bypass, regex, filter-mismatch
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://x.com/n0aziXss/status/2096524472601768217

---

## 8. SSRF / Header trust / 403 bypass

### 8.1 Blind SSRF via systematic header namespace + OOB
- **Vuln class / technique:** Blind SSRF discovery through header injection + OOB collaborator
- **Preconditions:** Intruder/Collaborator (or similar OOB); request that may honor custom headers
- **Generalized hunting idea:** Bruteforce header names with OOB callback values; monitor hits with a collaborator aggregator. Systematic header surface for SSRF often beats guessing `X-Forwarded-*` alone.
- **Tags:** SSRF, blind-SSRF, Burp, OOB, headers
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://x.com/ethical_h4ck3r_/status/2098744915001786871

### 8.2 403 paths that trust spoofable forwarding / IP headers
- **Vuln class / technique:** Access-control bypass via trusted client IP headers
- **Preconditions:** Target returns 403 on sensitive paths; app or WAF may trust forwarding headers
- **Generalized hunting idea:** On 403 responses, systematically challenge whether access decisions trust spoofable client-IP / forwarding headers (and similar identity headers) instead of true network identity. Tip only; not always applicable—treat as header-trust differential test.
- **Tags:** 403-bypass, header-injection, IP-spoofing, access-control
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://x.com/ethical_h4ck3r_/status/2099352309834588200

### 8.3 Under-tested features: export/PDF, digests, previews
- **Vuln class / technique:** Low-attention surface hunting (export/PDF → SSRF/SSTI; digests → IDOR; previews → path issues)
- **Preconditions:** Crowded BB program; authenticated feature access
- **Generalized hunting idea:** Prefer features with few testers: Export/PDF → SSRF/SSTI; email digests → IDOR on recipient IDs; file previews → path issues via filenames. Crowding on auth ≠ coverage of utilities.
- **Tags:** methodology, SSRF, SSTI, IDOR, path-traversal
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://x.com/aacle_/status/2105641477187817799

---

## 9. Classic recon → hunt workflows

### 9.1 Fixed pipeline: multi-source enum → param buckets → business logic → secrets → report
- **Vuln class / technique:** Repeatable BB workflow
- **Preconditions:** Authorized target; common recon suite; do not skip recon before exploitation
- **Generalized hunting idea:** Execute a fixed pipeline every time: (1) multi-source subdomain enum → live host/tech-detect → deep URL collection, (2) parameter extraction and pattern buckets via templates—not random poking, (3) manual business-logic/API work (JWT/cookie trust, IDOR/UUID predictability, GraphQL introspection), (4) secrets in JS bundles and leaked env/git artefacts, (5) evidence-first reporting. Meta-rule: attack-surface size decides success odds; automation ends where business logic begins.
- **Tags:** workflow, recon, projectdiscovery, idor, graphql, secrets, methodology
- **Lane provenance:** Researchy
- **Quality:** ok (WebFetch Cloudflare 403 → recovered via curl)
- **Sources:** https://infosecwriteups.com/my-complete-bug-bounty-hunting-workflow-every-command-i-use-step-by-step-68484276471f

### 9.2 Methodology-as-product (Ars0n): UI-gated stages + unified DB
- **Vuln class / technique:** End-to-end BB workflow automation / attack-surface mapping platform
- **Preconditions:** Docker Compose host; optional OSINT API keys; authorized targets only
- **Generalized hunting idea:** Force a correct hunting order via UI-gated stages wrapping common tools, store results in a central DB for attack-surface visualization, and pair each stage with lessons so beginners absorb the *why*. Pattern: methodology-as-product—make skipping recon hard; unify tool output; add MCP/AI assistant hooks for triage.
- **Tags:** framework, bug-bounty, recon, beginner, mcp, attack-surface
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://github.com/R-s0n/ars0n-framework-v2

### 9.3 Subdomain inventory + CVE/KEV + takeover signals early
- **Vuln class / technique:** Attack-surface recon; subdomain enum + DNS; takeover signals; CVE/KEV correlation
- **Preconditions:** Target org with public DNS/subdomains
- **Generalized hunting idea:** Map full subdomain inventory early; cross-reference discovered hosts/products against CVE/KEV feeds; prioritize takeover-prone dangling DNS and unpatched critically scored products before deep app testing.
- **Tags:** recon, subdomain, takeover, CVE-intel, ASM
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://SubMap.net

### 9.4 Classic class taxonomy checklist (input→sink)
- **Vuln class / technique:** Educational FAQ covering XSS, IDOR, SSRF, SQLi, RCE classes
- **Preconditions:** Beginner / general web app hunting context
- **Generalized hunting idea:** Prioritize classic web classes by how user input reaches sinks: unencoded reflection (XSS), direct object identifiers without authz (IDOR), server-side URL fetchers (SSRF incl. cloud metadata), query construction from input (SQLi), and eval/command construction (RCE). Treat FAQ-style class definitions as a checklist when mapping each endpoint’s trust boundaries.
- **Tags:** education, xss, idor, ssrf, sqli, rce, beginner
- **Lane provenance:** Researchy
- **Quality:** ok (thin on novel research; useful taxonomy)
- **Sources:** https://BugBountyHunting.com

### 9.5 Android: bulk APK ingest → exported activities → AI on ranked targets
- **Vuln class / technique:** Bulk APK triage automation
- **Preconditions:** APK/XAPK/ZIP inputs; decompiler; ADB for exported components
- **Generalized hunting idea:** Automate triage: extract main APK, enumerate exported activities, generate ADB launch commands, then apply AI only to ranked interesting components — mirrors web “map & rank then hunt.”
- **Tags:** Android, APK, exported-activities, mobile, AI-assist
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://x.com/dirtycoder0124/status/2097280683924467834

### 9.6 AD baseline automation: communicate chainable risks, not DA-or-bust
- **Vuln class / technique:** AD baseline automation; risk communication over DA-or-bust
- **Preconditions:** Authorized AD engagement
- **Generalized hunting idea:** Automate repetitive AD checks; success = identifying/communicating chainable risks (exposed data, weak configs), not only Domain Admin. Useful contrast to external-only skill packs.
- **Tags:** Active-Directory, automation, pentest-methodology
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://x.com/three_cube/status/2096695889259851867

---

## 10. N-day / Patch-diff / Kernel & enterprise patterns

### 10.1 AI accelerates known kernel pattern classes (RCU/UAF)
- **Vuln class / technique:** Kernel net/sched UAF (lock mismatch: RCU lookup vs non-RCU free); race window widening; pattern hunting
- **Preconditions:** Unprivileged user namespaces; authorized local kernel research lab
- **Generalized hunting idea:** AI accelerates discovery of known pattern classes (RCU/UAF lock mismatches) — treat fresh bugs like accelerated n-days. Hunt code that looks up under RCU but frees without grace period. Race reliability comes from window-widening + restructuring to cheaper error paths + isolation of contending locks. Still need deep subsystem judgment for AI blind spots. Pattern search can yield sibling bugs in other subsystems.
- **Tags:** kernel, net/sched, UAF, race, AI-assisted, LPE-research
- **Lane provenance:** Researcher
- **Quality:** ok
- **Sources:** https://starlabs.sg/blog/2026/07-when-ai-makes-0-days-feel-like-n-days/

### 10.2 Protocol state-machine rollback UAF family (SCTP)
- **Vuln class / technique:** Kernel SCTP use-after-free (stale COOKIE-ECHO rollback; freed stream scheduler pointer)
- **Preconditions:** Unpatched kernel with SCTP; ability to drive SCTP association state; authorized research only
- **Generalized hunting idea:** Protocol state-machine rollbacks often free tables without invalidating cached pointers or purging queues. Hunt for “rollback/restart” paths that free/rebuild stream or session state but leave scheduler/outqueue caches dangling. Cross-check n-day kernel advisories against still-live distro versions in scope. Do not reuse public exploit trees in unauthorized environments.
- **Tags:** kernel, SCTP, UAF, LPE-research, CVE-2026-52924
- **Lane provenance:** Researcher
- **Quality:** thin (GitHub folder no README; synopsis from Ubuntu/OpenCVE only; exploit sources not used)
- **Sources:** https://github.com/NebuSec/CyberMeowfia/tree/main/security-research/Linux-CVE-2026-52924-ubuntu-7.0.0-28/

### 10.3 AEM n-day triage: authZ + stored XSS by version fingerprint
- **Vuln class / technique:** AEM privilege escalation; security-feature bypass; stored XSS / incorrect authorization / improper input validation (multi-CVE bulletin)
- **Preconditions:** AEM Cloud Service / 6.5 LTS / 6.5 versions in scope matching bulletin
- **Generalized hunting idea:** On AEM targets, prioritize authZ flaws and stored XSS in form fields reachable by low-priv users; map bulletin CVEs to version fingerprints. When primary vendor pages block scrapers, use CERT mirrors + CVE aggregators for scope triage.
- **Tags:** AEM, Adobe, XSS, priv-esc, n-day, APSB26-98
- **Lane provenance:** Researcher
- **Quality:** blocked-recovered (helpx EdgeSuite 403; recovered via HKCERT/NotCVE)
- **Sources:** https://helpx.adobe.com/security/products/experience-manager/apsb26-98.html

---

## 11. Web3 audit corpora

### 11.1 Labeled smart-contract audit findings for pattern mining
- **Vuln class / technique:** n/a-meta (dataset for threat models / pattern libraries)
- **Preconditions:** Interest in smart-contract audit pattern mining; willingness to clean/dedupe raw findings
- **Generalized hunting idea:** Large corpora of labeled audit findings (title, description, severity, recommendations; often Solidity) can seed threat models and pattern libraries for web3 reviews—use for classification and invariant brainstorming after cleaning; treat embedded PoC fields as dataset content to study patterns, not as ready-to-run attack recipes. Recurring classes noted in preview: fee/token decimal mismatches, reentrancy CEI issues, deflationary token accounting, slippage, gas underestimation.
- **Tags:** dataset, smart-contracts, solidity, audit-findings, web3, training-data
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://huggingface.co/datasets/Zaevlad/audit-findings-dataset/viewer

---

## 12. PoC hygiene & responsible disclosure

### 12.1 Minimal public scare surface for takeover-style proofs
- **Vuln class / technique:** Responsible PoC hygiene for asset takeover (S3/subdomain-style) — reporting practice
- **Preconditions:** Demonstrated control of a misconfigured public asset; program customers could stumble on a flashy public PoC page
- **Generalized hunting idea:** For takeover-style proofs, minimize public scare surface: blank/minimal page, proof only in an HTML comment (optionally encoded), include your platform handle to deter claim-theft, and put decoding instructions in the private report so triage can verify without normies panicking.
- **Tags:** responsible-disclosure, PoC-hygiene, S3-takeover, subdomain-takeover, reporting, HackerOne
- **Lane provenance:** Deep Research
- **Quality:** ok
- **Sources:** https://x.com/vortexau/status/2098892189250343336

---

## 13. Program intel / Prioritization / Ops

### 13.1 Prioritize by public H1 activity / payout signals
- **Vuln class / technique:** Program intel / hunting prioritization
- **Preconditions:** Access to public HackerOne program metadata / community dashboards
- **Generalized hunting idea:** Use public-program activity and payout distribution signals to prioritize where researchers are currently succeeding, rather than hunting only by personal preference.
- **Tags:** hackerone, program-intel, prioritization
- **Lane provenance:** Researchy
- **Quality:** ok
- **Sources:** https://x.com/zseano/status/2105766060398162315

### 13.2 Historical program-policy signal (payout tables, unified scopes)
- **Vuln class / technique:** Bug-bounty program design / scope & payout policy (operator-side lessons for hunters)
- **Preconditions:** N/A beyond watching program updates
- **Generalized hunting idea:** Programs that publish payout tables, expand in-scope vuln types by CVSS/impact, shorten triage SLAs, and unify previously private brand scopes reward steady engagement. Prioritize classes programs explicitly top-rank while watching for newly opened assets when private sub-programs merge. Historical signal that live-hacking events + continuous private programs compound attack-surface reduction.
- **Tags:** hackerone, program-policy, payouts, scope, historical
- **Lane provenance:** Researchy
- **Quality:** ok (2018 historical)
- **Sources:** https://hackerone.com/blog/oath-bug-bounty-program-update-1m-payouts-and-expansion-program

### 13.3 Mobile-first remote session continuity (ops)
- **Vuln class / technique:** Mobile-driven pentest workflow (ops)
- **Preconditions:** Remote testing setup reachable from phone
- **Generalized hunting idea:** Treat mobile-first remote testing as an ops pattern (session continuity, lightweight tooling) rather than a vuln class—useful for sustained triage while away from desk.
- **Tags:** ops, mobile, pentesting-workflow
- **Lane provenance:** Researchy
- **Quality:** ok (low technical depth)
- **Sources:** https://x.com/UK_Daniel_Card/status/2096709936449212502

---

## 14. Thin / Outcome-only / Tangential

### 14.1 Crypto + WAF + encrypted login (title only)
- **Vuln class / technique:** Cryptographic issue enabling WAF bypass around encrypted login (title only; no method detail)
- **Preconditions:** Target behind WAF with encrypted/login-related surface; insufficient public detail
- **Generalized hunting idea:** When celebrating AI-assisted wins, extract only the vuln theme from titles/screenshots (here: crypto + WAF + login). Treat as a reminder to review cryptographic construction of auth/login envelopes for ways encoding or wrapping interacts with WAF inspection—without inventing steps not present in the post.
- **Tags:** HackerOne, WAF-bypass, cryptography, login, AI-assisted, thin
- **Lane provenance:** Deep Research
- **Quality:** thin
- **Sources:** https://x.com/X_cryptographer/status/2097729338926154046

### 14.2 Fine-tuned harness chained to RCE (outcome-only)
- **Vuln class / technique:** AI harness / agent chaining culminating in RCE claim (method not disclosed)
- **Preconditions:** Custom AI security harness; authorized target; production claim redacted
- **Generalized hunting idea:** Fine-tuning an agent harness and chaining findings toward higher impact is a workflow theme (agent → validate → escalate). Post is outcome-only; use it as motivation to build verification loops, not as a recipe—no chaining steps or payloads are published.
- **Tags:** RCE, AI-harness, agent-workflow, thin, outcome-only
- **Lane provenance:** Deep Research
- **Quality:** thin
- **Sources:** https://x.com/0xManan/status/2097230196252500043

### 14.3 General-purpose local AI agent (DeerFlow) — tangential
- **Vuln class / technique:** General-purpose local AI agent — no vuln technique
- **Preconditions:** Local or cloud LLM; willingness to run open-source agent with isolated task envs
- **Generalized hunting idea:** General agent platforms can support recon/note-taking workflows if sandboxed, but this post does not teach a security vuln class. Keep isolation/sandbox claims in mind when evaluating agent tooling; do not treat marketing feature lists as hunting methodology.
- **Tags:** DeerFlow, AI-agent, open-source, tooling, tangential, thin
- **Lane provenance:** Deep Research
- **Quality:** thin
- **Sources:** https://x.com/mikenevermiss/status/2096513894395043943

### 14.4 Cadence experimental learning library — tangential tooling
- **Vuln class / technique:** n/a-tooling (experimental ML/agent “brain” library)
- **Preconditions:** Python 3.11+; interest in alternative learning architectures
- **Generalized hunting idea:** Cadence is an experimental learning library (bounded patches, settlement, recursive error feedback)—relevant only as adjacent agent/ML tooling research, not as a security vulnerability technique. Marked for corpus completeness.
- **Tags:** ml-library, agents, experimental, learning, n/a-security-writeup
- **Lane provenance:** Deep Research
- **Quality:** ok (tangential; limited BB technique content)
- **Sources:** https://github.com/muellerberndt/cadence

---

## Lane provenance summary

| Lane | Source items | Quality notes |
|------|--------------|---------------|
| **Researchy** | 24 (12 articles + 12 posts) | 0 blocked; 2 fetch recoveries (Infosec Write-ups Cloudflare 403; Tsecbench SPA) |
| **Researcher** | 23 (11 articles + 12 posts) | ok=20 · blocked-recovered=2 · thin=1 |
| **Deep Research** | 22 (11 articles + 11 posts) | ok=19 · thin=3 · blocked=0 |
| **Total source items** | **69** | |

**Source receipts:**
- Researchy: `/workspace/bb-bookmark-lane-researchy/LANE_RECEIPT.md`
- Researcher: `/workspace/researcher-lane-extract-2026-10.md`
- Deep Research: `/workspace/bug-bounty-corpus/x-bookmark-lane/DEEP_RESEARCH_LANE_SUMMARY.md`

---

## Dedupe notes / gaps / conflicts

- **Merged:** Adverserial / CyberKimi product docs (`adverserial.ai` + `adverserial.ai/docs.html`) into one idea (4.16); both lanes cited under Sources.
- **Related but kept separate:** JS graveyard (1.2), MTN sourcemap→IDOR (1.3), and report-trained IDOR skill (1.4) share a theme but differ in technique; zsec `harnessing-harnesses` (4.1) vs `bullyingllms` (4.2) are distinct articles; two `adnanthekhan` posts (4.13 orchestration vs 4.14 swarm claim) kept separate.
- **Anecdotal / unverified:** Researcher agent-swarm SSRF→RCE→K8s claim (4.14); AdamShao fully-agentized workflow (4.21) marked culture signal.
- **Blocked-recovered honesty:** PageBreak findings (4.6) and AEM APSB26-98 (10.3) used alternate summaries when primary URLs gated/403’d; details limited to what alternates provided.
- **Thin preserved:** SCTP folder (10.2), crypto/WAF title-only (14.1), RCE outcome-only (14.2), DeerFlow (14.3).
- **No conflicts** on facts across lanes; exclusive URL assignment held. Methodology-only: any PoC/payload content present in sources was already stripped at lane extract or omitted here.
- **Gap:** No cross-lane coverage of GraphQL-specific deep techniques beyond workflow mentions; web3 limited to one corpus pointer; mobile beyond one Android triage tip is thin.

---

## Stats footer

| Metric | Count |
|--------|------:|
| Total source items ingested | **69** |
| Unique ideas after dedupe | **68** |
| Clusters | **14** |
| Thin | **4** (SCTP folder; crypto/WAF title-only; RCE outcome-only; DeerFlow) |
| Blocked-recovered | **2** (PageBreak findings; AEM APSB26-98) |
| Blocked unrecovered | **0** |
| Explicit merges | **1** (Adverserial/CyberKimi) |

*KB generated 2026-10-02 Asia/Calcutta. Patterns only — authorized hunting methodology. No inventing of missing details.*
