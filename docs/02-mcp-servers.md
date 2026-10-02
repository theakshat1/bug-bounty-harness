# 02 — MCP Server Catalog (with risk ratings)

> Verified 2026-10-02. Every entry carries a maintenance date and a risk rating,
> because in this ecosystem **an abandoned offensive-tooling MCP server is a
> supply-chain liability, not a convenience.**

**The one architectural rule, before anything else:**

> **Never combine a target-touching server with a data-bearing or write-capable
> server in the same session.** Toxic data flows are ~37% of real MCP findings
> and ~100% of the ways an agentic hunter gets banned. A prompt-injected response
> from the target you are testing is how an agent gets retargeted at assets you
> are not authorized to touch.

---

## 2.1 The recommended stack

Start here. This is a small, boring, maintained set — which is the point.

| Server | Why | Risk |
|---|---|---|
| **Burp Suite MCP (official)** | The control plane. Proxy history, Repeater, Collaborator OAST. | Medium — see §2.2 |
| **HackerOne MCP (official)** | Program/scope/report data, **read-only by construction**. | **Lowest in this document** |
| **Semgrep MCP** (local stdio) | Code analysis, runs entirely on your machine. | Low |
| **Chrome DevTools MCP** or **Playwright MCP** | Client-side validation — proving XSS actually executes. | Medium — profile isolation required |
| **Censys / Shodan (official)** | Passive recon, scoped read keys. | Low security risk; **credit-burn risk is real** |
| **pd-mcp** (optional) | ProjectDiscovery recon with `confirm:true` gating and no-shell spawns. | Low by design, unproven by adoption |

Everything else in this document is either situational or a cautionary tale.

---

## 2.2 Burp Suite MCP Server — OFFICIAL (the anchor tool)

| | |
|---|---|
| BApp | https://portswigger.net/bappstore/9952290f04ed4f628e624d0aa9dccebc |
| Source | https://github.com/PortSwigger/mcp-server |
| Version | **1.3.0, updated 2026-05-28** — vendor-maintained |
| Transport | SSE on `http://127.0.0.1:9876`; bundled `mcp-proxy-all.jar` for stdio-only clients |
| Requires | Java on PATH. Burp **Community** works for most tools; **Professional required** for Collaborator + scanner issues |

Also now a first-class feature of **Burp Suite DAST 2026.8.2** (2026-08-27) — a
separate server-side MCP for scan/issue orchestration with API-key auth.

### 27 tools, grouped
- **HTTP:** `send_http1_request`, `send_http2_request`
- **Repeater/Intruder:** `create_repeater_tab`, `create_repeater_tab_http2`, `send_to_intruder`
- **Proxy history:** `get_proxy_http_history`, `get_proxy_http_history_regex`,
  `get_proxy_websocket_history`, `get_proxy_websocket_history_regex` (paginated)
- **Organizer:** `get_organizer_items`, `get_organizer_items_regex`
- **Pro only:** `get_scanner_issues`, `generate_collaborator_payload`,
  `get_collaborator_interactions`
- **Config (dangerous):** `output_project_options`, `output_user_options`,
  `set_project_options`, `set_user_options`
- **Control:** `set_task_execution_engine_state`, `set_proxy_intercept_state`
- **Editor:** `get_active_editor_contents`, `set_active_editor_contents`
- **Utils:** encode/decode helpers, `generate_random_string`

### Install
```bash
# 1. BApp Store → "MCP Server" → install. Burp → MCP tab → Enable.
# 2. In the MCP tab: set the auto-approve target allowlist, and
#    LEAVE "allow config editing" OFF.
# 3. Register with Claude Code:
claude mcp add --transport sse burp http://127.0.0.1:9876/sse

# Fallback if SSE is unavailable:
claude mcp add burp -- java -jar /path/to/mcp-proxy-all.jar --sse-url http://127.0.0.1:9876
```

