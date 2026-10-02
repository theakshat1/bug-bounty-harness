# Scope — \<PROGRAM NAME\>

> Copy to `scope/<program>.md`. **Copy scope verbatim from the live policy — never
> paraphrase it.** Re-read the live policy if `VERIFIED` is more than 14 days old;
> assets get acquired, divested and re-pointed.

```
VERIFIED:    2026-10-02          # date you last read the live policy
POLICY_URL:  https://...
PLATFORM:    hackerone | bugcrowd | intigriti | yeswehack | self-hosted
SAFE_HARBOR: yes | no | partial  # and where it's stated
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
