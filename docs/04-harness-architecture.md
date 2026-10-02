# 04 — Harness Architecture

> **The thesis every serious 2026 program converged on independently:**
>
> *"What actually raised capability, cost efficiency and reliability was not model
> selection but the orchestration layer wrapped around the model."* — Andy Gill, zsec
>
> *"The harness is the bit that lasts."* — Cloudflare
>
> Shopify titled their post *"Building an agentic harness that outlasts the model."*
> Three teams, one conclusion. **Invest in the harness, not the prompt.**

---

## 4.1 The five-element skeleton

Four independent programs — zsec, Cloudflare, Google PageBreak, Shopify — landed
on the same shape:

1. **Recon stage** that emits a *machine-readable work plan*, not prose.
2. **Fan-out hunters**, one narrow unit of work each, isolated context.
3. **A refutation gate** run by a *different agent* and ideally a *different
   model*, whose only job is to disprove.
4. **A reachability/evidence gate** — a call chain from an untrusted entrypoint,
   or a reproduced effect in a sandbox.
5. **Deterministic non-LLM validators** on schema and coverage, plus persistent
   state *outside* the context window.

```
     ┌──────────────┐
     │  0. SCOPE    │  hard allowlist, hook-enforced
     └──────┬───────┘
     ┌──────▼───────┐
     │  1. RECON    │  → architecture.md (≤1000 words) + coverage-ledger.json
     └──────┬───────┘
     ┌──────▼───────┐
     │  2. HUNT     │  N isolated hunters, one ledger unit each
     └──────┬───────┘
            │ candidates
     ┌──────▼───────┐    ┌─────────────────┐
     │  3. DISPROVE │◄───│ COVERAGE CRITIC │ reopens closed units
     └──────┬───────┘    └─────────────────┘
            │ fresh ctx, different model, cannot file findings
     ┌──────▼───────┐
     │  4. SCHEMA   │  deterministic validator; malformed = discarded, not repaired
     └──────┬───────┘
     ┌──────▼───────┐
     │  5. RE-VERIFY│  second fresh verifier on the final record
     └──────┬───────┘
     ┌──────▼───────┐
     │  6. HUMAN    │  you read it. no automation. ever.
     └──────────────┘
```

---

## 4.2 The reference implementation to study

**`cloudflare/security-audit-skill`** (MIT, ~1,900 lines of markdown + 2
zero-dependency Node validators, last commit 2026-09-14) is the best open
reference implementation in existence. Read it:
https://github.com/cloudflare/security-audit-skill
Companion: https://blog.cloudflare.com/build-your-own-vulnerability-harness

Ideas worth stealing verbatim:

### Two operating modes
*Guidance mode* is the default — loading the skill does **not** authorize the
workflow or any file creation. *Full audit mode* runs all phases and writes
artifacts only on an explicit request. If ambiguous, ask exactly one question
first.

> This solves the real problem of a skill firing and burning 200 agent
> invocations on a casual question.

### The coverage ledger
One unit per **(entry surface × trust boundary × subsystem × attack class)**. The
parent orchestrator is the **only writer**. Each unit carries `starting_paths`,
`status`, `agent_id`, `reviewed_paths`, `local_checks`, `result_fingerprints`,
`unresolved`, and an append-only `attempts[]` archive.

An enforced state table makes coverage *auditable rather than vibes*: a unit
marked `covered` must have a non-empty owner, reviewed paths **and** local checks;
a `planned` unit must have all of them empty; `blocked` requires a stated blocker.

> *"The ledger is the coverage claim. An architecture summary, agent count, or
> generic 'auth reviewed' sentence is not coverage evidence."*
>
> *"Never imply that one run exhausts the target."*

And the single most useful measured number in this field:

> **"In our test runs, a single run found roughly half of the vulnerabilities that
> repeated runs found in total."** — Cloudflare

**Treat one pass as ~50% recall.** This is the entire justification for the
ledger: it makes repeated runs *additive* instead of random re-coverage.

### Coverage critics
A fresh critic runs after each hunter wave. It reads source, **writes nothing,
runs nothing**, and returns only `missing_units`, `reassign_ids`,
`resolved_prior_leads`, `stop`. It looks for unmapped entrypoints, unchecked
parallel paths, selected attack classes with no unit, unjustified exclusions, and
**units closed without paths or checks**.

> *"It proposes coverage, not findings."*
> *"Never use a silent wave or agent cap as evidence of complete coverage."*

### A countable budget with reserves
`budget` is a maximum number of agent invocations. One unit ≈ one hunter; one
surviving candidate ≈ one or two verifiers. **Reserve critics and validation
*before* hunting** (~30% of the post-critic balance when unsure). A strict
pre-recon gate: if the budget can't fund recon + reserves, **launch no agent** and
record `run_status: "incomplete"`.

