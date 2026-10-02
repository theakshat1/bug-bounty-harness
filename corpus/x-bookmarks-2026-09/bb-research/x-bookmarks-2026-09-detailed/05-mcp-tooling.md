# MCP / Agent tooling meta

**Cluster file:** `05-mcp-tooling.md`  
**Audience:** Akshat (authorized / in-scope hunting only)  
**Constraint:** Abstract methodology only — **no** reproduction steps, payloads, PoCs, exploit recipes, Intruder setups, or attack procedures.  
**Items in this cluster:** 7

---

### 5.1 OWASP MCP Security Taxonomy

- **Root-cause class:** n/a-meta (shared vocabulary for MCP threat modeling)
- **Affected component:** MCP hosts, clients, servers, gateways, transport, and backend trust boundaries (taxonomy scope)
- **Impact:** n/a (not a vulnerability report)
- **Conditions called out:** Building, reviewing, or threat-modeling MCP hosts/clients/servers/gateways; Need for shared vocabulary across AppSec, AI security, and GRC
- **What the source teaches (abstract):** OWASP reference project providing a vendor-neutral MCP security taxonomy: relationship maps, OWASP MCP Top 10 mapping, and root-cause tags such as injection, SSRF, auth bypass, and cross-tenant classes. Aimed at security engineers, developers, GRC, and researchers who need common language for agent-tool and transport risks. It is a structuring aid for reviews, not a single-product vulnerability writeup. Pattern: Use a shared MCP risk taxonomy (component map + Top 10 + root-cause tags) to structure reviews of agent tools, transport, and backend trust boundaries instead of ad-hoc checklists.
- **Tags:** owasp, mcp, taxonomy, threat-modeling, ai-security, reference
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://github.com/OWASP/MCP-Taxonomy
  - https://x.com/i/web/status/2096312505907757265
- **Notes:** [Deep Research:4] n/a-meta reference resource.

---

### 5.2 Ripwire: call-graph / blast-radius before dumping context

- **Root-cause class:** Agent context compression / blast-radius & quality-delta tooling for code research
- **Affected component:** Local code repositories (agent context tooling)
- **Impact:** Tooling throughput / cost / hypothesis-assist impact; findings still need human verification in scope.
- **Conditions called out:** Local repo; optional MCP/agent skill install; no API key/embeddings/daemon required
- **What the source teaches (abstract):** Before agents dump whole files into context, give them a ranked deterministic map: callers/callees, edit blast radius, tests-to-run, quality deltas (what got worse), forgotten co-changes, and ambiguous name resolution—using signatures that are far smaller than bodies. For multi-agent security/code audits, lead with orientation/recall and close with edit-check + quality gates so fleets don’t silently diverge. Pattern: mechanical honesty floor for agent fleets (token savings + contract checks), not a substitute for bespoke measurement when hunting deep vulns. Extract note: Zero runtime deps C++23; multi-language; field report claims large token/orientation wins for orchestrated fleets. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** ripwire, mcp, call-graph, context-compression, multi-agent, quality-gate, redhat
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://github.com/redhat-et/ripwire
  - https://x.com/i/web/status/2099206742647222583
- **Notes:** [Researchy:A.7] Zero runtime deps C++23; multi-language; field report claims large token/orientation wins for orchestrated fleets.

---

### 5.3 Awesome Agent Orchestrators catalog

- **Root-cause class:** n/a-tooling (harness selection meta)
- **Affected component:** Multi-agent harnesses / orchestrators (worktrees, swarms, loop runners, infra primitives)
- **Impact:** n/a (not a vulnerability report)
- **Conditions called out:** Need to run or supervise multiple coding or research agents; Interest in harness patterns for long-running autonomous tasks
- **What the source teaches (abstract):** Curated awesome-list of agent orchestrators grouped into parallel coding agents, swarms, autonomous loop/task runners, infrastructure primitives, and personal assistants. Common patterns called out include git worktrees, durable sessions, verification/approval gates, and remote supervision. Useful meta-resource when designing LLM-assisted hunting pipelines; not a vulnerability report. Pattern: When designing multi-agent security workflows, prioritize isolation (worktrees/sandboxes), verification gates, and human approval inboxes over raw agent count.
- **Tags:** awesome-list, agent-orchestrators, multi-agent, harness, tooling
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://github.com/andyrewlee/awesome-agent-orchestrators
  - https://x.com/i/web/status/2096878410920312970
- **Notes:** [Deep Research:5] n/a-tooling catalog.

