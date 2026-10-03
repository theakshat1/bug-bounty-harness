# bb-harness

**A validation-first bug bounty harness and knowledge base for Claude Code.**

> For **authorized, in-scope security testing only.** Methodology and tooling — no
> exploit payloads or weaponized PoCs. Researched and verified 2026-10-02.

---

## The thesis

Everyone hunting your target now has an AI agent. Those agents trained on the same
disclosed reports and run the same playbooks, so **they converge on the same
findings.** That makes the binding constraint neither tooling nor coverage:

> **1. Originality decides what to hunt. 2. Validation decides what to submit.**

### Why originality first
A false positive costs you some triage goodwill. A **duplicate costs you the entire
pipeline** — recon, hunting, validation, proof, writing — and pays nothing. It passes
every gate you own, because it's *real*. You only find out at the end.

The one public dataset on agent-driven hunting: of ~1,060 reports, **208 were
duplicates and 209 informative — ~39% of output was work done correctly for zero
return.** That same account ranked **#1 on HackerOne's US leaderboard** while earning
**under $40,000 total since Feb 2024.** Volume and correctness weren't the constraint.
Novelty was.

So an obvious idea isn't merely low-value — it's **negative-value**, and the crowding
check belongs at *hypothesis* time, before you spend proof budget.
→ [11 — Non-Obvious Thinking](docs/11-non-obvious-thinking.md)

### Why validation second
- HackerOne's exploitable rate held **flat at ~25%** through a **76% volume surge** —
  so the bottleneck is *triage labour*. The market is short of people who can
  **confirm** bugs, not find them.
- **78% of *valid* autonomous findings were XSS** — the most crowded, least-paid class.
- **~70% of critical web vulnerabilities are business logic**, which no autonomous
  agent reliably detects, because the intent they violate isn't in the code.

Hence a **disprove-first validation ladder** rather than a bigger pile of hunting
prompts. → [05 — Validation Gates](docs/05-validation-gates.md)

### And the report is the last gate
A proven, novel bug still pays nothing if a triager closes it as Informative or stalls
it in Needs More Info. → [12 — Triage & Report Mechanics](docs/12-triage-and-report-mechanics.md)

---

## What's in here

```
docs/        the knowledge base — 13 researched documents
corpus/      the PRIVATE seed corpus — a curated idea bank (your edge)
skills/      8 working Claude Code skills
agents/      5 subagents, incl. the ideator and the adversarial disprover
schema/      the findings record contract, enforced by code
hooks/       PreToolUse scope guard · SessionStart state · Stop artifact gate
scripts/     hook implementations + validators + the test suite
reference/   scope template, example .mcp.json, checklists
```

### Enforced, not just documented

| Control | Hook | What it stops |
|---|---|---|
| Scope | `PreToolUse` | Any host off the allowlist — **including via `mcp__*` tools**, which are the usual bypass. Fails closed. |
| Findings schema | `Stop` + CLI | A `needs_validation` record carrying a severity; a trace that doesn't start at an entrypoint; a hedged impact sentence on a confirmed finding. |
| Gate 6 | `Stop` | A report draft built from a finding no human has reviewed. |

```bash
bash scripts/test-all.sh     # 57 checks across both hooks, manifests, links
```

### Why `corpus/` matters

Everything in `docs/` is synthesized from public research — so every other hunter can read
the same sources. `corpus/` is the half they can't: a curated, private idea bank that
ideation reads before generating. Per [docs/11 §11.10](docs/11-non-obvious-thinking.md),
seeding an agent with knowledge nobody else has is one of only two moves that reliably
differentiate a hunter now. **Grow it** — see [corpus/README.md](corpus/README.md).

### The knowledge base

