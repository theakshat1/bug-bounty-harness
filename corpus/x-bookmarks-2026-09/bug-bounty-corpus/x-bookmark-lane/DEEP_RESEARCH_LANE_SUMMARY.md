# Deep Research lane — X bookmarks (≥2026-09-02) — 22 items

Status: **complete** · ok=19 · thin=3 · blocked=0 · error=0
Blocked URLs: **none**
Thin (outcome/tooling-only, limited technique detail): 18, 19, 22

Per item: source · vuln class/technique · preconditions · generalized hunting idea · tags

### 1. [ARTICLE] Adverserial AI — Intelligence, engineered for cyber (CyberKimi / CyberGLM)
- **source:** https://adverserial.ai
- **status:** ok
- **vuln class/technique:** n/a-tooling
- **preconditions:** Access to specialized cyber-tuned LLM APIs (CyberKimi/CyberGLM) or similar security-focused models; Security context inputs: code, logs, artifacts for analysis workflows
- **generalized hunting idea:** Domain-specialized LLMs for security can support detection engineering, IR timeline reconstruction, and threat-hunt hypothesis generation when fed logs/code/artifacts—treat as an analysis aid with privacy and verification constraints, not an autonomous exploit engine.
- **tags:** llm-security-tooling, detection-engineering, threat-hunting, cyberkimi, api-product

### 2. [ARTICLE] Jenny was a Friend of Mine - MCPs and Friends (Autonomous Vulnerability Hunting with MCP)
- **source:** https://blog.zsec.uk/bullyingllms/
- **status:** ok
- **vuln class/technique:** LLM/MCP-orchestrated vuln hunting; grammar-based fuzzing; patch-diff campaigns; auth-bypass/SSRF/OEM chains (high-level methodology)
- **preconditions:** Isolated research lab (e.g., Proxmox VMs) with target and analysis hosts; MCP-wrapped RE/fuzz/debug/reporting tools and persistent campaign storage; Human validation gates before any disclosure/submission
- **generalized hunting idea:** Wrap the research toolchain as MCP tools, organize work as campaigns, force every LLM finding through a hallucination→validated promotion pipeline (PoC existence, clean-snapshot reproduce, exploitability, low-priv reachability), and feed crashes/defenses/bounty ROI back into RAG so later hunts skip hardened dead-ends and favor under-scrutinized high-ROI targets.
- **tags:** mcp, autonomous-hunting, hallucination-gates, rag-feedback, patch-diff, fuzzing, bounty-roi, methodology

### 3. [ARTICLE] Needle in the haystack: LLMs for vulnerability research
- **source:** https://devansh.bearblog.dev/needle-in-the-haystack/
- **status:** ok
- **vuln class/technique:** LLM-assisted code audit methodology; authz boundary bugs; JWT/JWKS algorithm confusion; signature validation flaws; CI egress-control gaps (pattern-level)
- **preconditions:** Readable target source (OSS or authorized audit scope); Prior CVE/advisory history or architectural threat model for the project; Verifier loop (tests, builds, harnesses) to confirm model claims
- **generalized hunting idea:** Avoid bloated AGENT.md scaffolds and 'find all vulns' prompts (context rot). Use minimal scaffolding: derive a one-page threat model from past CVEs and trust boundaries, audit thin slices (auth, JWT, cookies, sandbox egress), demand call-chain evidence, and spend most tokens on slice exploration + verification—not prompt bureaucracy.
- **tags:** llm-audit, threat-model, context-rot, minimal-scaffolding, authz, jwt, ci-security, prompt-patterns

### 4. [ARTICLE] OWASP MCP Security Taxonomy
- **source:** https://github.com/OWASP/MCP-Taxonomy
- **status:** ok
- **vuln class/technique:** n/a-meta
- **preconditions:** Building, reviewing, or threat-modeling MCP hosts/clients/servers/gateways; Need for shared vocabulary across AppSec, AI security, and GRC
- **generalized hunting idea:** Use a vendor-neutral MCP risk taxonomy (relationship map, OWASP MCP Top 10 mapping, root-cause tags like INJ-CMD/SSRF/AUTH-BYPASS/X-TENANT) to structure reviews of agent tools, transport, and backend trust boundaries instead of ad-hoc checklists.
- **tags:** owasp, mcp, taxonomy, threat-modeling, ai-security, reference

