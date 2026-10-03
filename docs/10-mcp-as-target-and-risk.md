# 10 — MCP: as a Target, and as a Risk to You

MCP cuts both ways for a bug bounty hunter. It is **a fast-growing, under-tested
attack surface you can get paid to break**, and simultaneously **the most likely
way your own harness gets you banned or compromised.** Both halves below.

---

## Part A — MCP as a paying target

### 10.1 Why this surface is worth your time

- **30+ CVEs** against MCP servers, clients and infrastructure in Jan–Feb 2026
  alone; 14 more in Q3 2026.
- **Censys counted 12,520 internet-reachable MCP services across 8,758 IPs**
  (2026-04-28), and roughly **40% exposed tools with no authentication at all**.
- HackerOne independently names **MCP OAuth account takeover** and **agent
  authorization confusion** among the classes that currently pay well.
- The surface is new, the frameworks are young, and the tester-to-surface ratio is
  far better than on any mature web app.

**Caveat first:** confirm MCP endpoints are in scope. Many are internal tooling,
and a vendor's MCP server may be third-party infrastructure.

### 10.2 The OWASP MCP Top 10 as a hunting checklist

Published 2025, still beta. Primary:
https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html

| ID | Risk | What to look for |
|---|---|---|
| MCP01 | Token mismanagement & secret exposure | Tokens in config, logs, or echoed in tool output; over-scoped tokens; tokens shared across servers |
| MCP02 | Privilege escalation via scope creep | A tool that accepts a resource selector the caller shouldn't control |
| MCP03 | Tool poisoning | Malicious instructions in tool *descriptions* and schemas — these enter the model's context as semi-trusted text |
| MCP04 | Supply chain & dependency tampering | Unpinned servers, rug-pull on update, typosquatted deps |
| MCP05 | Command injection and execution | Shell-wrapping servers with no input boundary (the single most common real bug) |
| MCP06 | Intent flow subversion | Prompt injection via tool results steering the agent |
| MCP07 | Insufficient authentication/authorization | **~40% of internet-exposed servers.** Start here. |
| MCP08 | Lack of audit and telemetry | No record of which tool ran with what args |
| MCP09 | Shadow MCP servers | Undocumented servers reachable in the environment |
| MCP10 | Context injection and over-sharing | A tool returning far more than the caller is entitled to |

### 10.3 The classes that actually pay

**Frame these as classical bugs, per [06 §6.5](./06-target-selection.md) — "MCP
jailbreak" gets closed; "unauthenticated RCE in an exposed MCP tool" gets paid.**

1. **Missing authentication on an exposed server (MCP07).** Highest base rate.
   Transport is often SSE or streamable HTTP on a port someone assumed was
   internal. The finding is plain unauthenticated access to privileged tools.
2. **Command injection in tool arguments (MCP05).** Many servers are thin wrappers
   around CLI tools with naive string interpolation. This is RCE.
3. **OAuth flow bugs** — the class HackerOne calls out by name. Check
   `redirect_uri` validation, PKCE enforcement, `state` binding, token audience
   validation, and confused-deputy patterns where the server redeems a code it
   shouldn't. The [08 §auth](./08-vuln-class-playbooks.md) five-condition matrix
   applies directly.
4. **Toxic flows / capability aggregation.** The highest-value *architectural*
   finding: demonstrate that two individually-reasonable tools compose into
   exfiltration or privilege gain. This is what scored `bugbounty-mcp-server` 10/100.
5. **Agent authorization confusion.** The agent acts with its own credentials
   rather than the requesting user's, so any user can reach any resource the agent
   can. A plain authorization bug with a new shape — and under-tested.
6. **Tool poisoning (MCP03).** Instructions hidden in a tool description or schema
   that the host renders into context. Prove a concrete boundary crossing, not just
   "the model obeyed."
7. **Cross-tenant leakage in hosted MCP servers.** Standard multi-tenant isolation
   testing against a new surface.
8. **SSRF via a fetch-shaped tool.** Many servers expose a URL-taking tool with no
   egress controls, no DNS pinning, and no private-IP blocking.

### 10.4 Tooling for testing MCP

| Tool | Use |
|---|---|
| **MCP Inspector** — https://github.com/modelcontextprotocol/inspector | Enumerate real tool lists and schemas. First step always. |
| **MCPwned** (Fenrisk) — Burp extension | Detect MCP traffic, enumerate capabilities, **tool-argument fuzzing**. |
| **MCP-ASD** (Attack Surface Detector) | SSE/WebSocket transports are awkward in Burp; this makes enumeration and manual testing practical. |
| **mcp-scan** (Invariant Labs) | Static analysis for prompt injection, tool poisoning, rug pulls, toxic flows, cross-origin issues. |
| **Cisco mcp-scanner** | Rule-based + semantic detection of poisoned tool metadata. |
| **MCPSecBench** (arXiv 2508.13220) | Benchmark — useful for a test checklist. |

**For threat-modelling a specific MCP deployment**, the OWASP **MCP-Taxonomy** repo
(`https://github.com/OWASP/MCP-Taxonomy`) adds what the Top 10 list alone doesn't: component
**relationship maps** between host, client, server and gateway, plus root-cause tags
(injection, SSRF, auth bypass, cross-tenant) you can use to structure a review rather than
working a flat checklist. **[S — no maintenance date verified.]**

Research anchors: **MCP-DPT** defense-placement taxonomy (arXiv 2604.07551),
*"When MCP Servers Attack"* (arXiv 2509.24272), **MCPGuard** (arXiv 2510.23673),
and the NSA-guidance ↔ OWASP-MCP-Top-10 mapping (equixly.com, 2026-06-04).

