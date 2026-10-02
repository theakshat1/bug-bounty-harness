# Researchy lane — Articles (deepened, non-repro)

**Audience:** Akshat (authorized / in-scope hunting only)  
**Lane:** Researchy (`/workspace/bb-bookmark-lane-researchy/`)  
**Items:** 12 articles  
**Constraint:** Expanded from existing lane extracts only. **No** reproduction steps, payloads, PoCs, exploit recipes, or attack procedures.

**Quality rollup:** ok=11 · thin=1 · blocked-recovered=0

---

### A.1 BugBountyHunting.com — Community FAQ & hunting resource

- **Root-cause class:** Educational FAQ covering XSS, IDOR, SSRF, SQLi, RCE classes
- **Affected component:** General web apps (educational taxonomy)
- **Impact:** Process/coverage improvement for authorized hunting; educational or platform meta rather than a single vuln impact.
- **Conditions called out:** Beginner / general web app hunting context; understanding input→output and access-control surfaces
- **What the write-up/tweet teaches (abstract):** Prioritize classic web classes by how user input reaches sinks: unencoded reflection (XSS variants stored/reflected/DOM), direct object identifiers without authz (IDOR), server-side URL fetchers (SSRF incl. cloud metadata), query construction from input (SQLi), and eval/command construction from strings/files (RCE). Treat FAQ-style class definitions as a checklist when mapping each endpoint’s trust boundaries. Extract note: Community-curated search/FAQ site; thin on novel research but useful class taxonomy for hunters. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** education, xss, idor, ssrf, sqli, rce, beginner, faq
- **Lane:** Researchy
- **Quality:** thin
- **Sources:**
- [https://BugBountyHunting.com](https://BugBountyHunting.com)
- X bookmark post: [2098301017989558495](https://x.com/i/web/status/2098301017989558495)
- **Notes:** Community-curated search/FAQ site; thin on novel research but useful class taxonomy for hunters.

---

### A.2 Adverserial AI docs — CyberKimi / CyberGLM OpenAI-compatible API

- **Root-cause class:** AI-assisted security workflows / offensive-tuned LLM API integration
- **Affected component:** Cyber-tuned LLM API product (analysis aid)
- **Impact:** Methodology / tooling impact: lower false positives, better token use, and stronger validation gates — not a single product CVE.
- **Conditions called out:** Prepaid wallet + API key; client that speaks OpenAI chat completions or Anthropic dialect (Claude Code, Codex, OpenCode, Hermes, Kimi Code)
- **What the write-up/tweet teaches (abstract):** Wire a security-specialized model into existing agent/CLI harnesses via a shim base URL rather than rebuilding tooling. Use model routing (cheap classify/summarize vs strong deep analysis), stream reasoning fields separately from final answers, and keep secrets out of client-side/shared images. Treat cyber-tuned models as assistants for triage, Sigma/rule drafting, and code review inside authorized scopes—not as autonomous exploit engines. Extract note: Product docs for CyberKimi/CyberGLM; privacy-first (no inference/session logs claimed); memberships + prepaid wallet. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** llm, cyberkimi, api, agent-tooling, claude-code, codex, opencode, privacy
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://adverserial.ai/docs.html](https://adverserial.ai/docs.html)
- X bookmark post: [2097060366652186927](https://x.com/i/web/status/2097060366652186927)
- **Notes:** Product docs for CyberKimi/CyberGLM; privacy-first (no inference/session logs claimed); memberships + prepaid wallet.

---

### A.3 Harnessing Harnesses — Climbing the LLM Hills (ZephrFish / Andy Gill)

- **Root-cause class:** LLM orchestration / AI security research harness design
- **Affected component:** Authorized codebases/binaries + coding-agent/MCP harness
- **Impact:** Scale without triage/dedupe quality increases duplicate and false-positive load.
- **Conditions called out:** Access to coding agents + optional MCPs; codebase or binary targets under authorization; ability to stage prompts and artefacts
- **What the write-up/tweet teaches (abstract):** Invest in the orchestration layer more than raw model choice: split work into recon→hunt→validate→trace→report with per-stage prompts and structured artefacts; give each stage only scoped context; use adversarial/validate agents that try to disprove findings; route cheap models for classify/summarize and strong models for validation/trace; add RAG memory of prior notes and a post-run feedback loop. Surveyed harness patterns: RAPTOR (static+dynamic+solver gates), Anthropic defending-code (ASAN-verified find/grade/patch), baby-naptime (runtime feedback loop), evilsocket/audit (8-stage trust-boundary + taint trace), Visa VVAH (threat-model first, triage candidates). Context budget discipline (summarize scanner noise; ~8K for single-function, ~32K for synthesis) beats dumping full repos into prompts. Extract note: Strong methodology piece; author also released ZephrFish/harness-kit template (recon→hunt→validate→trace→report). Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** llm-harness, orchestration, raptor, mcp, validation-gates, rag, token-budget, offensive-research
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://blog.zsec.uk/harnessing-harnesses/](https://blog.zsec.uk/harnessing-harnesses/)
- X bookmark post: [2097218639074070705](https://x.com/i/web/status/2097218639074070705)
- **Notes:** Strong methodology piece; author also released ZephrFish/harness-kit template (recon→hunt→validate→trace→report).

---

### A.4 Generic secret/key name regex gist (h4x0r-dz)

- **Root-cause class:** Secret / credential pattern matching (static secret hunting)
- **Affected component:** Source, configs, CI env dumps, JS bundles, public repos in scope
- **Impact:** Leaked credentials/secrets in readable sources when name-based detectors catch misnamed keys format-only tools miss.
- **Conditions called out:** Readable source, configs, CI env dumps, JS bundles, or public repos in scope
- **What the write-up/tweet teaches (abstract):** Hunt leaked credentials by matching high-signal key *names* (api_key, aws_secret, client_secret, db_password, cloudflare_api_key, etc.) near assignment operators rather than only known token formats. Broad name-based regexes catch misnamed or vendor-specific secrets that format-only detectors miss; combine with entropy/format validators and rotate-on-find hygiene. Useful as one layer in JS/env/.git history secret sweeps during recon. Extract note: Popular gist (129 forks / 60 comments); single large case-insensitive OR-list of credential-ish identifiers. Methodology extract only—do not treat as an exploit kit. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** secrets, regex, credential-leak, recon, gist, static-analysis
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://gist.github.com/h4x0r-dz/be69c7533075ab0d3f0c9b97f7c93a59](https://gist.github.com/h4x0r-dz/be69c7533075ab0d3f0c9b97f7c93a59)
- X bookmark post: [2097741657684971786](https://x.com/i/web/status/2097741657684971786)
- **Notes:** Popular gist (129 forks / 60 comments); single large case-insensitive OR-list of credential-ish identifiers. Methodology extract only—do not treat as an exploit kit.

---

### A.5 Ars0n Framework v2 — AI-native beginner bug-bounty methodology wrapper

- **Root-cause class:** End-to-end bug-bounty workflow automation / attack-surface mapping platform
- **Affected component:** Azure / Entra ID tenant surfaces (blob, vault, AKS paths as named)
- **Impact:** Process/coverage improvement for authorized hunting; educational or platform meta rather than a single vuln impact.
- **Conditions called out:** Docker Compose host; optional API keys for OSINT providers (SecurityTrails, Censys, Shodan, Whoxy, etc.); authorized targets only
- **What the write-up/tweet teaches (abstract):** Force a correct hunting order via UI-gated stages wrapping 50+ common tools (Amass, Subfinder, httpx, Katana, Nuclei, ffuf, GAU, cloud_enum, Naabu, GitHub recon, etc.), store results in a central DB for attack-surface visualization, and pair each stage with ‘Help Me Learn!’ lessons so beginners absorb the *why*. Pattern: methodology-as-product—make skipping recon hard; unify tool output; add MCP/AI assistant hooks for triage. Compete with pros by breadth of passive+active asset discovery and consistent process, not by skipping steps. Extract note: README via raw.githubusercontent.com; beta 0.1.0; ‘Earn While You Learn’ framing. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** framework, bug-bounty, recon, docker, beginner, mcp, attack-surface, rs0n
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://github.com/R-s0n/ars0n-framework-v2](https://github.com/R-s0n/ars0n-framework-v2)
- X bookmark post: [2097322316120437210](https://x.com/i/web/status/2097322316120437210)
- **Notes:** README via raw.githubusercontent.com; beta 0.1.0; ‘Earn While You Learn’ framing.

---

### A.6 cloudflare/security-audit-skill — multi-phase coding-agent security audit skill

- **Root-cause class:** Coverage-led AI code audit / adversarial finding verification
- **Affected component:** Codebases under authorized coding-agent audit
- **Impact:** Methodology / tooling impact: lower false positives, better token use, and stronger validation gates — not a single product CVE.
- **Conditions called out:** Coding agent with tool-use + parallel sub-agents; Node.js for validators; OS sandbox (no egress, allowlisted env, scratch-only writes) for any target-code execution
- **What the write-up/tweet teaches (abstract):** Run audits as six gated phases: (1) recon → architecture.md + coverage-ledger.json, (2) coverage-led hunting with isolated hunters + coverage critics, (3) fresh verifiers that try to *disprove* candidates, (4) structured findings (confirmed / needs_validation / rejected) against a schema, (5) independent record re-verification, (6) target-neutral reports. Confirm only established boundary failures with source traces; severity needs impact; defense-in-depth gaps alone are hardening notes. Repeat runs are additive against the ledger. Attack-class prompt packs span web/protocol/auth, client-side, supply-chain, cloud, RPC/messaging, resource exhaustion, data isolation, desktop/mobile IPC, memory-safety, and AI/LLM surfaces. Extract note: Seeds Cloudflare’s vulnerability harness blog; install via skills CLI. Strong defensive/research process design. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** cloudflare, agent-skill, code-audit, coverage-ledger, adversarial-validation, sarif-like, harness
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://github.com/cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill)
- X bookmark post: [2099473233787388049](https://x.com/i/web/status/2099473233787388049)
- **Notes:** Seeds Cloudflare’s vulnerability harness blog; install via skills CLI. Strong defensive/research process design.

---

### A.7 redhat-et/ripwire — ‘ripgrep of AI context’ call-graph CLI + MCP

- **Root-cause class:** Agent context compression / blast-radius & quality-delta tooling for code research
- **Affected component:** Local code repositories (agent context tooling)
- **Impact:** Tooling throughput / cost / hypothesis-assist impact; findings still need human verification in scope.
- **Conditions called out:** Local repo; optional MCP/agent skill install; no API key/embeddings/daemon required
- **What the write-up/tweet teaches (abstract):** Before agents dump whole files into context, give them a ranked deterministic map: callers/callees, edit blast radius, tests-to-run, quality deltas (what got worse), forgotten co-changes, and ambiguous name resolution—using signatures that are far smaller than bodies. For multi-agent security/code audits, lead with orientation/recall and close with edit-check + quality gates so fleets don’t silently diverge. Pattern: mechanical honesty floor for agent fleets (token savings + contract checks), not a substitute for bespoke measurement when hunting deep vulns. Extract note: Zero runtime deps C++23; multi-language; field report claims large token/orientation wins for orchestrated fleets. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** ripwire, mcp, call-graph, context-compression, multi-agent, quality-gate, redhat
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://github.com/redhat-et/ripwire](https://github.com/redhat-et/ripwire)
- X bookmark post: [2099206742647222583](https://x.com/i/web/status/2099206742647222583)
- **Notes:** Zero runtime deps C++23; multi-language; field report claims large token/orientation wins for orchestrated fleets.

---

### A.8 Oath Bug Bounty Program Update: $1M payouts and expansion (2018)

- **Root-cause class:** Bug-bounty program design / scope & payout policy (operator-side)
- **Affected component:** Bug-bounty program policy / scope (operator-side historical)
- **Impact:** Better hunt ROI via program activity, payout tables, and newly unified scopes (ops/planning impact, not a vuln).
- **Conditions called out:** N/A for hunters beyond being invited to the (then) private Oath program covering Tumblr/Yahoo/AOL/EdgeCast brands
- **What the write-up/tweet teaches (abstract):** From a researcher planning angle: programs that publish payout tables, expand in-scope vuln types by CVSS/impact, shorten triage SLAs, and unify previously private brand scopes reward steady engagement over moonshot-only hunting. Prioritize classes programs explicitly top-rank (here: SQLi, RCE, XXE/XMLi) while watching for newly opened assets when private sub-programs merge into a unified program. Historical signal that live-hacking events + continuous private programs compound attack-surface reduction. Extract note: Aug 23, 2018 post by Katrina Dene / Chris Nims; historical program ops lessons, not a vuln writeup. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** hackerone, program-policy, oath, payouts, scope, historical
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://hackerone.com/blog/oath-bug-bounty-program-update-1m-payouts-and-expansion-program](https://hackerone.com/blog/oath-bug-bounty-program-update-1m-payouts-and-expansion-program)
- X bookmark post: [2100981796192338406](https://x.com/i/web/status/2100981796192338406)
- **Notes:** Aug 23, 2018 post by Katrina Dene / Chris Nims; historical program ops lessons, not a vuln writeup.

---

### A.9 My Complete Bug Bounty Hunting Workflow — Every Command I Use, Step by Step (Hacker MD)

- **Root-cause class:** Repeatable BB workflow: recon → vuln hunt → business logic/API → secrets → reporting
- **Affected component:** Cloud object storage (S3-class) + app download/API path
- **Impact:** Leaked credentials/secrets in readable sources when name-based detectors catch misnamed keys format-only tools miss.
- **Conditions called out:** Authorized target; ProjectDiscovery suite + common recon tools installed; do not skip recon before exploitation
- **What the write-up/tweet teaches (abstract):** Execute a fixed pipeline every time: (1) multi-source subdomain enum (tool diversity + CT logs) → live host/tech-detect filter → deep URL collection (active crawl + historical indexes), (2) parameter extraction and pattern buckets (XSS/SQLi/SSRF/redirect/RCE-SSTI candidates) via templates and focused scanners—not random poking, (3) manual business-logic/API work (JWT/cookie trust, IDOR/UUID predictability, GraphQL introspection exposure), (4) secrets in JS bundles and leaked env/git artefacts, (5) evidence-first reporting. Core meta-rule: attack-surface size decides success odds; automation ends where business logic begins. Extracted as process patterns only—omit weaponized payload recipes. Extract note: WebFetch hit Cloudflare 403; recovered via curl (HTTP 200). Published ~2026-02-26 on InfoSec Write-ups. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** workflow, recon, projectdiscovery, idor, graphql, secrets, beginner, methodology
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://infosecwriteups.com/my-complete-bug-bounty-hunting-workflow-every-command-i-use-step-by-step-68484276471f](https://infosecwriteups.com/my-complete-bug-bounty-hunting-workflow-every-command-i-use-step-by-step-68484276471f)
- X bookmark post: [2098351354309722129](https://x.com/i/web/status/2098351354309722129)
- **Notes:** WebFetch hit Cloudflare 403; recovered via curl (HTTP 200). Published ~2026-02-26 on InfoSec Write-ups.

---

### A.10 When a Simple Google Dork Led to an S3 Misconfiguration and Sensitive Data Exposure

- **Root-cause class:** Cloud storage misconfiguration / sensitive data exposure via public listing + unsigned object serving
- **Affected component:** Cloud object storage (S3-class) + app download/API path
- **Impact:** Sensitive data / export exposure via public listing combined with unsigned object serving (as stated in write-up; ~$2k bounty noted in extract).
- **Conditions called out:** In-scope web app using object storage; indexed public files revealing bucket naming; ability to probe listing/ACL without auth (authorized testing)
- **What the write-up/tweet teaches (abstract):** Start large scopes with lightweight Google dorks for indexed PDFs/uploads (`site:*.target TLD filetype` style) to surface CDN/S3 path patterns in URLs. When path segments look like bucket names, check whether listing is open and whether the app’s download/API path serves objects without time-limited signed URLs or auth. Chain: public listing (filename oracle) + unauthenticated content fetch = PII/export exposure even if direct object-store GET is partially restricted. Prefer signed URLs, least-privilege bucket policies, and separate sensitive exports from public assets. Extract note: Author Amrul / Seek404; ~$2k bounty; methodology only—no copy of exposed data or attack scripts. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** s3, misconfiguration, google-dork, sensitive-data, cloud, yeswehack, recon
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://medium.com/@Seek404/when-a-simple-google-dork-led-to-an-s3-misconfiguration-and-sensitive-data-exposure-4d7d86f54b16](https://medium.com/@Seek404/when-a-simple-google-dork-led-to-an-s3-misconfiguration-and-sensitive-data-exposure-4d7d86f54b16)
- X bookmark post: [2096270617205162368](https://x.com/i/web/status/2096270617205162368)
- **Notes:** Author Amrul / Seek404; ~$2k bounty; methodology only—no copy of exposed data or attack scripts.

---

### A.11 Exploit brokers pay $500,000 for a WordPress RCE. I found one with GPT5.6 Sol Ultra (Searchlight Cyber)

- **Root-cause class:** LLM-assisted 0-day discovery; batch-API validate/execute desync; type-confused sanitization; privilege-escalation gadget chaining
- **Affected component:** WordPress (or similar CMS) — as framed in source
- **Impact:** High-impact code-audit findings (desync / sanitizer gaps / privilege gadgets) under authorized LLM-assisted review — PoCs deliberately omitted from extract.
- **Conditions called out:** Authorized source-code audit of WordPress (or similar) with multi-agent coding model; forbid changelog/diff cheating; require realistic pre-auth production constraints
- **What the write-up/tweet teaches (abstract):** Prompt/orchestrate multi-agent code audits with diverse approach portfolios, adversarial double-checks, and hard constraints (pre-auth, default config, no fabricated preconditions; encourage reading dependency source). High-level bug patterns to hunt—without reproducing PoCs: (1) APIs that validate in one loop and execute in another can desync when error paths push only one of two parallel arrays; (2) sinks that sanitize arrays but pass scalars through unsanitized; (3) nested/self-calls of batch endpoints that inherit broken validation assumptions; (4) after a read primitive, in-memory object caches + features that reconcile cache vs DB can become escalation gadgets; (5) temporary identity switches driven by attacker-influenced structured records; (6) dynamically named hooks/actions built from status×type strings. Meta lesson: as models do more chain-building, human value shifts to target selection, prompt heuristics, and steering. Extract note: Jul 20, 2026 Adam Kues / Searchlight Cyber. Extracted methodology only—deliberately omitted request bodies, SQL strings, and step-by-step exploit procedures. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** wordpress, llm-research, batch-api, desync, sqli-class, gadget-chain, searchlight, agentic
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://slcyber.io/research-center/exploit-brokers-pay-500000-for-a-wordpress-rce-i-found-one-with-gpt5-6/](https://slcyber.io/research-center/exploit-brokers-pay-500000-for-a-wordpress-rce-i-found-one-with-gpt5-6/)
- X bookmark post: [2099022295033684284](https://x.com/i/web/status/2099022295033684284)
- **Notes:** Jul 20, 2026 Adam Kues / Searchlight Cyber. Extracted methodology only—deliberately omitted request bodies, SQL strings, and step-by-step exploit procedures.

---

### A.12 Tsecbench — Tencent Offensive AI Agentic benchmark leaderboard

- **Root-cause class:** Offensive-AI / automated red-team agent capability benchmarking
- **Affected component:** Public offensive-AI agent benchmark platforms
- **Impact:** Calibration of agent harness strategies via public leaderboards (evaluation meta).
- **Conditions called out:** Public SPA/API access; agents submitted under platform rules; cheat-disclosure process exists
- **What the write-up/tweet teaches (abstract):** Use public offensive-AI benchmarks to compare agent harnesses across capability domains rather than chasing single demos. Tsecbench frames Agentic red-team scoring across real CVE/production-like and cloud-native tasks; related sets include XBOW Validation Benchmarks (web CTF-style) and Cybench (crypto/web/RE/vuln CTF tasks). For researchers: track leaderboard + capability-stats + cheat-disclosures to calibrate which multi-agent strategies generalize; treat benchmarks as evaluation of hunting workflows (recon, chaining, evasion) not as attack manuals. Extract note: WebFetch returned empty (client-rendered SPA); recovered via curl + /api/v1/benchmark-sets and leaderboard. Default home set_id=4 (Tsecbench v1). Zh title: 智能攻防 AI 跑分基准平台. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** tsecbench, benchmark, offensive-ai, leaderboard, xbow, cybench, tencent, agentic
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://tsecbench.zc.tencent.com/#leaderboard](https://tsecbench.zc.tencent.com/#leaderboard)
- X bookmark post: [2096897731168268635](https://x.com/i/web/status/2096897731168268635)
- **Notes:** WebFetch returned empty (client-rendered SPA); recovered via curl + /api/v1/benchmark-sets and leaderboard. Default home set_id=4 (Tsecbench v1). Zh title: 智能攻防 AI 跑分基准平台.
