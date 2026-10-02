# LLM & agent hunting process

**Cluster file:** `04-llm-hunting-process.md`  
**Audience:** Akshat (authorized / in-scope hunting only)  
**Constraint:** Abstract methodology only — **no** reproduction steps, payloads, PoCs, exploit recipes, Intruder setups, or attack procedures.  
**Items in this cluster:** 23

---

### 4.1 Orchestration layer over raw model choice (recon→hunt→validate→trace→report)

- **Root-cause class:** LLM orchestration / AI security research harness design
- **Affected component:** Authorized codebases/binaries + coding-agent/MCP harness
- **Impact:** Scale without triage/dedupe quality increases duplicate and false-positive load.
- **Conditions called out:** Access to coding agents + optional MCPs; codebase or binary targets under authorization; ability to stage prompts and artefacts
- **What the source teaches (abstract):** Invest in the orchestration layer more than raw model choice: split work into recon→hunt→validate→trace→report with per-stage prompts and structured artefacts; give each stage only scoped context; use adversarial/validate agents that try to disprove findings; route cheap models for classify/summarize and strong models for validation/trace; add RAG memory of prior notes and a post-run feedback loop. Surveyed harness patterns: RAPTOR (static+dynamic+solver gates), Anthropic defending-code (ASAN-verified find/grade/patch), baby-naptime (runtime feedback loop), evilsocket/audit (8-stage trust-boundary + taint trace), Visa VVAH (threat-model first, triage candidates). Context budget discipline (summarize scanner noise; ~8K for single-function, ~32K for synthesis) beats dumping full repos into prompts. Extract note: Strong methodology piece; author also released ZephrFish/harness-kit template (recon→hunt→validate→trace→report). Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** llm-harness, orchestration, raptor, mcp, validation-gates, rag, token-budget, offensive-research
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://blog.zsec.uk/harnessing-harnesses/
  - https://x.com/i/web/status/2097218639074070705
- **Notes:** [Researchy:A.3] Strong methodology piece; author also released ZephrFish/harness-kit template (recon→hunt→validate→trace→report).

---

### 4.2 MCP-wrapped campaigns with hallucination→validated promotion

- **Root-cause class:** LLM/MCP-orchestrated vuln hunting; grammar-based fuzzing; patch-diff campaigns (methodology)
- **Affected component:** Research toolchain: MCP-wrapped RE/fuzz/debug/reporting tools and campaign RAG store
- **Impact:** Process risk of false-positive or unverified LLM findings if promotion gates are skipped; methodology aims to reduce that
- **Conditions called out:** Isolated research lab (e.g., Proxmox VMs) with target and analysis hosts; MCP-wrapped RE/fuzz/debug/reporting tools and persistent campaign storage; Human validation gates before any disclosure or submission
- **What the source teaches (abstract):** A methodology writeup on wrapping a vulnerability-research toolchain as MCP tools, organizing work as campaigns, and forcing every LLM finding through a multi-gate promotion pipeline before disclosure. It discusses grammar-based fuzzing and patch-diff campaigns at a high level, plus feeding crashes, defenses, and bounty ROI back into RAG so later hunts avoid hardened dead-ends. Emphasis is on human validation and knowledge compounding, not on publishing attack recipes. Pattern: Wrap the research toolchain as MCP tools, run campaign-scoped hunts, promote only findings that pass hallucination→validated gates (existence, clean-snapshot confirmation, exploitability, low-priv reachability), and store negatives/defenses/ROI so future campaigns skip dead-ends.
- **Tags:** mcp, autonomous-hunting, hallucination-gates, rag-feedback, patch-diff, fuzzing, bounty-roi, methodology
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://blog.zsec.uk/bullyingllms/
  - https://x.com/i/web/status/2097218639074070705
- **Notes:** [Deep Research:2] High-level methodology only; extract already frames auth-bypass/SSRF/OEM chains without repro steps.

---

### 4.3 Minimal threat-model scaffolding (avoid context rot)

