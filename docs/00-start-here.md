# 00 — Start Here

A knowledge base for getting **paid** bug bounty findings with Claude Code, built
from research verified 2026-10-02.

> **Authorized, in-scope testing only.** Methodology and tooling — no exploit
> payloads or weaponized PoCs.

---

## The 30-minute path

If you read only three documents, read these in this order:

1. **[09 — Scope, Authorization & Ethics](./09-scope-authorization-and-ethics.md)**
   — the gate before everything. 10 minutes.
2. **[05 — Validation Gates](./05-validation-gates.md)** — the moat, and the actual
   thesis of this knowledge base. 15 minutes.
3. **[06 — Target Selection](./06-target-selection.md)** §6.1–6.2 — where the money
   is, and what to stop hunting. 5 minutes.

Then set up the scope hook (see the [README](../README.md)) and run
`/bb-harness:hunt-campaign`.

---

## Full reading order

### Understand the market (read once, properly)
- **[01 — The 2026 Landscape](./01-landscape-2026.md)** — what changed, platform
  policy as of October 2026, and **three widely-repeated claims that are factually
  wrong**. Read §1.1 even if you skip the rest.
- **[06 — Target Selection](./06-target-selection.md)** — payout tiers,
  under-tested surfaces, what's newly open in 2026.

### Build the machine
- **[04 — Harness Architecture](./04-harness-architecture.md)** — the five-element
  skeleton every serious program converged on, and exactly how to wire it in Claude
  Code. Includes **three traps that will bite you.**
- **[05 — Validation Gates](./05-validation-gates.md)** — the disprove ladder,
  per-class deterministic oracles, the negative ledger.

### Pick your tools
- **[02 — MCP Server Catalog](./02-mcp-servers.md)** — every security MCP server with
  maintenance dates and risk ratings. Includes what to **avoid**.
- **[03 — Skills & Plugins](./03-skills-and-plugins.md)** — skill packs assessed, the
  **supply-chain problem**, and the context-budget tax that makes mega-bundles
  counterproductive.

### Hunt and report
- **[08 — Vuln Class Playbooks](./08-vuln-class-playbooks.md)** — per-class
  methodology, ordered by what pays. Plus the current recon stack.
- **[07 — Reporting](./07-reporting-that-gets-paid.md)** — what triagers reward and
  punish.

### Stay safe and legal
- **[09 — Scope, Authorization & Ethics](./09-scope-authorization-and-ethics.md)**
- **[10 — MCP as Target & Risk](./10-mcp-as-target-and-risk.md)** — a paying surface,
  and simultaneously the most likely way your own harness gets you banned.

---

## The five things that matter most

If you internalize nothing else:

### 1. The market pays for *proving*, not *finding*
Discovery is commoditized — agents do it cheaply, and companies now do it in-house
at roughly 1/1000th of bounty prices (Shopify: $50–300 per scan producing findings
worth $400K+ in bounty-equivalent). Confirmation is **not** commoditized: the best
published automated exploit-confirmation result caps around **30%**.

### 2. Separate the thing that proposes from the thing that confirms
Never let the component that proposes a bug confirm it. Fresh context, different
model, inverted instruction (*"disprove this"*), and structurally **unable to file
findings**. Anthropic measured that fresh context alone roughly **halves** the
non-exploitable rate.

### 3. Build an oracle outside the model
From the AI-slop literature: security experts reason **deductively**, LLMs generate
**autoregressively**. The gap is **structural, not a prompting problem** —
chain-of-thought and tool use help but don't close it.

So: a timer, a created file, a DNS callback, a JS execution context, a canary string
from a second owned account, a test that flips fail→pass. **A script cannot
hallucinate.** Prefer any of these over any amount of model judgment.

### 4. Don't compete with agents on their best class
78% of valid autonomous findings are XSS. Hunt where confirmation requires knowing
what the application is *supposed* to do — business logic, authorization, auth
implementation, races, agentic/MCP authorization, compositional multi-commit risk.
Those are also **duplicate-resistant**.

### 5. Guarantees go in hooks; preferences go in prompts
A `PreToolUse` hook can **deny**. A system prompt can only **ask**. Scope
enforcement, write isolation, and stage-completion gates all belong in hooks. Claude
Code's own docs say it of output styles: *"It doesn't guarantee that something always
happens or never happens."*

---

## How claims are labelled

- **[V]** — verified against a primary source (platform press release, changelog,
  official engineering blog, arXiv paper)
- **[S]** — single-source or secondary; indicative, not established
- **[U]** — could not confirm; stated as unconfirmed rather than smoothed over

Where two sources conflict, the docs say so and tell you not to cite either. There
are several of these — the research was deliberately skeptical, and the
[01 §1.7](./01-landscape-2026.md) source-discipline note explains why that matters
on this topic specifically.

---

## What this knowledge base will not give you

- **Payloads, wordlists, or weaponized PoCs.** It tells you *where to look and why
  it breaks*, not what string to paste.
- **A promise of autonomy.** Every credible program keeps a human in the loop; low
  false-positive rates are achieved by throwing almost everything away.
- **Confidence in unverified numbers.** The ecosystem's stated metrics are
  unreliable — every skill pack surveyed disagreed with its own documentation, and no
  pack publishes efficacy data. The docs flag this rather than repeating it.

---

**Begin:** [09 — Scope & Ethics](./09-scope-authorization-and-ethics.md) →
[05 — Validation Gates](./05-validation-gates.md) →
[06 — Target Selection](./06-target-selection.md)