### 5. [ARTICLE] Awesome Agent Orchestrators
- **source:** https://github.com/andyrewlee/awesome-agent-orchestrators
- **status:** ok
- **vuln class/technique:** n/a-tooling
- **preconditions:** Need to run/supervise multiple coding or research agents (worktrees, loops, swarms); Interest in harness patterns for long-running autonomous tasks
- **generalized hunting idea:** Curated catalog of agent orchestrators (parallel coding agents, swarms, autonomous loop/task runners, infrastructure primitives) helps researchers pick harnesses for multi-agent security workflows—isolation via worktrees/sandboxes, verification gates, and human approval inboxes matter more than raw agent count.
- **tags:** awesome-list, agent-orchestrators, multi-agent, harness, tooling

### 6. [ARTICLE] Cadence — experimental learning library (flat/deep/recursive patch nets)
- **source:** https://github.com/muellerberndt/cadence
- **status:** ok
- **vuln class/technique:** n/a-tooling
- **preconditions:** Python 3.11+ environment for experimental learning/agent research; Interest in alternative learning architectures (not a vuln writeup)
- **generalized hunting idea:** Cadence is an experimental 'brain' library (bounded patches, settlement, recursive error feedback) for learning routines—relevant only as adjacent agent/ML tooling research, not as a security vulnerability technique.
- **tags:** ml-library, agents, experimental, learning, n/a-security-writeup

### 7. [ARTICLE] Chat On Steroids — local MCP capabilities for ChatGPT
- **source:** https://github.com/totec448-spec/chat-on-steroids
- **status:** ok
- **vuln class/technique:** n/a-tooling
- **preconditions:** ChatGPT account with MCP app capability; local desktop install; Approved project folders and reviewed local tool permissions
- **generalized hunting idea:** Local MCP + browser companion patterns let chat models operate on real files/terminals/workers—for security research tooling, emphasize permission scoping, provider rule compliance, and human supervision; do not use local tools to override safety refusals.
- **tags:** mcp, chatgpt, local-tools, multi-agent, tooling, desktop

### 8. [ARTICLE] Zaevlad/audit-findings-dataset — Smart Contract Audit Findings (viewer)
- **source:** https://huggingface.co/datasets/Zaevlad/audit-findings-dataset/viewer
- **status:** ok
- **vuln class/technique:** n/a-meta
- **preconditions:** Interest in smart-contract audit pattern mining / model training data prep; Willingness to clean/dedupe/normalize raw semi-structured findings first
- **generalized hunting idea:** Large corpora of labeled audit findings (title, description, severity, recommendations; often Solidity) can seed threat models and pattern libraries for web3 reviews—use for classification and invariant brainstorming after cleaning; treat embedded PoC fields as dataset content to study patterns, not as ready-to-run attack recipes.
- **tags:** dataset, smart-contracts, solidity, audit-findings, web3, training-data

### 9. [ARTICLE] Leaking MTN Customer PII & Order History via IDOR on a Ticket Management Domain
- **source:** https://medium.com/@4osp3l/leaking-mtn-customer-pii-order-history-via-idor-on-a-ticket-management-domain-cd3306e36e29?postPublishedType=initial
- **status:** ok
- **vuln class/technique:** IDOR / broken object-level authorization; JS/sourcemap recon leading to hidden API surface
- **preconditions:** In-scope (or accepted) assets under org control, including ticket/management subdomains referenced from JS; Ability to harvest JS/source maps and enumerate backend API routes; Public or weakly gated endpoints that reveal object identifiers (e.g., event creator UUIDs)
- **generalized hunting idea:** After subdomain enum, recursively harvest JS and source maps for hidden domains and full API route maps; when a 'public' endpoint leaks object IDs (UUIDs), cross-check other routes that take the same ID for missing authz (classic IDOR chaining). Expand surface to org-managed ticket/ops domains that may still be in bounty scope.
- **tags:** idor, bola, js-recon, sourcemaps, api-enumeration, pii, bug-bounty