### Risk and hardening — read this
1. **`set_project_options` / `set_user_options` are the sharp edge.** They merge
   arbitrary JSON into Burp config. A prompt-injected agent could flip your
   upstream proxy, your scope, or your intercept rules. **Disable config editing
   in the MCP tab and deny the tools explicitly.**
2. **`get_proxy_http_history` is a prompt-injection firehose.** It returns raw
   attacker-influenced response bodies directly into your context. Prefer the
   `*_regex` variants with tight `count`/`offset` over bulk dumps.
3. **Never auto-approve `*`.** Scope auto-approve to your target.
4. PortSwigger notes data sent to external AI clients falls under those vendors'
   data-processing policies — relevant for private-program and NDA'd traffic.
5. No HTTP/3, no WebSocket *sending*, no scanner *launch* in the desktop extension.

Recommended permission block:
```json
{
  "permissions": {
    "allow": [
      "mcp__burp__get_proxy_http_history_regex",
      "mcp__burp__send_http1_request",
      "mcp__burp__send_http2_request",
      "mcp__burp__generate_collaborator_payload",
      "mcp__burp__get_collaborator_interactions"
    ],
    "deny": [
      "mcp__burp__set_project_options",
      "mcp__burp__set_user_options",
      "mcp__burp__set_proxy_intercept_state",
      "mcp__burp__set_active_editor_contents"
    ]
  }
}
```

**Allowlist individual MCP tools, never a whole server.** This is your main
defense against toxic flows, because it breaks the chain at the capability level
instead of relying on the model's judgment.

---

## 2.3 BurpMCP (community alternative) — swgee

https://github.com/swgee/BurpMCP · MIT · SSE `:8181` + `stdio-bridge.py` ·
**last commit 2026-01-21 — ~8 months idle**

Philosophically different and worth knowing: **opt-in data exposure.** You
explicitly save requests from Burp into a list; the model reads only those.

| | Official | BurpMCP |
|---|---|---|
| Data model | Whole proxy history queryable | **Only requests you save** |
| Config mutation | Yes | **No** |
| Repeater/Intruder/editor control | Yes | No |
| Regex-replacement resend | No | **Yes** (genuinely useful primitive) |
| Observability | Burp logging | Dedicated MCP comms log |
| Maintenance | Vendor, active | Single maintainer, idle |

**Verdict:** smaller blast radius and better for careful low-exposure work, but
feature-poor and going stale. Its documented caveats are honest and generalize:
models forget `Content-Length`, HTTP/2 header handling interferes with
protocol-level testing, and **LF→CRLF conversion breaks request-smuggling
testing** — do smuggling by hand in Repeater regardless of which server you use.

---

## 2.4 HackerOne MCP — OFFICIAL, GA (lowest-risk server here)

https://docs.hackerone.com/en/articles/16069077-hackerone-mcp-server-setup-tool-reference

Platform-hosted HTTP, OAuth. **Read-only by design** — HackerOne states you
cannot use an MCP client to modify reports, tickets, assets, or program settings.
20+ tools: program/asset discovery, report search/analysis/comparison, bounty
data, remediation plans, insight extraction. Access mirrors your existing
platform permissions.

**Why it's the best server in this document:** no code on your machine, no write
path, no token you manage, and the data it returns is from a platform you already
trust rather than from a hostile target.

**Gotcha:** each client has its own OAuth `client_id`. The Claude Code (CLI) id
differs from Claude Desktop/Web — using the wrong one fails auth.

**Use it for:** scope ingestion (feed `scope/<program>.md`), duplicate checking
against your own prior reports, and regression sweeps over resolved reports.

> **Avoid all community HackerOne MCPs** (sicks3c, j0hndo, xtofuub, c0tton-fluff
> variants). They take your platform API token. The `sicks3c` one scored 65/100
> "Review Recommended" by AgentSeal. The official server makes them pointless.

**Bugcrowd:** no official or credible community MCP exists as of 2026-10. Use
the REST API directly; treat any "Bugcrowd MCP" you find as unvetted.

---

## 2.5 Code analysis