- **Root-cause class:** LLM-assisted audit process failure modes (context rot; weak threat-model scaffolding)
- **Affected component:** LLM code-audit workflow over authz, JWT/JWKS, signature validation, and CI egress boundaries (pattern-level)
- **Impact:** Missed or hallucinated findings when prompts are too broad; improved signal when audits are slice-scoped and verified
- **Conditions called out:** Readable target source (OSS or authorized audit scope); Prior CVE/advisory history or architectural threat model for the project; Verifier loop (tests, builds, harnesses) to confirm model claims
- **What the source teaches (abstract):** Methodology article arguing that bloated agent scaffolds and 'find all vulns' prompts cause context rot and hide real issues. It recommends deriving a one-page threat model from past CVEs and trust boundaries, auditing thin slices (auth, JWT, cookies, sandbox egress), demanding call-chain evidence, and spending tokens on exploration plus verification. Pattern-level mentions of authz boundary bugs, JWT/JWKS confusion, signature flaws, and CI egress gaps appear as hunt themes, not as reproduction guides. Pattern: Prefer minimal scaffolding and CVE-derived threat models; audit thin trust-boundary slices; require call-chain evidence; verify with tests/harnesses rather than expanding prompt bureaucracy.
- **Tags:** llm-audit, threat-model, context-rot, minimal-scaffolding, authz, jwt, ci-security, prompt-patterns
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://devansh.bearblog.dev/needle-in-the-haystack/
  - https://x.com/i/web/status/2098447232764969079
- **Notes:** [Deep Research:3] Pattern-level vuln themes only; no repro content in lane extract.

---

### 4.4 Coverage-led AI code audit with adversarial disprove verifiers

- **Root-cause class:** Coverage-led AI code audit / adversarial finding verification
- **Affected component:** Codebases under authorized coding-agent audit
- **Impact:** Methodology / tooling impact: lower false positives, better token use, and stronger validation gates — not a single product CVE.
- **Conditions called out:** Coding agent with tool-use + parallel sub-agents; Node.js for validators; OS sandbox (no egress, allowlisted env, scratch-only writes) for any target-code execution
- **What the source teaches (abstract):** Run audits as six gated phases: (1) recon → architecture.md + coverage-ledger.json, (2) coverage-led hunting with isolated hunters + coverage critics, (3) fresh verifiers that try to *disprove* candidates, (4) structured findings (confirmed / needs_validation / rejected) against a schema, (5) independent record re-verification, (6) target-neutral reports. Confirm only established boundary failures with source traces; severity needs impact; defense-in-depth gaps alone are hardening notes. Repeat runs are additive against the ledger. Attack-class prompt packs span web/protocol/auth, client-side, supply-chain, cloud, RPC/messaging, resource exhaustion, data isolation, desktop/mobile IPC, memory-safety, and AI/LLM surfaces. Extract note: Seeds Cloudflare’s vulnerability harness blog; install via skills CLI. Strong defensive/research process design. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** cloudflare, agent-skill, code-audit, coverage-ledger, adversarial-validation, sarif-like, harness
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://github.com/cloudflare/security-audit-skill
  - https://x.com/i/web/status/2099473233787388049
- **Notes:** [Researchy:A.6] Seeds Cloudflare’s vulnerability harness blog; install via skills CLI. Strong defensive/research process design.

---

### 4.5 PageBreak: deterministic non-AI validators for agent hypotheses