### 10. [ARTICLE] How I Got AWS Secret Keys from Exposed Variables in JS File
- **source:** https://medium.com/@mohameddiv77/how-i-got-aws-secret-keys-from-exposed-variables-in-js-file-c67f61039da6
- **status:** ok
- **vuln class/technique:** Client-side secret exposure; Cognito User Pool / Identity Pool misconfiguration leading to temporary AWS credentials
- **preconditions:** JS bundles (and especially source maps) on in-scope hosts exposing Cognito pool/client/identity IDs; Cognito flows that allow signup/auth and identity pools with usable IAM roles for authenticated users; Authorized bug-bounty testing of the affected program
- **generalized hunting idea:** On SPA/dev subdomains, mine JS and reconstructed source maps for cloud identity config (Cognito userPoolId, clientId, identityPoolId). Assess whether exposed client config plus open signup/auth can obtain temporary cloud credentials and what IAM permissions those roles grant—report exposure and over-permissioned identity pools; do not use obtained access beyond authorized proof.
- **tags:** aws, cognito, js-secrets, sourcemaps, credential-exposure, bug-bounty, misconfiguration

### 11. [ARTICLE] From Patch to Exploit; Using Claude Code to reverse engineer a zero-day in Papercut NG
- **source:** https://techanarchy.net/from-patch-to-exploit-using-claude-code-to-reverse-engineer-a-zero-day-in-papercut-ng/
- **status:** ok
- **vuln class/technique:** N-day / patch-diff research with LLM harness; authz filter vs dispatcher path-normalization mismatches; multi-bug chain analysis (high-level methodology only)
- **preconditions:** Public advisory/IoCs and access to vulnerable vs patched builds for authorized lab analysis; Isolated lab (VM snapshots) plus RE tools (decompiler, browser automation) orchestrated carefully; Human skepticism: challenge agent assumptions and demand end-to-end lab validation
- **generalized hunting idea:** For freshly patched, actively exploited products: stand up vulnerable and patched labs, patch-diff from IoC strings to changed auth/SQL sinks, hunt systematic auth-check mismatches (filter normalization vs router semantics; page/service context confusion), and keep pushing the model when a chain is incomplete. After vendor patches, re-sweep the same bug classes for residual bypasses—without publishing exploit recipes.
- **tags:** n-day, patch-diff, llm-harness, auth-bypass-patterns, java, enterprise-software, methodology

### 12. [POST] BRuteLogic (Brute)
- **source:** https://x.com/BRuteLogic/status/2105307679640223925
- **status:** ok
- **vuln class/technique:** Path traversal filter bypass (null-byte termination, strip-evasion, nested percent-decoding, length truncation)
- **preconditions:** App accepts user-controlled file/path parameters and applies naive blacklist/normalization; Downstream consumer may stop at NUL, re-decode, strip '../' once, or truncate long paths
- **generalized hunting idea:** When path or file upload/download params are filtered, probe classes of filter mistakes: early string termination, single-pass strip of '../', incomplete multi-layer URL decoding, and fixed-buffer truncation that drops the filter suffix while leaving a dangerous prefix. Map each class to how the language/runtime and reverse proxy normalize paths before access checks.
- **tags:** path-traversal, lfi, filter-bypass, encoding, null-byte, truncation, bug-bounty

### 13. [POST] immunefi
- **source:** https://x.com/immunefi/status/2102010814442181024
- **status:** ok
- **vuln class/technique:** Research methodology / AI-assisted hunting (career + process, not a single vuln class)
- **preconditions:** Active bug-bounty or Immunefi-style program access; Willingness to systematize hunting with AI as a force multiplier, not a replacement for validation
- **generalized hunting idea:** Study high-earning researchers' process: how they onboard to a program, where AI helps surface candidates, and how they validate/report. Prefer methodology interviews over tool hype; treat AI as a triage and pattern-matching aid that still needs human confirmation of impact.
- **tags:** methodology, AI-assisted-hunting, immunefi, career, bug-bounty