| Doc | What it's for |
|---|---|
| [00 — Start Here](docs/00-start-here.md) | Reading order and a 30-minute path |
| [01 — The 2026 Landscape](docs/01-landscape-2026.md) | What actually changed, and **three widely-repeated claims that are wrong** |
| [02 — MCP Server Catalog](docs/02-mcp-servers.md) | Every security MCP server, with maintenance dates and **risk ratings** |
| [03 — Skills & Plugins](docs/03-skills-and-plugins.md) | Skill packs assessed, plus the **supply-chain problem** (36.8% of audited skills had flaws) |
| [04 — Harness Architecture](docs/04-harness-architecture.md) | How to build the pipeline. Cloudflare, Shopify, PageBreak, zsec — what to copy |
| [05 — Validation Gates](docs/05-validation-gates.md) | **The moat.** The disprove ladder, deterministic oracles, the negative ledger |
| [06 — Target Selection](docs/06-target-selection.md) | Where the money actually is, and what to stop hunting |
| [07 — Reporting](docs/07-reporting-that-gets-paid.md) | What triagers reward and punish |
| [08 — Vuln Class Playbooks](docs/08-vuln-class-playbooks.md) | Per-class methodology, ordered by what pays |
| [09 — Scope & Ethics](docs/09-scope-authorization-and-ethics.md) | Read first. The gate before everything |
| [10 — MCP as Target & Risk](docs/10-mcp-as-target-and-risk.md) | A paying surface, **and** how your own harness gets you banned |
| [11 — Non-Obvious Thinking](docs/11-non-obvious-thinking.md) | **The core principle.** 14 generators for duplicate-resistant hypotheses, the obviousness filter, and the audited duplicate data |
| [12 — Triage & Report Mechanics](docs/12-triage-and-report-mechanics.md) | Platform-by-platform: exact states, reputation costs, what gets closed, how to dispute |

### The skills

| Skill | Does |
|---|---|
| `/bb-harness:hunt-campaign` | Orchestrates a full campaign with gates between phases |
| `/bb-harness:scope-guard` | **Gate 0.** Scope verification + builds the enforced allowlist |
| `/bb-harness:hypothesis-forge` | **Originality engine.** Runs 12 generators, scores every idea for crowding |
| `/bb-harness:recon-surface-map` | Attack-surface inventory, route map, coverage ledger |
| `/bb-harness:authz-hunt` | IDOR/BOLA/BFLA/BOPLA, shadow API versions, tenant isolation |
| `/bb-harness:validate-finding` | **The moat.** Adversarial disprove ladder |
| `/bb-harness:regression-sweep` | Retests shipped fixes — ~3–8% of program fixes regress |
| `/bb-harness:report-writer` | Writes the report so a triager can't close it |

### The subagents

| Agent | Role |
|---|---|
| `ideator` | Invents non-obvious hypotheses. **No obligation to prove anything** — that's what keeps the ideas strange. |
| `hunter` | Proposes candidates for **one narrow slice**. Never verdicts. |
| `disprover` | Fresh context, different model, **tries to refute**. Cannot file findings. |
| `recon-mapper` | Maps surface. Does not hunt or exploit. |
| `report-drafter` | Drafts only from human-reviewed confirmed findings. |

---

## Install

### As a plugin (recommended)

```bash
git clone https://github.com/theakshat1/bug-bounty-harness
claude plugin validate ./bug-bounty-harness          # → ✔ Validation passed
claude plugin marketplace add ./bug-bounty-harness
claude plugin install bb-harness@bb-harness-marketplace
claude plugin details bb-harness                      # confirm the inventory
```

### For one session (dev loop)

```bash
claude --plugin-dir ./bug-bounty-harness
```

### Verify it loaded

```
/bb-harness:scope-guard example.com
```

Skills appear as `/bb-harness:<name>`; subagents as `bb-harness:<name>`.

> **Turn marketplace auto-update OFF for security plugins**, including this one, so
> code you reviewed can't change under you.

---

## Enable the scope hook (do this before testing anything)

The hook is the only control that actually stops an agent leaving scope. A system
prompt can only ask; a hook can **deny**.