- **Root-cause class:** Over-trusting LLM vulnerability hypotheses without class-specific, deterministic validators — false positives and unverified “findings” at agentic scale; also, broad codebases without safe-by-design frameworks leave large bug-class surfaces open.
- **Affected component:** Agentic vuln-discovery pipelines targeting classes such as XSS, SQLi, path traversal, RCE, SSRF; monorepo-scale apps with HTTP↔source mapping; validation/oracle layer separate from the hypothesizing agent.
- **Impact:** As framed by Google: agentic discovery can surface real, multi-class flaws when validators prove impact — but unverified candidates are noise; safe-by-design frameworks dramatically shrink findings vs broad codebases.
- **Conditions called out:** Running application environment for validation; specialized validators per vuln class; source/config access (monorepo-scale helps); authenticated scanning infrastructure.
- **What the source teaches (abstract):** Treat LLM hypotheses as untrusted until a separate validator proves impact on a live target. Prefer near-zero-FP pipelines: hypothesize → validate with class-specific oracles → only then report. Unverified candidates seed deeper runs and guide new validator development. Safe-by-design frameworks (eliminate whole bug classes) shrink findings vs broad codebases. Chain-capable agents benefit from HTTP↔source mapping and repeated identical seeds.
- **Tags:** agentic-AI, validation, XSS, SSRF, SQLi, RCE, PageBreak, false-positives
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://blog.google/security/agentic-hacks-real-proofs-inside-googles-pagebreak-project/
- **Notes:** [Researcher:02] ok

---

### 4.6 PageBreak real-world finding themes (cache / signature / UXSS)

- **Root-cause class:** 1. **Incomplete cache key** — shared CDN/static cache omits path/query dimensions that should distinguish responses, enabling unrelated requests to collide and poison shared JavaScript. 2. **Signature trust of attacker-influenced params via sibling endpoints** — multi-endpoint signing where an alternate path will sign values the primary flow should not accept with the same key. 3. **Overly broad extension message-channel trust** — browser extension accepts connections from wide origin scopes (e.g. parent-domain wildcards) without exact sender checks, so XSS on a broad parent can escalate to UXSS.
- **Affected component:** Shared CDN/static JS cache; crypto/signing endpoints; browser extension messaging (Tag Assistant–class UXSS as summarized by alternate).
- **Impact:** Cache-key collision → JS cache poisoning; crypto signature bypass via alternate signing endpoint; UXSS via permissive extension messaging (per alternate summary of gated post).
- **Conditions called out:** Shared CDN/static-cache with incomplete cache key; multi-endpoint signing of attacker-influenced params; browser extension trusting broad origins.
- **What the source teaches (abstract):** (1) Audit cache keys for omitted path/query dimensions that let unrelated requests collide and poison shared JS. (2) When an exploit needs a signature, hunt sibling endpoints that will sign attacker-controlled values with the same key. (3) Extension/message-channel trust: any XSS on a broad parent domain can escalate if the extension accepts connections from “any \*.google.com”-style scopes without exact sender checks. — Planning/audit language only; no reproduction of original PoCs.
- **Tags:** cache-poisoning, XSS, UXSS, signature-bypass, PageBreak
- **Lane:** Researcher
- **Quality:** blocked-recovered (primary Google Bug Hunters URL sign-in gated; ideas recovered via CyberKendra summary)
- **Sources:**
  - https://bughunters.google.com/blog/pagebreak-real-world-findings
  - https://www.cyberkendra.com/2026/09/google-pagebreak-ai-agent-500-xss-flaws.html
- **Notes:** [Researcher:03] blocked — Original URL returned a Google sign-in wall. Ideas below recovered **only** from the CyberKendra summary already cited in the extract; primary post body was not fetched.

---

### 4.7 StrikeAgent: hunt → attack graph → re-rate/verify → memory

- **Root-cause class:** AI pentest agents that skip re-rate / second verification inflate false positives; platforms that leak predictable entry paths (`/login`, `/api`) or lack replay/bruteforce controls recreate the same classes of flaws they hunt for.
- **Affected component:** Agentic external foothold hunting; attack-graph self-loop; red-team / SRC / CTF mode separation; the hunter platform’s own auth and path exposure surface.
- **Impact:** Better FP reduction and technique distillation when verification is mandatory; conversely, unhardened hunter consoles become soft targets themselves.
- **Conditions called out:** Explicit authorization; console + model config; tools on PATH (Docker image includes probe tooling).
- **What the source teaches (abstract):** Structure agent cycles as: hunt → attack graph → re-rate/verify → distill techniques into memory. Prefer “finish a full round before asking human” with interruptible chat. Separate red-team / SRC / CTF modes. Hardening of the hunter platform itself (random entry paths, no leaked `/login`|`/api`, replay/bruteforce controls) is itself a checklist for apps you test.
- **Tags:** agentic-AI, red-team, SRC, attack-graph, FP-reduction, authorized-only
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://github.com/Yean-Sec/StrikeAgent_AtkBrain-Flash
- **Notes:** [Researcher:05] ok

