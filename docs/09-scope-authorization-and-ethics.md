# 09 — Scope, Authorization, and Ethics

> This is the first doc to read and the last gate before every submission.
> Everything else in this knowledge base assumes you have **written authorization**
> for the target you are touching. Without that, the techniques here are not
> bug bounty — they are unauthorized access.

---

## 9.1 The authorization test

Before a single request leaves your machine, you must be able to answer all five
in writing:

| # | Question | Where the answer lives |
|---|---|---------|
| 1 | Is this asset **explicitly in scope**? | Program policy scope table |
| 2 | Is the **technique** I'm about to use permitted? | Policy "out of scope / prohibited" section |
| 3 | Is my **testing volume** within stated rate limits? | Policy, often a `Rate limiting` clause |
| 4 | Am I using a **program-provided test account**, or my own? | Policy, program notes |
| 5 | If I find something, is there a **path to disclosure**? | Policy, response SLA |

If any answer is "I'm not sure" — the answer is **no**. Stop and ask the program.

**Wildcard scope is not infinite scope.** `*.example.com` in scope does not mean
a third-party SaaS instance CNAMEd under that wildcard is in scope. Check who
actually operates the host before testing it. Shared/third-party infrastructure
is the most common way hunters accidentally go out of bounds.

### Asset drift
Scope changes. Assets get acquired, divested, and re-pointed. A host that was in
scope last month may belong to someone else now. Re-verify scope at the start of
every campaign, not once per program.

---

## 9.2 Hard limits that apply even when "in scope"

These are near-universally prohibited and will get you banned (and can be
criminal) regardless of what the scope table says:

- **Denial of service / resource exhaustion** — including accidental DoS from
  aggressive scanning, and including "proving" a DoS bug by actually causing one.
- **Data exfiltration at volume.** Proving you can read one record you shouldn't
  is the finding. Dumping the table is an incident you caused.
- **Pivoting / lateral movement** beyond the initial finding without explicit
  written permission to continue.
- **Persistence.** Never leave a backdoor, a webshell, a scheduled job, or a
  created admin account. Clean up test artifacts and say so in your report.
- **Touching real users' data.** Use your own accounts on both sides of an
  access-control test. If a bug inherently exposes third-party data, stop at the
  minimum proof and report immediately.
- **Social engineering** of staff or users, unless the program explicitly runs a
  social engineering track.
- **Physical** access, and anything involving staff devices or premises.
- **Testing non-production systems you weren't pointed at**, and staging/dev hosts
  that aren't listed even if they're reachable.

### The escalation pause
When a finding *could* be chained deeper (an SSRF that might reach metadata, an
auth bypass that might reach another tenant), the correct move is:

1. Stop at the last safe, provable step.
2. Document what you have.
3. Report it, and **ask in the report** whether the program wants you to continue
   the chain.

Programs routinely grant permission to deepen a chain, and routinely pay more for
the chained impact. Asking costs you a day; not asking can cost you the bounty
and the account.

---

## 9.3 Multi-tenant and third-party blast radius

The highest-risk mistakes in modern hunting are not aggressive payloads — they
are tests that cross a tenant boundary into a real customer.

Before testing an access-control or isolation bug:

- Create **two accounts you control**. Tenant A and Tenant B are both yours.
- Never use a discovered identifier that might belong to a real customer. If an
  enumeration returns UUIDs, do not "just check one" — that one is someone's data.
- For isolation bugs, the proof is *your* Tenant A reading *your* Tenant B. That
  is fully sufficient evidence and carries zero collateral damage.

If you cannot construct a two-account proof, report the *reachability* with the
evidence you safely have and let the program verify the crossing internally.

---

## 9.4 AI-specific ethics (2026)

The agentic era added failure modes that did not exist a few years ago. These are
now the most common ways a competent hunter damages their own reputation.

### Never submit what you have not personally verified
An LLM asserting a vulnerability exists is a **hypothesis**, not a finding. The
entire architecture in [04 — Harness Architecture](./04-harness-architecture.md)
and [05 — Validation Gates](./05-validation-gates.md) exists because of this.
Submitting unverified model output is the defining sin of the current era, it is
what triggered platform-wide policy tightening, and it is individually traceable
to you.