---

### 5.4 Local MCP + chat companion permission scoping

- **Root-cause class:** n/a-tooling (local MCP capabilities for chat models)
- **Affected component:** ChatGPT + local MCP desktop bridge (files, shell, workers, Goal/Loop workflows)
- **Impact:** n/a (not a vulnerability report)
- **Conditions called out:** ChatGPT account with MCP app capability and local desktop install; Approved project folders and reviewed local tool permissions
- **What the source teaches (abstract):** Project that bridges ChatGPT to local files, shell, workers, and Goal/Loop-style workflows via MCP, plus a browser companion pattern. README stresses responsible use: permission scoping, provider rule compliance, and not using local tools to override safety refusals. Tooling-adjacent for agentic research setups; not a vulnerability writeup. Pattern: Local MCP + browser companion setups should emphasize permission scoping, provider compliance, and human supervision; do not use local tools to override safety refusals.
- **Tags:** mcp, chatgpt, local-tools, multi-agent, tooling, desktop
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://github.com/totec448-spec/chat-on-steroids
  - https://x.com/i/web/status/2096596480874127450
- **Notes:** [Deep Research:7] n/a-tooling; responsible-use emphasis in source extract.

---

### 5.5 Burp Montoya re-exported as localhost OpenAPI for agents

- **Root-cause class:** n/a (tooling bridge: Burp Montoya → localhost OpenAPI)
- **Affected component:** Burp Suite extension surface (Montoya API) re-exported for local AI agents
- **Impact:** n/a (not a vulnerability report)
- **Conditions called out:** Burp Suite with extension support (Montoya API); Local AI agents that can call REST/OpenAPI
- **What the source teaches (abstract):** Announcement of reburp, an extension that exposes Burp Montoya capabilities over a localhost OpenAPI REST API so AI agents can drive interactive proxy workflows. Claimed gaps versus stock Burp API/MCP include fuller UI workflows (scan control, sitemap, websockets, helpers, other extensions). Tooling bridge for authorized automation, not a vulnerability writeup. Pattern: When vendor MCP/APIs underserve UI power, thin localhost bridges that re-export internal APIs can unlock interactive proxy workflows for agents under authorized scope.
- **Tags:** burp, reburp, AI-agents, MCP, tooling, openapi, pentest-workflow
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://x.com/forefy/status/2098160999719211488
- **Notes:** [Deep Research:17] Tooling bridge; no attack procedures.

---

### 5.6 Agentic SAST pass on AI-written code (plain-language + re-verify)

- **Root-cause class:** Agentic SAST / secure-coding feedback for AI-generated code (defensive)
- **Affected component:** Local codebase or AI-agent-produced patches reviewed by a second security agent
- **Impact:** n/a (not a vulnerability report)
- **Conditions called out:** Codebase or AI-agent-produced patches available locally; Desire for plain-language plus business-cost framing over CVE-only output
- **What the source teaches (abstract):** Post about Agentic Security: a defensive tooling pattern that scans AI-written or whole-repo code, explains issues in plain English with dollar-cost framing, and re-verifies fixes before writing to disk. Useful for defending AI-written code and for remediation language in reports. Open-source tooling announcement, not a vulnerability writeup. Pattern: Pair code-writing agents with a second agentic security pass that explains issues plainly, estimates business impact, and re-verifies fixes before touching disk.
- **Tags:** agentic-security, SAST, AI-code, verification, open-source, tooling
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://x.com/7h3h4ckv157/status/2096654287162245122
- **Notes:** [Deep Research:21] Defensive tooling; not a vuln report.

---

### 5.7 DAST: crawl + JS + API + replay evidence in one workflow

- **Root-cause class:** DAST / crawl-assisted recon tooling
- **Affected component:** Authorized HTTP/browser targets (DAST workflow)
- **Impact:** Evidence-oriented findings vs one-off scans when crawl/JS/API/replay stay in one workflow.
- **Conditions called out:** Authorized target; ability to run local CLI scanner
- **What the source teaches (abstract):** Combine HTTP + browser-assisted crawling, JS analysis, API import, and replayable evidence into one workflow so findings stay evidence-oriented instead of one-off scans. Extract note: Promotes AKCA Go DAST scanner (github.com/akha-security/akca). Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** DAST, crawling, JS-analysis, AKCA, tooling
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://x.com/bountywriteups/status/2103890018670616715
- **Notes:** [Researchy:P.2] Promotes AKCA Go DAST scanner (github.com/akha-security/akca).