---

### 4.8 Claude-BugHunter: per-class skills + 7-Question Gate

- **Root-cause class:** Ad-hoc hunting without per-class skill packs and triage gates leads to out-of-scope work, weak evidence, and missed regression/shadow-API/cloud-IAM classes that disclosed-report patterns already encode.
- **Affected component:** Per-class hunt skills spanning XSS, IDOR, SSRF, JWT, OAuth, GraphQL, cache-poison, enterprise VPN/M365/Okta/vCenter, etc.; 7-Question Gate triage; recon→map→hunt→validate→report pipeline; optional Burp MCP.
- **Impact:** Codified methodology improves consistency and reduces bad submits; deliberate OOS split keeps external BB skills separate from internal AD/C2.
- **Conditions called out:** Authorized BB/pentest scope; Claude Code / compatible harness; optional Burp MCP.
- **What the source teaches (abstract):** Codify disclosed-report patterns into auto-loaded per-class skills. Enforce validation gates before submit (scope, impact acceptance, evidence hygiene). Split external surface skills from internal AD/C2 (deliberate OOS). Extend skill packs with: cache-poison, shadow APIs, cloud IAM post-cred, mid-engagement IR detection, regression of “fixed” bugs.
- **Tags:** skills, methodology, triage, hunt-\*, enterprise-platform, reporting
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://github.com/elementalsouls/Claude-BugHunter/tree/main/skills
- **Notes:** [Researcher:06] ok

---

### 4.9 Quarry: H1 sync + regression retest of shipped fixes

- **Root-cause class:** Treating resolved reports as closed forever misses high-ROI regression/bypass surfaces; agent memory locked in proprietary stores reduces portability; ignoring CVE feeds vs program assets leaves n-day gaps.
- **Affected component:** Hunt-ops platform: HackerOne sync/submit; regression retest of shipped fixes; Markdown leads as agent memory; advisory/payload FTS (index/search capability — content not reproduced here).
- **Impact:** Faster regression and lead reuse; H1 remains system of record while local DB is cache.
- **Conditions called out:** Docker host; H1 API token; local-only / allowlisted deployment.
- **What the source teaches (abstract):** Treat resolved reports as high-ROI surfaces (new patch code + known PoC context) — queue every fix for regression/bypass. Store leads as plain Markdown so agents can draft/refine without lock-in. Keep H1 as system of record; local DB is cache. Cross-ref CVE feeds against your program assets.
- **Tags:** HackerOne, regression, agentic-ops, leads, advisories
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://github.com/skraft9/quarry-vrc
- **Notes:** [Researcher:07] ok

---

### 4.10 Detect-then-prove autonomous scanner pattern (Xalgorix)

- **Root-cause class:** Autonomous AI pentest tooling with independent verification loop
- **Affected component:** Self-hosted autonomous AI pentest stack with independent verifier agent (example: Xalgorix)
- **Impact:** n/a (not a vulnerability report)
- **Conditions called out:** Self-hosted environment and bring-your-own LLM; Authorized scope for automated testing
- **What the source teaches (abstract):** Post about autonomous AI pentest tooling that separates detection from proof: an autonomous hunter plus an independent verifier that re-checks findings before reporting, reducing false-positive triage load. Example stack (Go + TypeScript, Xalgorix) is self-hosted with BYO-LLM for data-privacy concerns versus SaaS scanners. Tooling pattern, not a vulnerability writeup. Pattern: Prefer scanners/agents that separate detect from prove: independent verification before report reduces false-positive load in private AI-assisted testing stacks.
- **Tags:** AI-pentester, tooling, verification, false-positives, open-source, xalgorix
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://x.com/bountywriteups/status/2099143734369690104
- **Notes:** [Deep Research:15] Tooling announcement; linked repo noted in extract only.

