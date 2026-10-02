# 03 — Skills & Plugins Catalog

> Verified 2026-10-02. **Read §3.1 before you install anything from this page.**

---

## 3.1 ⚠️ Read this first: the supply-chain problem

Snyk's **"ToxicSkills"** audit scanned 3,984 agent skills from ClawHub and
skills.sh (snapshot 2026-02-05):

> **36.8% (1,467) had at least one security flaw. 13.4% (534) had a critical
> issue** — malware distribution, prompt injection hidden in `description` fields
> (e.g. instructing the agent to read `~/.ssh/id_rsa` and POST it out), shell
> payloads chained to evade Bash deny rules, and typosquatted dependencies in
> bundled `package.json` / `requirements.txt`.

Corroborating academic work in the same window: arXiv **2605.11418** (semantic
supply-chain attacks on skill registries), **2604.06550** (SkillSieve triage),
**2608.16246** (CompoSkill — chains of individually scanner-passing skills),
**2606.00448** (compositional risk), plus CSA's research note on **SKILL.md
context poisoning** (2026-05-06).

### Why security skill packs are the worst case
1. They are **large third-party instruction + code bundles that run with your
   privileges**.
2. Security repos **legitimately contain attacker-shaped strings**, which makes
   malicious content far harder to spot — and triggers AV false positives, so
   people disable the AV rather than investigate.
3. Their users hold **bug bounty platform tokens, client data, and NDAs**. That
   makes offensive-tooling packs a high-value supply-chain target.
4. Per Claude Code's own plugin security docs: **hooks, MCP server processes, and
   mods run outside the sandbox and outside permission rules.** `bin/` is injected
   into the Bash tool's PATH. Auto-update can silently change files you reviewed.

### Minimum hygiene before installing any pack
- [ ] Read `SKILL.md`, `hooks/hooks.json`, `.mcp.json`, and **all of `bin/`** yourself
- [ ] `claude plugin validate <dir>` and `claude plugin details <name>` for an
      offline component inventory
- [ ] Prefer **commit-pinned** or **sha256-pinned** marketplace entries
- [ ] **Turn auto-update OFF** for security packs
- [ ] Run **SkillSpector** (NVIDIA) or **mcp-scan** over the bundle first
- [ ] Only `github.com/anthropics/*` may use official marketplace names
      (`claude-plugins-official`, `claude-community`). Everything else is
      third-party, whatever it calls itself.

---

## 3.2 ⚠️ Read this second: stated counts in this ecosystem are unreliable

Every pack surveyed disagreed with its own documentation:

| Pack | Claimed | Actual |
|---|---|---|
| Claude-BugHunter | 82 skills, 7 commands documented | **83 skills, 15 commands** |
| transilienceai/communitytools | 26 skills | **27** |
| pentest-agents | 48 agents | **50** |
| trilwu/secskills | 16 skills, 6 subagents (per a March 2026 roundup) | **92 skills across 3 plugins** |

**Always count the directory yourself.** `trilwu/secskills` actively *removing*
skill-count displays from its site is the healthiest signal observed in the
ecosystem.

### And nobody publishes efficacy data
No pack surveyed offers an eval result, benchmark, or disclosed-bug attribution.
All "$40k earned", "found N bugs", and "100% OWASP coverage" claims are
self-reported. Treat them as marketing.

### Convergent methodology ≠ independent validation
The **7-Question Gate**, `hunt-*` skill naming, `/autopilot`, `/validate`,
`triage-validation` and `security-arsenal` recur **verbatim** across
Claude-BugHunter, Agentic-Bug-Hunter and pentest-agents. That is **copying, not
corroboration** — one lineage. Don't treat three packs agreeing as evidence.

---

## 3.3 The context-budget tax (the engineering constraint nobody respects)

Every **model-invocable** skill, agent, and command's name + description sits in
your context **every turn, in every session**, while the plugin is enabled — not
just when used.

Consequences for the 80–800-skill bundles:
- Descriptions get **truncated** when there are too many, so skills silently stop
  triggering.
- On compaction, only ~5,000 tokens per skill are retained.
- Skill content, once invoked, **stays in context for the rest of the session and
  is not re-read after you edit it** — restart to pick up changes.