| Server | Status | Notes |
|---|---|---|
| **Semgrep MCP** | The repo `semgrep/mcp` was **archived 2025-10-28**; folded into the main `semgrep` binary (≥1.146.0). Right tool, wrong repo. | `claude mcp add semgrep -- uvx semgrep-mcp`. Tools: `security_check`, `semgrep_scan`, `semgrep_scan_with_custom_rule`, `get_abstract_syntax_tree`, `semgrep_findings`. **Low risk over local stdio — nothing leaves your machine.** Best signal-to-noise code-analysis MCP in the lane. The hosted `mcp.semgrep.ai` is experimental *and* ships your code off-box — avoid for client work. |
| **codeql-development-mcp-server** | https://github.com/advanced-security/codeql-development-mcp-server — maintained by GitHub's CodeQL Expert Services | Helps an agent *write, validate and optimize QL queries* rather than wrapping a scanner. The genuinely useful CodeQL MCP for variant analysis. |
| codeql-mcp (JordyZomer) | Community, small, usable | Wraps the CodeQL query server for agent-driven querying. |
| **yezere/codeql_n1ght_mcp_server** | **AgentSeal 19/100 "Dangerous"** | Shell-wrapping MCP with no input boundary. **Avoid.** |
| **GitHub MCP (official)** | Active; secret-scanning tools GA 2026-05-05 | For source-available targets. **Scope the PAT ruthlessly — this is the single most dangerous token to hand an agent.** Never in the same session as target-touching tools. |

---

## 2.6 Client-side / browser

These matter because **"the string appears in the response" is not XSS.** You need
actual JS execution to clear Gate 5.

| Server | Notes |
|---|---|
| **Chrome DevTools MCP (official Google)** — https://github.com/ChromeDevTools/chrome-devtools-mcp | `npx -y chrome-devtools-mcp@latest`. Network inspection, console, screenshots, tracing, Puppeteer automation. `--slim` reduces the toolset. Its own README is blunt: it "exposes content of the browser instance to the MCP clients allowing them to inspect, debug, and modify any data in the browser." **Use a dedicated clean Chrome profile — never your logged-in daily profile.** Usage stats on by default; `--no-usage-statistics` opts out. |
| **Playwright MCP (Microsoft)** — https://github.com/microsoft/playwright-mcp | Accessibility-tree-driven. **Better for deterministic multi-step flows** — auth sequences, IDOR walking, comparing multiple role sessions. Weaker for network/performance forensics. Same profile-isolation caution. |
| **Caido MCP (community)** — https://github.com/c0tton-fluff/caido-mcp-server | Talks to local Caido over GraphQL. Caido also shipped official AI agent Skills (2026-03-06) and published "Agentic Pentesting with MCP" (2026-07-14). |

**For this harness, Playwright MCP is usually the better pick** — the two-account
IDOR oracle and the role-diff oracle both need deterministic session control.

---

## 2.7 Recon wrappers

| Server | Status | Risk |
|---|---|---|
| **pd-mcp** (toxicwind) — https://github.com/toxicwind/pd-mcp | New (MIT, few commits) | **Best-engineered of the recon wrappers.** 9 tools (subfinder, dnsx, naabu, httpx, katana, nuclei, tlsx, shuffledns + a workflow composite). No-shell spawns, hard per-tool timeouts, boundary input validation, **nuclei gated behind `confirm: true`**, 2-slot semaphore on heavy scans. **Low risk by design; unproven by adoption.** |
| mcp-recon (nickpending) | 31★, Go, MIT, active | **Low** — 3 narrow tools, no exec primitive. Good example of minimal surface. |
| pd-tools-mcp (intelligent-ears) | community | Medium; thinner guardrails than pd-mcp. |
| **secops-mcp** (securityfortech) | 216★, MIT, active | **Medium-high** — bundles sqlmap + xsstrike (active exploitation) with no documented scope allowlist. Run containerized, never with host network. |
| bb-mcp-server (d24yk4r4) | 3★, active, EUPL/AGPL | **Most interesting privacy design in the lane:** 60+ pattern sanitizer vaults tokens/creds/PII locally so the model only ever sees `<SAFE:type:id>` placeholders; hash-chain integrity; dual-output reports. The "13-layer security model" framing is marketing, but **the vaulting mechanism is the right idea for NDA'd private-program traffic.** Tiny adoption — audit before use. Copyleft matters if you build on it. |
| ~~mcp-for-security (cyproxio)~~ | **ARCHIVED 2026-03-30** → migrated to `cyberstrikeus/bolt` | **Do not install.** Frozen dependencies on a 23-tool offensive aggregator is a supply-chain liability. Still widely linked in blog posts. |