---

### 4.11 Mandatory working-PoC confirmation before triage (Crusader)

- **Root-cause class:** Autonomous hunters that triage on hypothesis alone flood queues with false positives; missing mandatory working-PoC confirmation.
- **Affected component:** Agentic hunting pipelines (Crusader alpha framing); triage/validation gate before human review.
- **Impact:** Reduced FP load when confirmed PoC is required before triage (mirrors PageBreak deterministic validation theme).
- **Conditions called out:** Tool access; authorized targets.
- **What the source teaches (abstract):** Require confirmed PoC before triage — mirrors PageBreak deterministic validation theme; reduces FP load. — Process rule only; no PoC contents.
- **Tags:** agentic-AI, validation, PoC
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://x.com/crusader_sec/status/2102646171562909924
- **Notes:** [Researcher:13] ok

---

### 4.12 Continuous find → validate → verify-fixes loop (Defense Factory)

- **Root-cause class:** Find-only loops without validate and verify-fix phases leave remediations unverified and regressions undetected.
- **Affected component:** Org-scale continuous AI defense loop; human mobilization alongside cyber models.
- **Impact:** Stronger remediation confidence when verify-fix is first-class (defense framing).
- **Conditions called out:** Org-scale cyber models + human mobilization.
- **What the source teaches (abstract):** Same loop as PageBreak/Quarry: agents find → validate → verify fixes hold. Skill extension: add “verify fix” / regression phase as first-class, not optional.
- **Tags:** defense-factory, agentic-AI, validation, regression
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://x.com/OpenAI/status/2097786616311840853
- **Notes:** [Researcher:18] ok

---

### 4.13 Multi-program orchestration needs triage quality

- **Root-cause class:** Multi-program automated hunting orchestration
- **Affected component:** Multiple authorized BB programs (agent orchestration)
- **Impact:** Scale without triage/dedupe quality increases duplicate and false-positive load.
- **Conditions called out:** Authorized programs; compute for parallel agent runs; triage capacity for duplicates
- **What the source teaches (abstract):** Orchestrate parallel hunt agents across several programs, then invest in dedupe/triage quality—scale helps only if duplicate rate and false positives are managed. Extract note: Wild Hunt hack-bot orchestrator; claims RCEs/ATOs with high duplication. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** automation, orchestration, RCE, ATO, Wild-Hunt
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://x.com/adnanthekhan/status/2099136955250352428
- **Notes:** [Researchy:P.5] Wild Hunt hack-bot orchestrator; claims RCEs/ATOs with high duplication.

---

### 4.14 Heterogeneous model swarms for chain focus (anecdotal)

- **Root-cause class:** Multi-stage trust failures allowing SSRF to reach RCE and then cluster-control planes — plus orchestration that keeps heterogeneous agents on a single long-running goal humans may abandon early.
- **Affected component:** Authorized infra targets; SSRF-reachable internal/metadata paths; Kubernetes control plane (as claimed); multi-agent orchestrator + specialist roles.
- **Impact:** Claimed SSRF → RCE → K8s takeover chain via multi-model swarm (unverified anecdote).
- **Conditions called out:** Authorized infra target; long-running agent budget; orchestrator model.
- **What the source teaches (abstract):** Heterogeneous model swarms with a clear goal and long runtime can surface chains humans miss. Skill extension: multi-agent roles (orchestrator + specialists) + chain focus toward cloud metadata/K8s-class impact. **Note:** anecdotal claim from post text; not independently verified in lane.
- **Tags:** agent-swarm, SSRF, RCE, Kubernetes, chaining
- **Lane:** Researcher
- **Quality:** ok (anecdotal)
- **Sources:**
  - https://x.com/adnanthekhan/status/2099445532192072048