### 14. [POST] wtf_yodhha (Brut)
- **source:** https://x.com/wtf_yodhha/status/2099388849772466557
- **status:** ok
- **vuln class/technique:** Newline / control-character injection in JSON email fields (password-reset multi-recipient logic flaw)
- **preconditions:** Password-reset (or similar) API accepts JSON with an email string; Backend or mail layer may split on newlines/control chars without validating a single address
- **generalized hunting idea:** On auth flows that take an email in JSON, test whether control characters (especially newlines) inside the string cause the mailer or parser to treat multiple addresses as recipients. Confirm impact only by observing whether reset material reaches an unintended inbox you control under program rules—not by broadcasting tokens.
- **tags:** password-reset, JSON-injection, newline-injection, ATO, input-validation, bug-bounty-tips

### 15. [POST] bountywriteups
- **source:** https://x.com/bountywriteups/status/2099143734369690104
- **status:** ok
- **vuln class/technique:** Autonomous AI pentest tooling with independent verification loop (tooling pattern)
- **preconditions:** Self-hosted environment and bring-your-own LLM; Authorized scope for automated testing
- **generalized hunting idea:** Prefer scanners/agents that separate 'detect' from 'prove': an autonomous hunter plus an independent verifier that re-checks findings before reporting reduces false-positive triage load. Useful pattern for private, self-hosted AI-assisted testing stacks (Go + TypeScript example: Xalgorix).
- **tags:** AI-pentester, tooling, verification, false-positives, open-source, xalgorix

### 16. [POST] vortexau (vortex)
- **source:** https://x.com/vortexau/status/2098892189250343336
- **status:** ok
- **vuln class/technique:** Responsible PoC hygiene for asset takeover (S3/subdomain-style) — reporting practice, not a new vuln class
- **preconditions:** You demonstrated control of a misconfigured public asset (e.g. abandoned bucket/host); Program customers or third parties could stumble on a flashy public PoC page
- **generalized hunting idea:** For takeover-style proofs, minimize public scare surface: blank/minimal page, proof only in an HTML comment (optionally encoded), include your platform handle to deter claim-theft, and put decoding instructions in the private report so triage can verify without normies panicking.
- **tags:** responsible-disclosure, PoC-hygiene, S3-takeover, subdomain-takeover, reporting, HackerOne

### 17. [POST] forefy
- **source:** https://x.com/forefy/status/2098160999719211488
- **status:** ok
- **vuln class/technique:** Burp Suite Montoya API re-exposed as localhost OpenAPI for AI-agent workflows (tooling bridge)
- **preconditions:** Burp Suite with extension support (Montoya API); Local AI agents that can call REST/OpenAPI
- **generalized hunting idea:** When vendor MCP/APIs underserve UI power, a thin extension that re-exports internal APIs over localhost can let agents drive scans, sitemap walks, websocket tooling, CSRF-PoC helpers, and other extensions. Hunt pattern: invest in tooling bridges that unlock interactive proxy workflows for automation under authorized scope.
- **tags:** burp, reburp, AI-agents, MCP, tooling, openapi, pentest-workflow

### 18. [POST] X_cryptographer
- **source:** https://x.com/X_cryptographer/status/2097729338926154046
- **status:** thin
- **vuln class/technique:** Cryptographic issue enabling WAF bypass around encrypted login (title only; no method detail)
- **preconditions:** Target behind WAF with encrypted/login-related surface; Insufficient public detail in post to reconstruct technique
- **generalized hunting idea:** When celebrating AI-assisted wins, extract only the vuln theme from titles/screenshots (here: crypto + WAF + login). Treat as a reminder to review cryptographic construction of auth/login envelopes for ways encoding or wrapping interacts with WAF inspection—without inventing steps not present in the post.
- **tags:** HackerOne, WAF-bypass, cryptography, login, AI-assisted, thin