### Aggregator
**FuzzingLabs mcp-security-hub** — https://github.com/FuzzingLabs/mcp-security-hub
(796★, MIT, active). 38 MCP servers / 300+ tools, each in a Docker container
running non-root, Trivy scanning in CI. Covers web, binary (radare2, ghidra, capa,
yara), cloud (trivy, prowler), secrets (gitleaks), OSINT, threat intel, AD, plus
wrappers around the official Shodan/Censys/Burp/ProjectDiscovery MCPs.

**This is the correct replacement for the stale `rootThatBox/BugbountiesMCP`
list.** Risk: it's an aggregator — **enable only the containers you need.** 38
servers' worth of tool descriptions in one context is itself a toxic-flow problem
*and* a large context tax.

---

## 2.8 Passive intel

| Server | Notes |
|---|---|
| **Censys Platform MCP (official)** — https://docs.censys.com/docs/platform-mcp-server | `claude mcp add --transport http censys-platform https://mcp.platform.censys.io/platform/mcp/`. OAuth or `Authorization: Bearer <PAT>` + `X-Organization-ID`. 13 tools incl. `investigate_host`, `discover_attack_surface`, `retrieve_cve_details`. **Calls burn credits — rate/cost is the real risk, not security.** An agent loop can drain a quota in minutes. |
| **Shodan MCP (official, July 2026)** | Host/device search, IP recon, DNS, CVE/CPE intel. Prefer official over the community forks. Scope the key to read. |

---

## 2.9 ⚠️ The cautionary case: `bugbounty-mcp-server`

**Disambiguation matters here.** Three repos share this name. AgentSeal's famous
**10/100 "Dangerous"** score describes **gokulapap's v1, which no longer exists.**

### The v1 finding
- **Score 10/100.** 21 findings, **15 critical/high**, across **93 tools**.
- The 93-tool surface spanned recon, scanning, **exploitation, persistence,
  credential theft, anti-forensics, and data exfiltration** — all agent-callable,
  with no scope gate.
- Finding classes: prompt injection, data exfiltration, **toxic data flows**.

### Why 10/100 was correct — the lesson to keep
1. **Capability aggregation *is* the vulnerability.** Individually reasonable
   tools (read a file, make an HTTP request, run a command) compose into
   exfiltration. 93 tools in one server guarantees a reachable malicious chain.
2. **No scope enforcement means the agent's target set is whatever text enters
   its context.** A prompt-injected response from a target you *are* testing can
   retarget the agent at assets you are *not* authorized to touch. In bug bounty
   that is not a bug — **it's unauthorized access with legal consequences.**
3. **Persistence, anti-forensics and credential-theft tools have no legitimate
   place in an MCP surface.** They cannot be reviewed before execution at agent
   speed, and they turn a research mishap into an incident.

### The v2 rebuild — a good reference design
https://github.com/gokulapap/bugbounty-mcp-server (latest commit 2026-08-24)
rebuilt as "scope-safe MCP v2", now 53 tools, explicitly excluding credential
dumping, persistence, anti-forensics, and destructive exploit automation. It adds:

- **fail-closed `ALLOWED_TARGETS` allowlist** — an empty allowlist rejects all network ops
- **DNS pinning** (anti-rebinding), private-IP blocking unless explicitly enabled
- server-side bounds on concurrency/depth/runtime/output; process-group cleanup
- bearer-token auth for HTTP transport, loopback-only by default
- `scope_check` / `batch_scope_check` as **first-class tools**