- **Notes:** [Researcher:14] ok — **Honesty:** Anecdotal claim from post text; **not independently verified** in the extract.

---

### 4.15 Agentic ROI: token burn vs bounty outcome

- **Root-cause class:** Browser / Chromium RCE via autonomous agents (economics)
- **Affected component:** Autonomous exploit-agent economics (meta)
- **Impact:** Technical agent success can still be negative economic ROI when token/cost burn exceeds bounty.
- **Conditions called out:** Interest in agentic hunting ROI, not a specific target recipe
- **What the source teaches (abstract):** When evaluating autonomous exploit agents, track token/cost burn against bounty outcome—technical success can still be negative ROI. Extract note: Commentary on $250k Chrome RCE by Xbow; cost question. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** Chrome, RCE, Xbow, agentic-hunting, ROI
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://x.com/payloadartist/status/2098056402954580039
- **Notes:** [Researchy:P.7] Commentary on $250k Chrome RCE by Xbow; cost question.

---

### 4.16 Cyber-tuned LLM APIs as analysis aids (Adverserial / CyberKimi)

- **Root-cause class:** AI-assisted security workflows / offensive-tuned LLM API integration
- **Affected component:** Cyber-tuned LLM APIs / security-analysis product surface (CyberKimi, CyberGLM)
- **Impact:** Methodology / tooling impact: lower false positives, better token use, and stronger validation gates — not a single product CVE.
- **Conditions called out:** Access to specialized cyber-tuned LLM APIs or similar security-focused models; Security-context inputs such as code, logs, or artifacts for analysis workflows
- **What the source teaches (abstract):** Wire a security-specialized model into existing agent/CLI harnesses via a shim base URL rather than rebuilding tooling. Use model routing (cheap classify/summarize vs strong deep analysis), stream reasoning fields separately from final answers, and keep secrets out of client-side/shared images. Treat cyber-tuned models as assistants for triage, Sigma/rule drafting, and code review inside authorized scopes—not as autonomous exploit engines. Extract note: Product docs for CyberKimi/CyberGLM; privacy-first (no inference/session logs claimed); memberships + prepaid wallet. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** llm-security-tooling, detection-engineering, threat-hunting, cyberkimi, api-product
- **Lane:** Deep Research + Researchy (deduped)
- **Quality:** ok
- **Sources:**
  - https://adverserial.ai/docs.html
  - https://adverserial.ai
  - https://x.com/i/web/status/2097060366652186927
  - https://x.com/i/web/status/2097848169002627208
- **Notes:** [Researchy:A.2] Product docs for CyberKimi/CyberGLM; privacy-first (no inference/session logs claimed); memberships + prepaid wallet. | [Deep Research:1] n/a-tooling; no vuln technique content.

---

### 4.17 Local LLM ensemble + ML meta-classifier for vuln classification

- **Root-cause class:** Single-model binary vuln classification on isolated functions is near coin-flip; missing call-graph context and lack of ensemble/meta-decision logic cause false confidence.
- **Affected component:** Static analysis of functions (Chromium dataset); multi-prompt ensemble + ML meta-classifier over agreement/disagreement + metadata.
- **Impact:** Single base LLMs ≈ 50–56% accuracy; with richer context, fine-tuning, multi-view prompts, and a traditional ML meta-model on ensemble signals, final ≈ 76.9% accuracy (per extract).
- **Conditions called out:** Function + caller/callee/location/pattern context; local LLM capacity; labeled train/test set.
- **What the source teaches (abstract):** Single base LLMs ≈ coin-flip. Gains from richer context (callers, callees, location, code patterns), fine-tuning, multi-view prompts, and a traditional ML model that learns from ensemble agreement/disagreement + metadata. Don’t trust one model vote — ensemble + meta-decision; feed call-graph context not isolated functions.
- **Tags:** LLM, ensemble, static-analysis, Chromium, ML
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://martinativadar.github.io/posts/llm-vulnerability-research.html?v=2
- **Notes:** [Researcher:09] ok

---

### 4.18 Local security-tuned models need human verify + scope