- Combined subagent descriptions are capped around **15,000 tokens**.

**Practical limits reported by working hunters:**
- **Cap concurrent subagents at 2–3.** Four or more breaks compaction and loses
  findings. (Note how badly a "50 subagents" or "parallel swarm" pack violates this.)
- Audit with `/skill-doctor` and the `/plugin` details pane's "Not used recently"
  group. Disable what you don't use.

> A 90-skill bundle you enabled "just in case" is a permanent tax on every turn
> of every session, and it makes the skills you *do* need less likely to fire.
> Install narrow, not broad.

---

## 3.4 The packs — assessed

### Highest signal

| Pack | URL | What / why | Maintenance |
|---|---|---|---|
| **Trail of Bits skills** | https://github.com/trailofbits/skills | **Highest-credibility option by a wide margin.** VR-relevant: `static-analysis` (CodeQL/Semgrep/SARIF), `variant-analysis`, `c-review`, `rust-review`, `semgrep-rule-creator`, `differential-review`, `supply-chain-risk-auditor`, `constant-time-analysis`, `burpsuite-project-parser`, `building-secure-contracts`. Code-audit/VR oriented, **not** black-box bug bounty. CC-BY-SA-4.0. | 7.3k★, new skills through Sept 2026. **Active.** |
| **trilwu/secskills** | https://github.com/trilwu/secskills | **Best quality machinery.** 92 skills across `secskills-offense`, `secskills-defense`, `secskills-core`. Every skill carries a `verified:` date checked against primary sources and enforced by `validate.py --strict`; CI runs `run_evals.py`; **builder subagents with independent critic agents that try to refute candidates.** Stated positioning: "encode the judgment professionals bring, not another wrapper around a scanner." | MIT, 153★, last commit **2026-08-06**. Active. |
| **Claude-BugHunter** | https://github.com/elementalsouls/Claude-BugHunter | **The clearest triage and evidence doctrine in the ecosystem — worth reading even if you never install it.** 83 skills (58 `hunt-*` classes, 10 enterprise-platform, 5 recon, 6 reporting/validation, 4 methodology), 15 commands, 681 disclosed-report patterns across 24 classes. 6-phase workflow SCOPE→RECON→HUNT→VALIDATE→CAPTURE→REPORT with `/validate` gating phase 5→6. Deliberate scope boundary (no AD, C2, post-ex, binary exploitation). Dual MIT + CC BY 4.0. | Last human feature commit **2026-09-09**; later daily commits are a star-history bot. Active. |
| **awarexone/Agentic-Bug-Hunter** (was `shuvonsec/claude-bug-bounty`) | https://github.com/awarexone/Agentic-Bug-Hunter | **Most active and most-starred: ~5.2k★, 252 commits, last commit 2026-10-02.** Strongest verification story: `/verify` **re-derives a finding independently from the saved PoC bundle and suppresses anything not re-proven.** Plus a scope-safety check before any action, 17 hunting rules + 6 critical directives (incl. "NEVER hunt theoretical bugs"), and a persistent per-target lead ledger. Runs subscription-free via Ollama/Groq/DeepSeek. | Very active. |

### The 7-Question Gate (worth stealing, from Claude-BugHunter's `triage-validation`)
Outputs PASS / KILL / DOWNGRADE / CHAIN-REQUIRED:

1. Is there a **real HTTP request**?
2. Is the impact on the program's **accepted** list?
3. Is the asset **in scope**?
4. Does it avoid **assuming pre-existing admin**?
5. Is it **novel** / not by-design?
6. Is it beyond "technically possible" — **actual victim data**, not just a 200?
7. Is it off the **never-submit** list (missing headers, non-sensitive clickjacking, …)?

This maps cleanly onto our gate ladder in
[05 — Validation Gates](./05-validation-gates.md). Questions 2, 6 and 7 are the
ones most hunters skip.

### Stale — don't build on these

