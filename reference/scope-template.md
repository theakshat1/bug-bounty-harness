# Scope — \<PROGRAM NAME\>

> Copy to `scope/<program>.md`. **Copy scope verbatim from the live policy — never
> paraphrase it.** Re-read the live policy if `VERIFIED` is more than 14 days old;
> assets get acquired, divested and re-pointed.

```
VERIFIED:    2026-10-02          # date you last read the live policy
POLICY_URL:  https://...
PLATFORM:    hackerone | bugcrowd | intigriti | yeswehack | self-hosted
SAFE_HARBOR: yes | no | partial  # and where it's stated
PROGRAM_STATE: in_progress | paused | closed   # from the platform's state field, not the copy
AI_POLICY:   <verbatim clause, or "none found">  # a ban = OUT; a disclosure rule → report
SOURCES:     <which section came from the live brief, the embedded JSON, a mirror, the vendor>
```

## QUALIFYING_CONDITIONS   # open-source product programs: copy the vendor's own rules
```
<verbatim: reproduce on latest release AND master? unmodified binaries? release builds
 only? experimental features excluded? which component counts?>
```

## SEVERITY_TABLE          # the program's own tiers and what LOWERS severity
```
<verbatim>
```

## TEST_TARGET             # what you actually send traffic to
```
<hosted asset, or: "local instance of release <version> (official artifact), stand-in for
 <hosted asset> under rule <n>">
```

## ALLOWLIST
Hosts and patterns that are in scope. These become `scope/allowlist.txt`.

```
example.com
*.example.com
api.example.com
```

## DENYLIST
Explicitly out of scope. **Denylist beats wildcard, always.** Prefix with `!` in
`allowlist.txt`.

```
!blog.example.com          # WordPress marketing, explicitly OOS
!*.partners.example.com    # customer tenants — real third-party data
!help.example.com          # Zendesk CNAME, third-party operator
```

## MCP-LOCAL servers
MCP servers that never contact the target, so the scope hook skips host checks for them.
Only for servers you know run locally and never fetch.

```
@mcp-local semgrep         # local stdio code analysis; hostnames in code are data
```

⚠️ **Never** list Burp, a recon wrapper, or anything with a URL parameter here — the hook
covers `mcp__*` tools precisely because those can otherwise send a request anywhere.

## PERMITTED
Verbatim from the policy.

## PROHIBITED
Verbatim from the policy. Expect to see: DoS/stress testing, social engineering,
physical, automated scanning above a rate, anything touching real users' data.

## RATE_LIMIT
```
<verbatim, or: "unstated — defaulting to 5 req/s, conservative">
```

## ACCOUNTS
Authorized test accounts. Two tenants minimum for isolation testing.

```
tenant-a:  acct-a@...        # attacker role
tenant-b:  acct-b@...        # victim role
canary-b:  CANARY-B-7f3a     # unique string in B's data, for unambiguous proof
lowpriv:   user@...          # within tenant A
elevated:  admin@...         # within tenant A
```

## ACCEPTED_RISK
**The highest-value section.** Bugs the program states it will not pay for. Check
every finding against this before submitting — it's the cheapest way to avoid
wasting a report, and it feeds the impact gate.

```
<verbatim from policy>
```

## AI POLICY
```
Disclosure required?   yes | no          # only Intigriti, Django, FFmpeg of 53 surveyed
Human verification required?  yes | no   # 13 of 16 AI-addressing programs
Autonomous submission allowed?  no       # assume no
```

## IN_SCOPE_AGENT_TOOLS
If the target has AI/agent features, enumerate which tools the policy puts in
scope. **If the policy doesn't say, ask before testing** — agent tool scope is the
#1 policy ambiguity of 2026.

```
<list, or: "UNSTATED — asked program on <date>, awaiting answer. Do not test.">
```

## NOTES
- Third-party assets under the wildcard (check CNAMEs before testing)
- Whether the GitHub org / CI-CD is in scope (usually **not**)
- Anything you asked the program and are waiting on
- Known crowded areas to deprioritize