### 10.5 Adjacent: agent skills are becoming a bug class

**SkillSpector** (NVIDIA, Aug 2026) scans agent skills for risk before install.
That such a tool exists is the signal. Combined with Snyk's ToxicSkills finding
(36.8% of 3,984 skills flawed, 13.4% critical — see
[03 §3.1](./03-skills-and-plugins.md)) and the academic work on compositional skill
risk, **agent-skill supply chain is an emerging surface.** If a program's product
ships or consumes agent skills, it's worth looking at.

---

## Part B — MCP as a risk to *your* harness

This half is not optional reading. It's how you avoid being the incident.

### 10.6 Prompt injection via tool output is not theoretical here — it's the job

You are **deliberately feeding your agent HTTP responses from hostile systems.** A
stored-XSS payload, a crafted `Server` header, an error message, a JS comment, a
`robots.txt`, a CI log, or a support ticket body can contain text that reads as
instructions.

`get_proxy_http_history` is an injection firehose by design.

**Mitigations:**
- Prefer `*_regex` history variants with tight `count`/`offset` over bulk dumps.
- **Never let a history-reading session also hold write-capable tools** (GitHub
  PAT, filesystem write, Burp config mutation).
- Keep `MAX_MCP_OUTPUT_TOKENS` at the default — the limit is incidentally an
  injection-surface limit.
- Wrap target output in nonce-delimited untrusted blocks via a `PostToolUse` hook,
  with the nonce generated *after* the content exists.
- Treat a target repository's own `CLAUDE.md`, skills and hooks as
  attacker-controlled — set `omitClaudeMd: true` on agents reading untrusted code.

### 10.7 Toxic flows are the dominant real finding

AgentSeal's scan of 1,808 servers: **66% had findings. 8,282 findings total — 427
critical, 1,841 high.** By category: **code execution 40.1%, toxic data flows
37.2%**, data exposure 3.2%, prompt injection 2.2%.

> **The practical rule: one target-touching server + one data-bearing server in the
> same session is the dangerous combination — regardless of either one's individual
> score.**

Toxic flows, not individual CVEs, are 37% of real findings and ~100% of the ways an
agentic hunter gets banned.

### 10.8 Why a sketchy MCP server is worse than a sketchy CLI

1. It executes **on your host with your environment** — `~/.aws`, `~/.ssh`, Burp
   project files, your HackerOne token, client NDAs.
2. It is **invoked by a model**, not by you, so you don't review each call.
3. Its **tool descriptions enter your context** as semi-trusted instructions.
4. It can **rug-pull on any update**, because almost none are version-pinned.
5. Offensive-tooling MCPs are a **high-value supply-chain target precisely because
   their users hold bounty platform tokens and client data.**

### 10.9 Sandboxing: what is and isn't covered

> `/sandbox` provides OS-level filesystem and network isolation for
> **Bash/PowerShell/Monitor only.** Built-in file tools, **MCP servers, and hooks
> run directly on the host.**

**Sandboxing Bash does not contain an MCP server.** Run security MCP servers in a
devcontainer or VM — Anthropic's own guidance is to *"use virtual machines to run
scripts and make tool calls, especially when interacting with external web
services."* Read-only filesystem by default; egress allowlisted to your scope.

And: **Anthropic does not security-audit MCP servers.** Directory presence is not
endorsement, and a Glama/mcp.so/PulseMCP listing is a scrape.

### 10.10 The out-of-scope risk, which is the one that actually ends careers

A prompt-injected agent that wanders out of scope is not a bug in your tooling. It
is **unauthorized access, with legal consequences**, performed from your machine
under your identity.

This is why scope allowlists enforced in code — `pd-mcp`'s `confirm: true`,
`gokulapap` v2's fail-closed `ALLOWED_TARGETS`, this repo's
`scripts/scope-enforce.py` `PreToolUse` hook — matter **more than any other control
in this document.**

> A hook can deny. A system prompt can only ask.

### 10.11 Your hygiene checklist

- [ ] Allowlist **individual MCP tools**, never a whole server
- [ ] One target-touching server per session; nothing data-bearing alongside it
- [ ] Per-server, least-privilege, short-lived tokens; never one token across servers
- [ ] No cloud keys, SSH keys, or password-store access in the agent's environment
- [ ] Prefer read-only-by-construction servers (HackerOne MCP)
- [ ] Secrets via `${VAR}` or `headersHelper`, never literals in a committed `.mcp.json`
- [ ] Run security MCP servers in a container/VM, not on the host
- [ ] `PreToolUse` scope hook, failing **closed**, and **covering `mcp__*` tools** —
      allowlisting a tool is not the same as constraining which host it may reach.
      Verify this specifically; it is the easiest scope control to get wrong, because
      an MCP tool name doesn't look like a network call
- [ ] Audit with MCP Inspector before trusting any server's README
- [ ] Pin tool definitions by hash; alert on change
- [ ] Marketplace auto-update **off** for security packs
- [ ] Log every tool invocation with arguments
- [ ] Never run `claude -p` against an untrusted repo **without `--bare`** — it
      otherwise executes that repo's hooks and connects its MCP servers with no prompt

---

**Next:** [02 — MCP Servers](./02-mcp-servers.md) ·
[09 — Scope and Ethics](./09-scope-authorization-and-ethics.md) ·
[04 — Harness Architecture](./04-harness-architecture.md)