```bash
mkdir -p scope findings recon reports
cp bug-bounty-harness/reference/scope-template.md scope/myprogram.md
# fill it in from the live program policy — verbatim, never paraphrased

# then the machine-readable allowlist the hook reads:
cat > scope/allowlist.txt <<'EOF'
*.example.com
api.example.com
!blog.example.com        # ! = explicit deny, beats any wildcard
EOF
```

The hook **fails closed**: with no `scope/allowlist.txt`, every outbound network
tool call is blocked. That's deliberate.

Verify it works before you trust it:

```bash
# off-allowlist host is blocked
echo '{"tool_name":"WebFetch","tool_input":{"url":"https://not-in-scope.test/"}}' \
  | python3 scripts/scope-enforce.py; echo "exit=$?"      # expect exit=2

# and so is an MCP server trying the same thing — this is the bypass most harnesses miss
echo '{"tool_name":"mcp__burp__send_http1_request","tool_input":{"host":"not-in-scope.test"}}' \
  | python3 scripts/scope-enforce.py; echo "exit=$?"      # expect exit=2

# in-scope host is allowed
echo '{"tool_name":"WebFetch","tool_input":{"url":"https://api.example.com/"}}' \
  | python3 scripts/scope-enforce.py; echo "exit=$?"      # expect exit=0

bash scripts/test-all.sh                                   # or just run everything
```

---

## Quickstart

```
1. Read docs/09 (scope), docs/11 (originality), docs/05 (validation).  ~35 min
2. /bb-harness:scope-guard <target>        → builds scope/ + allowlist
3. Enable the hook, verify it blocks.                 ← do not skip
4. /bb-harness:hunt-campaign <program>     → orchestrates the rest
     ...which runs ideation FIRST, so you hunt uncrowded ideas
5. Read every confirmed finding yourself.             ← Gate 6, never automated
6. /bb-harness:report-writer <finding> <platform>  → triage-optimized write-up
7. /bb-harness:regression-sweep <program>  → the surface nobody works
```

---

## The non-negotiables

1. **Authorized, in-scope targets only.** No exceptions, no "technically not
   prohibited."
2. **The hunter never validates its own candidate.** Separate subagent, fresh
   context, different model where possible, and it *cannot file findings*.
3. **A human reads every finding before it ships.** Automated submission bans
   accounts and poisons the well for everyone.
4. **Two accounts you own** for any isolation test. One record is proof; a table is
   an incident you caused.
5. **Severity from demonstrated impact**, never from the class name. *If you cannot
   state the concrete damage, the severity is lower than it feels.*
6. **Cap concurrent subagents at 2–3.** More breaks compaction and loses findings.
7. **Never run `claude -p` against an untrusted repo without `--bare`** — it
   otherwise executes that repo's hooks and connects its MCP servers with no prompt.
8. **Never combine a target-touching MCP server with a data-bearing one** in the
   same session.

---

## What this harness deliberately does not do

- **No exploit payloads, wordlists, or weaponized PoCs.** Methodology only.
- **No autonomous submission.** Ever.
- **No "find all vulns" prompts.** Slices only — a focused prompt measurably
  outperforms a broad one.
- **No claim of autonomy.** Nobody credible claims it: Cloudflare mandates human
  review, zsec says "the system needs me to make judgment calls," Google withholds
  unverified findings entirely. Low false-positive rates are achieved by **throwing
  almost everything away.**

---

## Source discipline

This topic has a bad secondary-source problem. Lots of 2026 content inverts
HackerOne's own meaning — turning *"25% exploitable, rate held steady"* into *"only
25% are real, so the growth is noise."* The second doesn't follow from the first, and
HackerOne never said it.

Claims in `docs/` are tagged **[V]** verified against a primary source, **[S]**
single/secondary source, **[U]** could not confirm. Anchor on
`hackerone.com` · `docs.hackerone.com` · `bugcrowd.com/blog` · `kb.intigriti.com` ·
`github.blog` · `shopify.engineering` · `anthropic.com` · `arxiv.org` ·
`portswigger.net/research`.

Where the research could not confirm something, the docs say so rather than
smoothing it over.

---

## License

MIT. Use it on targets you're authorized to test.