**Caveats:** no tagged releases; a recent commit **removed its own Dependabot and
CodeQL workflows** (a supply-chain regression); maintainer listed "Unresponsive";
**AgentSeal has not rescored v2**, so the 10/100 badge search engines surface does
not describe current code.

**Use v2's architecture as a reference design for scope-safe security MCP. Verify
the code yourself before running it.**

---

## 2.10 ❌ Avoid: VulneraMCP

https://github.com/telmon95/VulneraMCP · ~47★, 23 commits, last commit 2026-07-24

Claims subdomain/DNS/URL recon, ZAP scanning, "XSS/SQLi/**IDOR**/CSRF detection",
GraphQL introspection, JWT attacks, **OAuth misconfig analysis**, cloud bucket
scanning, knowledge-graph reasoning, and a web dashboard.

**Why to avoid:**
- **Claim-to-code ratio.** A 23-commit repo asserting IDOR detection, OAuth
  misconfiguration analysis and knowledge-graph reasoning. IDOR and business logic
  are *not mechanizable by a tool wrapper* — those claims are marketing.
- No visible CI, no tests, no audit. Documentation bloat typical of LLM-generated repos.
- Recent commits are **registry-submission and badge-farming** (Glama score badge,
  release automation) rather than capability work — distribution-first, substance-second.
- Earlier commits include "security-focused removal of sensitive data" and
  "redacting sensitive credentials" — **credentials were committed and later
  scrubbed. Assume git history still contains them.**
- Heavy dependency footprint (PostgreSQL 18, Redis, dashboard) for what is
  functionally a CLI wrapper = large unaudited surface running with your API keys.

If you want ZAP + recon wrappers, use `secops-mcp` or `pd-mcp` — they do less and
claim less.

### Also stale / dead
- **rootThatBox/BugbountiesMCP** — frequently cited as "the awesome-list for bug
  bounty MCP." It is a 10-row README from **May 2025** with dead and archived
  pointers. Use the FuzzingLabs hub instead.
- **cyproxio/mcp-for-security** — archived 2026-03-30.

---

## 2.11 Audit the servers before you trust them

Run these **as CLIs, not as connected MCP servers** — note the self-referential
trap that every scanner here is itself an MCP server you'd have to trust.

| Tool | Use |
|---|---|
| **MCP Inspector** — https://github.com/modelcontextprotocol/inspector | Enumerate a server's *real* tool list and schemas, rather than believing its README. |
| **mcp-scan** (Invariant Labs) | Static analysis of client configs + tool metadata for prompt injection, tool poisoning, rug pulls, toxic flows. CI-friendly, supports trusted-tool pinning. |
| **Cisco mcp-scanner** | Rule-based + semantic detection of poisoned tool metadata. |
| **SkillSpector** (NVIDIA, Aug 2026) | Scans agent *skills* (dirs, zips, git URLs) for risk before install. |

---

## 2.12 Claude Code MCP mechanics (exact)

```bash
# stdio — the `--` separator is MANDATORY before the command
claude mcp add semgrep -- uvx semgrep-mcp
claude mcp add --env API_KEY=xyz --transport stdio myserver -- python server.py --port 8080
#   WRONG: claude mcp add myserver python server.py --port 8080   ← Claude Code eats --port

# remote HTTP (preferred for hosted)
claude mcp add --transport http censys https://mcp.platform.censys.io/platform/mcp/

# SSE (deprecated in the spec, but what Burp speaks)
claude mcp add --transport sse burp http://127.0.0.1:9876/sse

# from raw JSON
claude mcp add-json weather '{"type":"http","url":"https://x/mcp"}'
```

### Scopes and precedence
```bash
claude mcp add ...                   # local (default) → ~/.claude.json, this project, private to you
claude mcp add --scope project ...   # → ./.mcp.json, COMMITTED, shared with the team
claude mcp add --scope user ...      # → ~/.claude.json, all your projects
```
Precedence, highest → lowest: **local → project → user → plugin → connectors.**