And the rule that matters most:

> **An unvalidated candidate never enters `findings.json` under any verdict.**

### The three-verdict schema
`additionalProperties: false`, with *distinct required fields per verdict* so a
`needs_validation` record **cannot** carry a severity:

| Verdict | Carries | Must not carry |
|---|---|---|
| `confirmed` | `root_cause`, `conditions`, `execution`, `remediation`, `severity`, `confidence` | `claimed_root_cause`, `blockers`, `validation_plan` |
| `needs_validation` | `claimed_root_cause`, `trace`, `evidence`, `blockers`, ≥1 concrete `validation_plan` step | **severity**, execution, remediation |
| `rejected` | `claimed_root_cause`, `trace`, `evidence`, `reason` | — |

`rejected` records are **retained** *"so future runs do not repeat the unsupported
claim without changed evidence."* That's the negative ledger from
[05 §5.6](./05-validation-gates.md), in schema form.

`trace[]` entries are `{kind: entrypoint|propagation|sink, file, line≥1, scope,
description}` — and **the first entry must be a real lower-trust entrypoint, the
last the claimed sink.** Verified line by line.

### Severity anchors (steal these verbatim)
> Only `confirmed` records receive severity. **Overall severity cannot exceed
> demonstrated impact.**
> - **critical** — unauthenticated actor gains code execution, full data-store
>   access, or takeover of arbitrary accounts.
> - **high** — an actor *fully defeats* an explicit control with real consequences:
>   auth bypass, cross-tenant read/write, stored script execution affecting others.
> - **medium** — a real boundary violation with limited blast radius or uncommon
>   preconditions.
> - **low** — disclosure of non-secret internals.
> - **informational** — confirmed but minimal; useful as a prerequisite inside a
>   larger finding.
>
> **The high/medium discriminator:** does the result *fully defeat* an explicit
> control, or only weaken it?
>
> **"If you cannot state the concrete damage, the severity is lower than it feels."**