| Pack | Last commit | Note |
|---|---|---|
| transilienceai/communitytools | **2026-07-29** | 27 skills, symlinked into isolated `projects/` sandboxes (a genuinely good architecture), coordinator/executor/validator roles, one MCP server for CVE enrichment. But **nothing in the Aug–Oct window**, and "100% OWASP coverage" is vendor marketing, not measurement. |
| H-mmer/pentest-agents | **2026-05-06** | Enormous: 50 subagents, 26 commands, 11 skills, 19 CLI tools, 2 MCP servers, 2,600-line rules library. Has explicit **"anti-Goodhart" validity gates** — a good sign. But 50 agents badly exceeds the 2–3 concurrency ceiling, licence is "for authorized security testing" (not OSI), and it's 5 months stale. |

### Avoid / flag

| Pack | Why |
|---|---|
| **Mystery223/Anthropic-Cybersecurity-Skills** | Claims **817+ skills**. Far past the point where descriptions truncate and context cost dominates. The name implies an Anthropic affiliation it **does not have**. This URL is a fork of `mukul975`. **Bloat/hype.** |
| **security-hunter-mcp** (vikrant-project) | Architecturally the right answer to cross-session memory (41 tools, SQLite FTS5, automatic secret scrubbing, scope authorization gates) — but **1 star, 1 commit.** A prototype. Don't depend on it. |
| Masriyan/Claude-Code-CyberSecurity-Skill | 22 broad domain skills, 455★, MIT. Breadth over depth, **no validation machinery**. Fine as reading, weak as a harness. |
| `DaoYiSec/SecSkills` | Unrelated Chinese-language collection — **name collision** with `trilwu/secskills`. Don't confuse them. |

---

## 3.5 When to write a skill vs when not to

The best published guidance on this is **HackerNotes Ep. 166** (Critical Thinking
podcast, "Claude Code Skills for Bug Bounty: When, Why, and How to Build Them",
sourced from Rez0): https://blog.criticalthinkingpodcast.io/p/hackernotes-ep-166-claude-code-skills-for-bug-bounty-when-why-and-how-to-build-them

**Write a skill only for one of three reasons:**
1. **Knowledge the model lacks** — the Caido SDK, a conference technique, paywalled
   enterprise product behavior, a client's internal conventions.
2. **Steering the solution space** — when curl, Python, Playwright and Caido would
   all technically work, and you want a specific one.
3. **Your own infrastructure** — VPS credentials, paths, collaborator domains.

**Do not** write a skill to re-explain a bug class the model already knows. That's
pure context tax.

**Design patterns from the same source:**
- Give each skill a **3-layer fallback**: primary tool → SDK/library → raw API.
- Include an explicit line telling Claude **not to confine itself** to the
  prescribed workflow.
- Structure `CLAUDE.md` as a funnel:
  **Notes → Leads → Primitives/Gadgets → Findings → Reports.**