- **Root-cause class:** Local cyber-offense LLM for vuln discovery (tooling)
- **Affected component:** Public offensive-AI agent benchmark platforms
- **Impact:** Methodology / tooling impact: lower false positives, better token use, and stronger validation gates — not a single product CVE.
- **Conditions called out:** Hardware for large MoE; authorized use only
- **What the source teaches (abstract):** Local security-tuned models can assist recon/hypotheses, but findings still need human verification and must stay within authorized scope—benchmarks ≠ production validity. Extract note: GLM-5.3 cybersecurity model promo; dual-use caution. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** LLM, local-models, CyberGym, tooling
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://x.com/0x0SojalSec/status/2096639626706649149
- **Notes:** [Researchy:P.11] GLM-5.3 cybersecurity model promo; dual-use caution.

---

### 4.19 Calibrate harnesses via public offensive-AI benchmarks

- **Root-cause class:** Offensive-AI / automated red-team agent capability benchmarking
- **Affected component:** Public offensive-AI agent benchmark platforms
- **Impact:** Calibration of agent harness strategies via public leaderboards (evaluation meta).
- **Conditions called out:** Public SPA/API access; agents submitted under platform rules; cheat-disclosure process exists
- **What the source teaches (abstract):** Use public offensive-AI benchmarks to compare agent harnesses across capability domains rather than chasing single demos. Tsecbench frames Agentic red-team scoring across real CVE/production-like and cloud-native tasks; related sets include XBOW Validation Benchmarks (web CTF-style) and Cybench (crypto/web/RE/vuln CTF tasks). For researchers: track leaderboard + capability-stats + cheat-disclosures to calibrate which multi-agent strategies generalize; treat benchmarks as evaluation of hunting workflows (recon, chaining, evasion) not as attack manuals. Extract note: WebFetch returned empty (client-rendered SPA); recovered via curl + /api/v1/benchmark-sets and leaderboard. Default home set_id=4 (Tsecbench v1). Zh title: 智能攻防 AI 跑分基准平台. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** tsecbench, benchmark, offensive-ai, leaderboard, xbow, cybench, tencent, agentic
- **Lane:** Researchy
- **Quality:** ok (SPA empty via WebFetch; recovered via API)
- **Sources:**
  - https://tsecbench.zc.tencent.com/#leaderboard
  - https://x.com/i/web/status/2096897731168268635
- **Notes:** [Researchy:A.12] WebFetch returned empty (client-rendered SPA); recovered via curl + /api/v1/benchmark-sets and leaderboard. Default home set_id=4 (Tsecbench v1). Zh title: 智能攻防 AI 跑分基准平台.

---

### 4.20 Proxy agentic CLIs to cheaper backends

- **Root-cause class:** Agentic coding CLI routing (tooling economics)
- **Affected component:** Local security-tuned LLM tooling
- **Impact:** Technical agent success can still be negative economic ROI when token/cost burn exceeds bounty.
- **Conditions called out:** Desire to run coding CLIs against alternate model backends
- **What the source teaches (abstract):** Proxy agentic coding CLIs to free/local model backends to lower iteration cost for research tooling—orthogonal to vuln classes but affects hunt throughput. Extract note: free-claude-code proxy; not a vulnerability pattern. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** Claude-Code, proxy, OpenRouter, local-LLM, tooling
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://x.com/7h3h4ckv157/status/2096488638456717430
- **Notes:** [Researchy:P.12] free-claude-code proxy; not a vulnerability pattern.

---

### 4.21 Fully agentized BB workflow culture signal

- **Root-cause class:** End-to-end agent ownership of recon/find/report without human-in-loop for scope ethics and severity risks shipping unvalidated agent reports.
- **Affected component:** Agent stack spanning target selection, finding, and report drafting; program access.
- **Impact:** Cultural push toward fully agentized BB workflows; quality risk if validation gates are skipped.
- **Conditions called out:** Agent stack + program access.
- **What the source teaches (abstract):** Trend toward agents owning target selection, finding, and report drafting. Ensure human-in-loop for scope ethics and severity; don’t ship unvalidated agent reports. **Note:** tone in source is satirical/boastful; treat as culture signal, not verified case study.
- **Tags:** agentic-AI, workflow, reporting
- **Lane:** Researcher
- **Quality:** ok (culture signal)
- **Sources:**
  - https://x.com/AdamShao/status/2097111709076910081