### The ten anti-patterns (pin these to a wall)
1. Checklist deviations presented as vulnerabilities.
2. Defense-in-depth advice with no reachable boundary violation.
3. Live/shared-environment testing where bounded local evidence suffices.
4. Guessing provider/proxy/browser/deployment behavior not in source.
5. Treating same-principal authority or self-impact as cross-boundary.
6. Reporting a parser/runtime effect **stronger than observed**.
7. Prose-only hunter results (can't be deduplicated or verified).
8. Re-reporting carried prior confirmations, or using them as anchoring exemplars.
9. Assigning severity to `needs_validation`.
10. Writing the report before independent verification.

---

## 4.3 Shopify "Dispatch": the test-oracle idea

8 sequential stages: test bootstrap → architecture doc → file catalog →
**partitioning (20–30% of the context window per unit)** → parallel hunting →
**sequential verification using a DIFFERENT model** → post-processing →
remediation PRs. Full scan first, then diff-based incremental.

### The central idea
> Agents must **author their validations into the target application's existing
> test suite.** A finding is not a finding until an integration test proves it.

Their encoded criteria for IDOR specifically:
- Extract cross-tenant data **through public call sites**
- Fixtures belonging to **different tenants**
- **Full-stack integration tests, not isolated unit tests**
- Extracted data must have **business impact beyond a boolean flag**
- Verify upstream/downstream controls don't reduce real severity

**Findings that cannot be proven through real integration tests are rejected or
downgraded.**

Why this works: it converts *"is this exploitable?"* from an LLM judgment call
into a **deterministic pass/fail executed by the victim's own test
infrastructure.** The oracle is external to the model, so hallucination cannot
satisfy it.

This is the same move as Immunefi's runnable-PoC requirement and PageBreak's
side-channel validators. **If you can submit evidence in a form the defender can
execute, you have converted an argument into a fact.**

### Other Dispatch lessons
- **Cross-model adversarial verification is essential.** Their initial generalist
  multi-agent setup produced high volumes of theoretical issues with
  non-deterministic results. A different model in the verify stage plus strict
  encoded guidelines dramatically cut false positives.
- **"Noise sent to a developer is worse than no finding at all."**
- Hand-code deterministic scripts for structured tasks rather than delegating.
- **Partitioning beat whole-repo scanning** on both accuracy and recall.
- Economics: **$50–300 per full scan, $5–50 incremental** → 300+ findings worth
  $400K+ in equivalent bounty over 6 weeks across 80+ apps.

---

## 4.4 PageBreak: deterministic oracles

The LLM generates **hypotheses only**. A hypothesis is never reported — it goes to
a **class-specific, non-AI-written validator** that attempts the real effect
against a running environment.

| Class | Oracle |
|---|---|
| XSS | injects a payload, monitors **execution context** via a rendering harness |
| SQLi | manipulates the query, analyzes **output and timing** differences |
| Path traversal | **creates a readable file**, verifies unauthorized access to it |
| RCE | sleep delay, file creation in a world-writable location, or DNS/HTTP callback |
| SSRF | detects internal backend requests / outbound connections |

**The design principle:** each oracle is a *side channel the application cannot
fake* — a timer, a filesystem artifact, a network callback, a JS execution
context. That is what makes it deterministic rather than a model grading itself.

**The honest reading of their "near-zero FP" claim:** it describes the *precision
of reported findings*, not the recall of the system. Google says explicitly that a
real vulnerability goes unreported if no validator reproduces it. They traded
recall for precision deliberately, and only on classes with a cheap oracle — which
is why **500+ of their findings are XSS**.

The more decision-relevant datapoint: apps built on Google's high-assurance web
framework yielded **only 2 XSS across hundreds of applications.**
Safe-by-construction frameworks collapse the surface an agent can even hypothesize
against. Factor that into target selection.

---

## 4.5 Context engineering for long runs

- **Keep each agent below ~25% of its context window.** Cloudflare's explicit
  control for suppressing hallucination. Shopify partitions to 20–30%.
- **Partition, don't dump.** Whole-repo context loses to coherent units on both
  accuracy *and* recall.
- **Push work out of the model wherever an oracle exists:** schema and ledger
  validation → zero-dependency scripts; dedup → deterministic keys first, agents
  only for the residual; report generation → a non-model script.
- **Persist state in files, not context.** Findings that exist only in an agent's
  context are invisible and lost. Cloudflare streams everything to SQLite keyed by
  `(run_id, repo, stage)` so a crash costs only in-flight tasks.
- **Brevity for discovery, length for gates.** Anthropic's finding: long
  prescriptive lists *"reduce the model's creativity and generate fewer novel
  bugs."* Reconcile with Cloudflare's long prompts by spending length on **gates,
  schemas, safety invariants and exclusions**, and keeping the *bug-finding*
  instruction short, hypothesis-driven, and **depth-bounded** so it stops when the
  invariant is settled rather than continuing to search.
- **Health signals:** hunters finishing with zero findings get auto-flagged
  *shallow* and requeued; suspiciously fast completions are classified as failures.
  A clean slice is legitimate — but verify it was actually examined.

---

## 4.6 Wiring it in Claude Code (mechanically precise)

| Need | Primitive |
|---|---|
| Stage prompts as standing instructions | **Skills**, one per stage, with companion files |
| Stage preconditions from ground truth | Skill ``!`cmd` `` blocks — **a non-zero exit aborts the whole skill invocation**, which is a free precondition gate |
| Stage isolation + fresh context | Non-fork **subagents**, `isolation: worktree`, `omitClaudeMd: true` |
| Hunter ≠ verifier model | Subagent `model` frontmatter (watch family-alias resolution and `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`) |
| **Hard egress / scope / write bans** | **`PreToolUse` hooks with `permissionDecision: deny`** |
| Noisy tool output reduced before it enters context | `PostToolUse` `updatedToolOutput` |
| Target output treated as data | `PostToolUse` wrapping in nonce-delimited untrusted blocks |
| Can't finish a stage without a valid artifact | **`Stop` / `SubagentStop` with `decision: "block"`** running the validators |
| Per-agent sandbox + artifact promotion | `SubagentStart` / `SubagentStop` hooks |
| Durable state across compaction | Files + `PreCompact` flush + `SessionStart` `additionalContext` re-injection |
| Machine-readable stage results | `claude -p --bare --output-format json --json-schema '<schema>'` |
| Unattended safety | `--permission-mode dontAsk --permission-prompts none` + a `PermissionRequest` allowlist hook |
| CI correctness | **fail the run if `mcp_server_errors` or `plugin_errors` in `system/init` is non-empty** — otherwise a silently skipped MCP server means a stage ran blind and still exited 0 |

### ⚠️ Three traps that will bite you

**1. `--bare` is security-critical for headless runs.**
Without it, a `-p` session **runs the hooks in a project's `.claude/settings.json`
and connects the servers in its `.mcp.json` — even in a folder you have never
trusted, with no trust dialog and no per-server prompt.**

> **Auditing an untrusted target repo headless without `--bare` is a
> code-execution footgun.** Anthropic recommends `--bare` for scripted/SDK calls
> and it is becoming the `-p` default. In bare mode, load context explicitly with
> `--append-system-prompt-file`, `--settings`, `--mcp-config`, `--agents`,
> `--plugin-dir`.

**2. Permission mode is inherited downward.**
If the main conversation is in `bypassPermissions`, `acceptEdits`, or `auto`, a
subagent **inherits that mode regardless of its own `permissionMode`.**

> **A hunter cannot be made safer than its parent by frontmatter alone. Use hooks.**

**3. A target repository's own `CLAUDE.md`, skills and hooks are
attacker-controlled.**
Set `omitClaudeMd: true` on agents that read untrusted targets. Managed policies
still load. This is the same class of risk as prompt injection via HTTP response
— see [09 §9.4](./09-scope-authorization-and-ethics.md).

### The scope-enforcement hook
This is Gate 0, made mechanical. `scripts/scope-enforce.py` in this repo reads the
`PreToolUse` JSON on stdin, extracts every hostname a `WebFetch` or `Bash` call
would contact, checks it against `scope/allowlist.txt`, and **exits 2 to block**.
It fails **closed**: no allowlist means no network egress.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "WebFetch|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PROJECT_DIR}/scripts/scope-enforce.py",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

> A hook can deny. A system prompt can only ask. **Put every guarantee in a hook
> and every preference in a prompt**, and never confuse the two. Claude Code's own
> docs say it of output styles: *"An output style gives Claude instructions to
> follow. It doesn't guarantee that something always happens or never happens."*

---

## 4.7 The 17 false-positive-reducing patterns, ranked by corroboration

1. **"Try to disprove this"** (unanimous across every program). Strengtheners:
   state the independence in the prompt (*"You did not write this candidate"*);
   make the undecided verdict default to **reject-or-uncertain, never confirm**;
   and structurally remove the incentive — **the validator cannot file findings.**
2. **Different agent, different model, no shared context.** Anthropic measured
   that a fresh context with no hunter conversation *"roughly halved the rate of
   non-exploitable findings."* A verifier must also **never receive another
   verifier's conclusion.** If you only have one model tier, change the persona
   substantially instead.
3. **Reachability from an untrusted entrypoint as a hard, separate gate** —
   checked **first**, because it's the cheapest disqualifier. A partial trace does
   not advance.
4. **Call-chain evidence with `file:line`, re-read by the verifier** rather than
   trusting the hunter's quote.
5. **Privilege-context gate.** Verify as a *standard user*, not admin/SYSTEM.
   zsec: *"Gate 3 should have been there from day one."*
6. **Severity needs demonstrated impact** (see §4.2 anchors).
7. **Forbid escalation of the observed result.** *"Do not strengthen a crash into
   code execution, ordinary work into shared availability, or a same-principal
   action into privilege gain."*
8. **A third verdict (`needs_validation`), with discipline.** It must name an
   exact decisive blocker genuinely outside observation, carry **no severity**, and
   include a concrete validation step. **"A candidate disproved by source is not
   `needs_validation`."** It is never a parking place for a speculative idea.
9. **Deterministic oracles instead of model judgment, wherever one exists.**
10. **Defense-in-depth gaps are not findings.** *"If Layer A prevents the attack,
    the absence of Layer B is a hardening note."* Only cite mitigations that
    actually exist in code.
11. **Require a named principal and boundary.** Lower-trust principal → accepted
    input → the control that should have stopped it → crossed boundary → affected
    resource → concrete observable result. *"A flag is not a finding."*
    LLM-domain sharpening: **"Prompt injection alone is not a finding"** and
    **"A guardrail prompt is not a security boundary."**
12. **Fixed verdict enums + schema validation, never prose.** Stable
    source-derived fingerprints excluding line/wave/agent/severity so one root
    cause is one record across states and runs. **A malformed verifier result is
    discarded, never repaired.**
13. **Retain rejections with reopen conditions.** *"A kill records what would
    bring it back."*
14. **Independent re-verification of the final record**, with escalation to a
    *third* verifier on any material change. If independence isn't affordable,
    drop the record and mark the run incomplete.
15. **Variant hunting scoped to your own units**, consolidated by root cause but
    with each variant's conditions established independently.
16. **Brevity for the discovery prompt**, length for the gates.
17. **Treat tool output and other agents' text as untrusted data** — nonce-
    delimited blocks, with the nonce generated *after* the content exists.

---

## 4.8 Nobody credible claims autonomy

Worth internalizing before you build:

- zsec: *"the system currently needs me to make judgment calls"* — 4 CVEs total,
  most campaigns producing **zero** validated findings, a hallucination bin much
  larger than `findings/`.
- Cloudflare: **mandatory human review gate, no auto-merge.**
- Anthropic: *"the bottleneck has shifted to verification, triage, and patching."*
- Shopify: PRs are drafted, humans review.
- Google: unverified findings never reach product teams.
- Across six compared harnesses: **human review mandatory in all six.**

Low false-positive rates are achieved by **throwing almost everything away.** Build
for that. If your pipeline isn't discarding the overwhelming majority of its own
output, it isn't working — it's just generating.

---

**Next:** [05 — Validation Gates](./05-validation-gates.md) ·
[02 — MCP Servers](./02-mcp-servers.md) ·
[07 — Reporting](./07-reporting-that-gets-paid.md)