**For bug bounty:** put **engagement-specific** servers in `--scope project`
inside a per-target repo, so scope travels with the engagement and is reviewable
in git. Put **your credentials** in `local` or `user` so they never land in a
committed `.mcp.json`.

### `.mcp.json`
```json
{
  "mcpServers": {
    "burp":    { "type": "sse",   "url": "http://127.0.0.1:9876/sse" },
    "semgrep": { "type": "stdio", "command": "uvx", "args": ["semgrep-mcp"] },
    "censys": {
      "type": "http",
      "url": "https://mcp.platform.censys.io/platform/mcp/",
      "headers": {
        "Authorization": "Bearer ${CENSYS_PAT}",
        "X-Organization-ID": "${CENSYS_ORG}"
      }
    }
  }
}
```

Gotchas that will cost you an hour each:
- **`"url"` without `"type"` is parsed as stdio and fails.** Always set `type`.
- `${VAR}` / `${VAR:-default}` expansion works in `command`, `args`, `env`, `url`,
  `headers` — **at connection time**, so export before launching `claude`.
- `ANTHROPIC_API_KEY` and `AWS_BEARER_TOKEN_BEDROCK` are **blocked** from
  expanding into remote URLs/headers (deliberate leak prevention).
- `"headersHelper": "/path/script.sh"` must emit JSON; runs fresh on every
  reconnect, no caching. Use it for short-lived tokens.
- A project `.mcp.json` triggers its **own approval prompt**. **A `-p` headless
  session shows neither that nor the trust dialog** — that is the dangerous
  configuration for automation. Know it before you script anything.

### Output limits
Default **25,000 tokens** per MCP tool result. You can raise it with
`MAX_MCP_OUTPUT_TOKENS` — **don't, for proxy-history tools.** The limit is
incidentally an injection-surface limit.

### Management
```bash
claude mcp list        # servers + status
claude mcp get <name>
claude mcp remove <name>
claude mcp login <name>   # OAuth
```
In session: `/mcp` for status and per-project enable/disable, `/mcp reconnect all`.

---

## 2.13 Sandboxing: know what is and is not covered

This is the most commonly misunderstood control.

> `/sandbox` gives OS-level filesystem and network isolation for
> **Bash/PowerShell/Monitor only.** Built-in file tools, **MCP servers, and hooks
> run directly on the host.**

**So sandboxing Bash does not contain an MCP server.** For security MCPs, run them
in a devcontainer or VM — which is also Anthropic's own guidance ("use virtual
machines to run scripts and make tool calls, especially when interacting with
external web services"). Read-only filesystem by default, egress allowlisted to
your target scope.

**And note:** Anthropic "reviews connectors against its listing criteria before
adding them to the Anthropic Directory, but does not security-audit or manage any
MCP server." **Directory presence ≠ safety.** A Glama / mcp.so / PulseMCP listing
is a scrape, not an endorsement — VulneraMCP's recent commits are literally
badge-farming those registries.

---

## 2.14 Credential hygiene checklist

- [ ] Per-server, least-privilege, short-lived tokens. **Never one token across servers.**
- [ ] Read-only wherever the API offers it. Prefer servers that are read-only by
      construction (HackerOne MCP).
- [ ] Secrets via `${VAR}` expansion or `headersHelper` — **never literals in a
      committed `.mcp.json`.**
- [ ] No cloud keys, SSH keys, or password-store access in the environment that
      runs a target-touching agent.
- [ ] Scope Shodan/Censys keys to read, and watch credit burn.
- [ ] Log every tool invocation with params. BurpMCP's comms log is a good model.
- [ ] Pin tool definitions by hash; alert on change (rug-pull defense).
- [ ] Turn **off** marketplace auto-update for security packs, so reviewed code
      can't change under you.

---

**Next:** [10 — MCP as Target and as Risk](./10-mcp-as-target-and-risk.md) ·
[03 — Skills and Plugins](./03-skills-and-plugins.md) ·
[04 — Harness Architecture](./04-harness-architecture.md)