- **Declare authorized-tester identity** to cut spurious refusals.
- Store state in a per-target folder (or Obsidian/Notion API, or Caido's Findings tab).
- **Dual-agent diff pattern:** Agent A fully guided vs Agent B free-roaming, then
  diff the outputs to find gaps in your own methodology. Cheap and very effective.

And a finding from the same ecosystem worth internalizing — one practitioner
tested the same site twice and found **a focused prompt found 5 XSS where a broad
"find all vulns" prompt missed them.** Narrow beats broad, measurably. This is the
same conclusion Shopify reached with partitioning (see
[04 — Harness Architecture](./04-harness-architecture.md)).

---

## 3.6 Claude Code skill/plugin mechanics (exact, v2.1.28x)

### `SKILL.md`
Lives at `.claude/skills/<name>/SKILL.md` (project) or `~/.claude/skills/<name>/SKILL.md` (user).

```yaml
---
name: my-skill                    # optional; defaults to folder name. letters/digits/hyphens
description: When Claude should use this.   # REQUIRED — this is the trigger text
argument-hint: "[target]"         # autocomplete hint
arguments: [env, region]          # named args → $env, $region
allowed-tools: Bash(git *) Read   # pre-approve; clears on next user message
disable-model-invocation: true    # user-only (/skill-name)
user-invocable: false             # model-only reference content
context: fork                     # run as a subagent instead of inline
agent: disprover                  # which subagent, with context: fork
paths: "src/**"                   # only load when working with matching files
model: opus
effort: high
---
```

Variables: `$0 $1 $2`, `$ARGUMENTS`, named args, `${CLAUDE_SKILL_DIR}`,
`${CLAUDE_PROJECT_DIR}`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`.

Dynamic context injection — shell runs **before** the skill text reaches the model:
````markdown
Current scope:

!`cat scope/allowlist.txt`
````

**Progressive disclosure:** keep `SKILL.md` under ~500 lines and put detail in
sibling `reference.md`, `examples.md`, `scripts/`. Those load only when referenced.

### Plugin layout
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json         ← ONLY this file goes in .claude-plugin/
├── skills/<name>/SKILL.md  ← runs as /my-plugin:name
├── agents/<name>.md
├── hooks/hooks.json
├── .mcp.json
├── bin/                    ← injected into Bash PATH (review this!)
└── scripts/
```
**Everything except `plugin.json` lives at the plugin root, not inside
`.claude-plugin/`.** This is the single most common structural mistake.

### Marketplace
`.claude-plugin/marketplace.json` requires `name`, `owner`, `plugins[]`; each
entry needs `name` and `source` (a path from the marketplace root, or a
`github`/`git-subdir`/`archive`/`npm` source object).

```bash
claude plugin validate ./my-marketplace        # before anything else
claude plugin marketplace add owner/repo       # or a local path
claude plugin install my-plugin@my-marketplace
claude plugin list
claude plugin details my-plugin                # component inventory
```
**The entry `name` in `marketplace.json` must match the `name` in that plugin's
`plugin.json`**, or installs fail with a confusing "not found in marketplace".

Dev loop without a marketplace:
```bash
claude --plugin-dir ./my-plugin -p "..."
```
In-session `/reload-plugins` picks up edits to a locally-sourced plugin.

### Subagents — `.claude/agents/<name>.md`
```yaml
---
name: disprover                   # REQUIRED
description: When to delegate to this agent.   # REQUIRED
tools: Read, Grep, Glob, Bash     # allowlist; or use disallowedTools
model: opus                       # sonnet|opus|haiku|fable|full id
permissionMode: default
skills: [validate-finding]        # preload
memory: project                   # user|project|local
maxTurns: 10
isolation: worktree
color: red
---
System prompt goes here as markdown body.
```
Non-fork subagents start with **fresh context** + CLAUDE.md — which is exactly
what makes them usable as independent validators. Nesting depth 3, 20 concurrent
max (but **use 2–3**).

MCP tools in `tools`: `mcp__burp__*`, or name them individually (preferred).

### Hooks
Where the real enforcement lives. See
[04 — Harness Architecture](./04-harness-architecture.md) §4.6 for the scope-guard
hook. Key events: `PreToolUse` (blockable, **exit 2 denies the call**),
`PostToolUse`, `SessionStart`, `UserPromptSubmit` (blockable), `Stop` (blockable),
`SubagentStop`, `PreCompact`, `ConfigChange`.

Command hooks receive JSON on stdin and signal via exit code: **0 = allow,
2 = block**, anything else = non-blocking error.

---

## 3.7 Recommendation

**Don't install a mega-bundle.** Install narrow and specific:

1. **This harness** (`bb-harness`) for the validation ladder, scope enforcement,
   and report discipline — the parts that determine whether you get paid.
2. **Trail of Bits skills** if you do source-available / code-audit work.
3. **Read** Claude-BugHunter's `triage-validation` and `evidence-hygiene` skills
   and `awarexone`'s `/verify` re-derivation gate, and port the ideas you want
   into your own narrow skills.
4. Add individual `hunt-<class>` skills **only for classes you actually hunt**,
   and only where they encode something the model doesn't already know.

The reason is in §3.3: every skill you enable is a permanent per-turn tax and a
dilution of your trigger space. The hunters landing P1/P2 on competitive targets
are running **narrower** automation against **more carefully selected** surface —
not broader automation.

---

**Next:** [04 — Harness Architecture](./04-harness-architecture.md) ·
[02 — MCP Servers](./02-mcp-servers.md) ·
[05 — Validation Gates](./05-validation-gates.md)