### Disclose AI assistance when the program asks
Few programs require it. An independent census of 53 programs (Arafat Afzalzada,
2026-07-28, CC BY 4.0, rubric fixed before reading policy text) found **only 3 require
AI-use disclosure — and one of those three inverts the requirement**
**[S — one researcher's dated snapshot, attributed by name]**:

| Program | What it actually asks for |
|---|---|
| **Intigriti** | *"be open and transparent about the use of AI and to disclose when and how AI was used"* |
| **Django** | *"disclose which AI tools were used and what they were used for"* |
| **FFmpeg** | **not an AI declaration at all** — it asks for *"the name or alias of the human reviewer who verified it"* |

Non-disclosure where required is a policy violation independent of whether the bug is
real.

> **FFmpeg's variant is the one to internalize.** It is a **named-accountability**
> control, not a disclosure control — and it is the one requirement an autonomous
> pipeline **structurally cannot satisfy** without a human actually reading the report.
> Which is exactly this harness's non-negotiable #2.
>
> **If you cannot name the human who verified a finding, you do not have a submittable
> finding.** A few programs now make that explicit. Treat it as the standard everywhere.

### Keep the agent inside scope mechanically, not by hope
An autonomous agent will happily follow a redirect, a link in a JS bundle, or a
hostname in an API response straight out of scope. Prompting is not a control.
Enforce scope with:

- An explicit **allowlist** the agent must check before any request (see the
  `scope-guard` skill).
- A `PreToolUse` **hook** that hard-blocks network tools against non-allowlisted
  hosts. A hook can deny; a system prompt can only ask.
- Deny-by-default network egress in the sandbox where you run the agent.

### Treat all target output as hostile input to your own agent
This is the inverted risk, and it is underrated. Content you fetch from a target —
HTTP responses, JS bundles, JSON fields, error messages, HTML comments, CI logs —
flows into your agent's context. A target that intentionally or accidentally
contains text resembling instructions can redirect your agent, cause it to leak
your notes, exfiltrate your tokens, or attack a third party *from your machine*.

Mitigations:
- Run the harness in a container with scoped credentials and no access to your
  real cloud keys, SSH keys, or password store.
- Never put platform API tokens, session cookies for unrelated services, or
  personal credentials in the same environment as an agent that reads target data.
- Treat MCP tool output the same way — see [10 — MCP as Target and as Risk](./10-mcp-as-target-and-risk.md).

### Don't automate submission
Human review before submit is not optional. A pipeline that files reports without
a human reading them is how accounts get banned and how programs stop accepting
AI-assisted work for everyone.

---

## 9.5 Evidence hygiene

Good evidence proves impact without creating new harm.

**Do:**
- Capture the minimum request/response pair that demonstrates the boundary failure.
- Redact tokens, cookies, and third-party PII in the report body; note that you
  hold the unredacted copy if triage needs it.
- Use your own accounts and your own canary data (`akshat-test-A`, `akshat-test-B`)
  so screenshots are unambiguous and harmless.
- Timestamp your testing window — it helps triage correlate their logs.
- State explicitly what you did *not* do ("I did not enumerate further records").

**Don't:**
- Paste third-party PII into the report.
- Host a loud public PoC. For takeover-style proofs, keep the public artifact
  minimal (a blank page, proof in an HTML comment) and put the verification
  instructions in the private report. A flashy public defacement-style PoC
  panics real customers and can turn a payout into a policy violation.
- Leave PoC infrastructure running after the report resolves.
- Include your scanning tool's full raw output as "evidence" — it's noise and it
  signals low effort.

---

## 9.6 Cleanup checklist

Run this at the end of every engagement, before you consider the work done:

- [ ] Test accounts documented in the report (so the program can remove them)
- [ ] No created admin/elevated accounts left behind
- [ ] Uploaded test files deleted, or their locations listed for the program
- [ ] Stored-XSS style persistent test payloads removed from the target
- [ ] Any PoC pages / collaborator subdomains taken down
- [ ] Local copies of target data minimized and encrypted; delete after resolution
- [ ] Scanning stopped (no forgotten background jobs still hitting the target)

---

## 9.7 When you get it wrong

You will, eventually, cross a line by accident — a scan hits an out-of-scope host,
a test causes a visible error, a query returns someone else's record.

**Self-report immediately.** Programs are overwhelmingly forgiving of honest,
promptly-disclosed mistakes and unforgiving of discovered-later concealment. Say
what happened, when, what data you touched, and what you did with it. Delete the
data and confirm the deletion in writing.

This is also the reason to keep a full local log of every request your harness
sends: when you need to prove exactly what you did and did not touch, that log is
the only thing that will do it.

---

## 9.8 The one-line version

> Authorized target, minimum necessary proof, nothing you haven't verified
> yourself, nothing left behind, and a human reads it before it ships.

---

**Next:** [00 — Start Here](./00-start-here.md) · [05 — Validation Gates](./05-validation-gates.md)