### 19. [POST] 0xManan (!Manan)
- **source:** https://x.com/0xManan/status/2097230196252500043
- **status:** thin
- **vuln class/technique:** AI harness / agent chaining culminating in RCE claim (outcome post; method not disclosed)
- **preconditions:** Custom AI security harness fine-tuned by author; Authorized target; production claim in media is redacted
- **generalized hunting idea:** Fine-tuning an agent harness and chaining findings toward higher impact is a workflow theme (agent → validate → escalate). Post is outcome-only; use it as motivation to build verification loops, not as a recipe—no chaining steps or payloads are published.
- **tags:** RCE, AI-harness, agent-workflow, thin, outcome-only

### 20. [POST] unknown0x3a (Unknown)
- **source:** https://x.com/unknown0x3a/status/2096959661446746168
- **status:** ok
- **vuln class/technique:** IDOR / BOLA discovery via report-trained agent skill + client-side JS analysis
- **preconditions:** Prior personal reports used as training material for a reusable 'skill'; Target exposes JS that reveals API shapes; low-priv session available
- **generalized hunting idea:** Codify your past IDOR lessons into a reusable agent skill (rules, bypass notes, training docs), then point it at live JS/API surfaces to find authorization gaps you previously missed. Especially check list/search endpoints that return other users' PII/RBAC metadata under a low-priv session while anon correctly 403s.
- **tags:** IDOR, BOLA, JS-analysis, AI-skill, access-control, bug-bounty-tips

### 21. [POST] 7h3h4ckv157
- **source:** https://x.com/7h3h4ckv157/status/2096654287162245122
- **status:** ok
- **vuln class/technique:** Agentic SAST / secure-coding feedback for AI-generated code (defensive tooling pattern)
- **preconditions:** Codebase or AI-agent-produced patches available locally; Desire for plain-language + business-cost framing over CVE-only output
- **generalized hunting idea:** Pair code-writing agents with a second agentic security pass that explains issues in plain English, estimates dollar impact, and re-verifies fixes before writing to disk. Useful both for defending your own AI-written code and for prioritizing remediation language in reports.
- **tags:** agentic-security, SAST, AI-code, verification, open-source, tooling

### 22. [POST] mikenevermiss (MIKE)
- **source:** https://x.com/mikenevermiss/status/2096513894395043943
- **status:** thin
- **vuln class/technique:** General-purpose local AI agent (DeerFlow) — tangential to bug bounty; no vuln technique
- **preconditions:** Local or cloud LLM; willingness to run open-source agent with isolated task envs
- **generalized hunting idea:** General agent platforms (research, code, media) can support recon/note-taking workflows if sandboxed, but this post does not teach a security vuln class. Keep isolation/sandbox claims in mind when evaluating agent tooling for security work; do not treat marketing feature lists as hunting methodology.
- **tags:** DeerFlow, AI-agent, open-source, tooling, tangential, thin

## Cross-cutting patterns (this lane)
- **JS/sourcemap recon → IDOR/secrets:** harvest bundles/maps for hidden APIs, UUIDs, Cognito/AWS client config (#9, #10, #20).
- **LLM hunting loops need gates:** hallucination→validate→promote; detect-then-prove; minimal threat-model scaffolding (#2, #3, #11, #15).
- **Authz / filter mismatches:** path-normalization vs checks; path-filter bypass classes; password-reset control-char parsing (#11, #12, #14).
- **MCP/agent tooling meta:** OWASP MCP taxonomy, orchestrators, Burp↔agent bridges (#4–7, #17).
- **Web3 audit corpus:** HF ~23.6k findings for pattern mining (#8).
- **PoC hygiene:** minimal public takeover PoCs (#16).

Artifacts: `/workspace/bug-bounty-corpus/x-bookmark-lane/deep_research_{articles,posts}.{jsonl,md}`