- **Notes:** [Researcher:20] ok — **Honesty:** Tone is satirical/boastful; treat as **culture signal**, not a verified case study.

---

### 4.22 Immunefi-style process interviews over tool hype

- **Root-cause class:** Research methodology / AI-assisted hunting (career + process)
- **Affected component:** Bug-bounty / Immunefi-style research process (onboarding, triage, validation, reporting)
- **Impact:** n/a (not a vulnerability report)
- **Conditions called out:** Active bug-bounty or Immunefi-style program access; Willingness to systematize hunting with AI as a force multiplier, not a replacement for validation
- **What the source teaches (abstract):** Immunefi post highlighting a high-earning researcher's process interview covering program start, AI use, hunt methodology, and industry direction. Emphasizes transferable habits: process and validation discipline matter as much as tooling. Video/interview format useful for methodology, not copy-paste exploits. Pattern: Study high-earning researchers' onboarding, AI-assisted candidate surfacing, and validation/reporting discipline; treat AI as triage/pattern aid that still needs human confirmation of impact.
- **Tags:** methodology, AI-assisted-hunting, immunefi, career, bug-bounty
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://x.com/immunefi/status/2102010814442181024
- **Notes:** [Deep Research:13] Methodology/career content; not a single vuln class.

---

### 4.23 LLM-assisted code-audit patterns (batch desync, sanitizer gaps, privilege gadgets)

- **Root-cause class:** LLM-assisted 0-day discovery; batch-API validate/execute desync; type-confused sanitization; privilege-escalation gadget chaining (patterns only)
- **Affected component:** WordPress (or similar CMS) — as framed in source
- **Impact:** High-impact code-audit findings (desync / sanitizer gaps / privilege gadgets) under authorized LLM-assisted review — PoCs deliberately omitted from extract.
- **Conditions called out:** Authorized source-code audit of WordPress (or similar) with multi-agent coding model; forbid changelog/diff cheating; require realistic pre-auth production constraints
- **What the source teaches (abstract):** Prompt/orchestrate multi-agent code audits with diverse approach portfolios, adversarial double-checks, and hard constraints (pre-auth, default config, no fabricated preconditions; encourage reading dependency source). High-level bug patterns to hunt—without reproducing PoCs: (1) APIs that validate in one loop and execute in another can desync when error paths push only one of two parallel arrays; (2) sinks that sanitize arrays but pass scalars through unsanitized; (3) nested/self-calls of batch endpoints that inherit broken validation assumptions; (4) after a read primitive, in-memory object caches + features that reconcile cache vs DB can become escalation gadgets; (5) temporary identity switches driven by attacker-influenced structured records; (6) dynamically named hooks/actions built from status×type strings. Meta lesson: as models do more chain-building, human value shifts to target selection, prompt heuristics, and steering. Extract note: Jul 20, 2026 Adam Kues / Searchlight Cyber. Extracted methodology only—deliberately omitted request bodies, SQL strings, and step-by-step attack procedures. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** wordpress, llm-research, batch-api, desync, sqli-class, gadget-chain, searchlight, agentic
- **Lane:** Researchy
- **Quality:** ok (methodology only; PoCs stripped at extract)
- **Sources:**
  - https://slcyber.io/research-center/exploit-brokers-pay-500000-for-a-wordpress-rce-i-found-one-with-gpt5-6/
  - https://x.com/i/web/status/2099022295033684284
- **Notes:** [Researchy:A.11] Jul 20, 2026 Adam Kues / Searchlight Cyber. Extracted methodology only—deliberately omitted request bodies, SQL strings, and step-by-step attack procedures.

