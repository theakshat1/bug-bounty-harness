---
name: scope-guard
description: Gate 0 — verify a target host, URL, or asset is in scope and the technique is permitted BEFORE any request is sent. Use at the start of every campaign, whenever a new hostname appears from recon/JS/redirects, and before any active testing. Also use to set up the scope allowlist for a new program.
argument-hint: "[hostname-or-url]"
---

# Scope Guard — Gate 0

You are enforcing the **first and only non-negotiable gate**. No finding, however
good, survives an out-of-scope asset. No bounty is paid for testing something the
program does not own.

## Operating rule

> If scope cannot be positively confirmed, the answer is **NO**. Absence of a
> prohibition is not permission.

## Step 1 — Load the scope file

Read `scope/<program>.md` in the working directory. If it does not exist, you
cannot proceed with active testing. Create it first (see Step 5).

The file must contain:
- `ALLOWLIST` — exact hosts and wildcard patterns that are in scope
- `DENYLIST` — explicitly out-of-scope hosts (these override wildcards)
- `PERMITTED` — techniques the program allows
- `PROHIBITED` — techniques the program forbids
- `RATE_LIMIT` — stated request-rate ceiling
- `ACCOUNTS` — the test accounts you are authorized to use
- `VERIFIED` — the date you last re-read the live program policy

If `VERIFIED` is more than 14 days old, re-read the live policy before testing.
Scope drifts: assets get divested, acquired, and re-pointed.

## Step 2 — Resolve what the host actually is

A hostname matching a wildcard is **not** sufficient. Check ownership before
testing:

```bash
# Who does this actually resolve to, and who operates it?
dig +short CNAME <host>
dig +short A <host>
```

Then classify:

| Observation | Verdict |
|---|---|
| CNAME points to a third-party SaaS (zendesk, github.io, herokuapp, shopify, netlify, s3, azurewebsites, cloudfront-with-foreign-origin) | **OUT** unless the program explicitly lists that third-party asset. Testing it attacks the vendor, not your target. |
| A record in the target org's own netblock / their stated cloud account | In scope if it matches `ALLOWLIST` |
| Host appears only in a JS bundle, never resolves | Not testable; record as intel only |
| Host is on `DENYLIST` | **OUT** — denylist beats wildcard, always |
| Host is a partner/customer-branded instance under the wildcard | **OUT** pending clarification — this is multi-tenant customer data |

**The dangling-CNAME exception:** if a CNAME points to an unclaimed third-party
resource, that is a potential subdomain takeover on a host the target controls —
that *is* in scope as a finding, but do **not** claim the resource. Report the
dangling record. Claiming it to "prove" it is an action against the third party
and risks hijacking real traffic.

## Step 3 — Check the technique, not just the asset

Match what you intend to do against `PROHIBITED`. Reject, without exception:

- Denial of service, load/stress testing, resource exhaustion
- Automated scanning above `RATE_LIMIT`
- Social engineering of staff or users
- Physical access attempts
- Anything touching a real user's account or data
- Credential bruteforce / password spraying (unless explicitly permitted)
- Persistence of any kind
- Bulk data extraction

If the technique is prohibited, the test does not happen. Do not look for a
variant that is "technically not what they said".

## Step 4 — Emit the verdict

Output exactly this block, and nothing softer:

```
SCOPE VERDICT: IN | OUT | UNCLEAR
  Asset:      <host/url>
  Resolves:   <A / CNAME result and who operates it>
  Matched:    <the ALLOWLIST line that covers it, verbatim>
  Technique:  <what you intend to do>  → PERMITTED | PROHIBITED
  Rate cap:   <RATE_LIMIT>
  Accounts:   <which authorized test accounts you will use>
  Policy read: <VERIFIED date>
```

On `OUT` or `UNCLEAR`: stop. State what specific question the program must
answer. Do not test while waiting for the answer.

## Step 5 — Bootstrapping a new program

When no scope file exists, build one from the live policy. Fetch the program
policy page and extract verbatim — never paraphrase scope:

```markdown
# Scope — <program>
VERIFIED: <today>
POLICY_URL: <url>

## ALLOWLIST
*.example.com
api.example.com
<copy the scope table exactly>

## DENYLIST
blog.example.com        # WordPress, marketing, explicitly OOS
*.partners.example.com  # customer tenants

## PERMITTED
<verbatim from policy>

## PROHIBITED
<verbatim from policy>

## RATE_LIMIT
<verbatim, or "unstated — default to 5 req/s and stay conservative">

## ACCOUNTS
tenant-a: <your test account>
tenant-b: <your second test account>

## ACCEPTED_RISK   # bugs the program says it will not pay for
<verbatim — check findings against this before submitting>
```

Capture `ACCEPTED_RISK` carefully. It is the cheapest way to avoid wasting a
report, and it feeds Gate 3 (impact).

## Step 6 — Make it mechanical

Prompting yourself is not a control. Generate `scope/allowlist.txt` and let the
`PreToolUse` hook (`scripts/scope-enforce.py`, shipped with this plugin) hard-block
out-of-scope hosts.

```
# scope/allowlist.txt
*.example.com            # wildcard: apex + any depth of subdomain
api.target.io            # exact host
!blog.example.com        # explicit deny — beats any wildcard
@mcp-local semgrep       # this MCP server never touches the target
```

**`@mcp-local` matters and is easy to get wrong.** The hook covers `mcp__*` tools,
because allowlisting `mcp__burp__send_http1_request` permits the *tool* but says nothing
about which *host* it may reach — an MCP server is otherwise a complete scope bypass. For
a server that genuinely only runs locally (Semgrep over stdio, a filesystem server), a
hostname inside the data it analyzes would otherwise look like a target, so mark it
exempt. **Never mark Burp, a recon wrapper, or anything with a URL parameter as local.**

Verify the hook actually blocks before you trust it:

```bash
echo '{"tool_name":"WebFetch","tool_input":{"url":"https://not-in-scope.test/"}}' \
  | python3 scripts/scope-enforce.py; echo "exit=$?"     # expect 2
echo '{"tool_name":"mcp__burp__send_http1_request","tool_input":{"host":"not-in-scope.test"}}' \
  | python3 scripts/scope-enforce.py; echo "exit=$?"     # expect 2
bash scripts/test-scope-enforce.sh                        # full suite
```

The hook **fails closed**: with no `scope/allowlist.txt`, every outbound network call is
blocked. That is deliberate.

A hook can deny. A system prompt can only ask.

## Red flags that mean STOP and ask the program

- The asset handles payments or healthcare data and scope is ambiguous
- You are about to test something that would affect other tenants
- A finding can only be proven by accessing data you don't own
- Scope says "all our assets" with no enumeration (get an explicit list)
- You found an asset that looks like it belongs to an acquisition not yet listed
