# Researchy lane receipt — X bookmarks (past ~1 month)

**Status:** COMPLETE — 24/24 items, **0 blocked**
**Exclusive URLs only** (no overlap with other lanes).
**Artifacts:** `articles.jsonl` · `articles.md` · `posts.jsonl` · `posts.md`

## Themes (for KB merge)
1. **AI/agent harnesses for authorized hunting** — orchestration gates, coverage ledgers, adversarial verification, context compression (zsec harnesses, Cloudflare security-audit-skill, ripwire, Adverserial CyberKimi, Tsecbench).
2. **Classic BB recon→hunt pipelines** — multi-source attack-surface mapping, S3/ACL via dorks, secret-name regexes, Ars0n methodology-as-product, ProjectDiscovery-style workflows.
3. **Deep code-audit patterns (WordPress piece, patterns only)** — batch validate/execute desyncs, array-vs-scalar sanitizer gaps, privilege gadgets; plus cloud multi-tenant isolation, JS graveyard endpoints, 403 header trust, Azure residue.

## Articles (12/12 OK)
| # | Source | Class | Idea (1-line) | Tags |
|---|--------|-------|---------------|------|
| 1 | https://BugBountyHunting.com | education / class taxonomy | Checklist classic sinks: XSS/IDOR/SSRF/SQLi/RCE by input→sink | education,xss,idor,ssrf |
| 2 | https://adverserial.ai/docs.html | AI-assisted workflows | Wire cyber-tuned models into existing harnesses via OpenAI-shim; route cheap vs strong | llm,api,agent-tooling |
| 3 | https://blog.zsec.uk/harnessing-harnesses/ | LLM harness design | Orchestration > model: recon→hunt→validate→trace→report + adversarial validate + token budget | llm-harness,validation-gates |
| 4 | https://gist.github.com/h4x0r-dz/be69c7533075ab0d3f0c9b97f7c93a59 | secret name regex | Hunt by key *names* near assignments, not only token formats | secrets,recon |
| 5 | https://github.com/R-s0n/ars0n-framework-v2 | BB workflow platform | Methodology-as-product: UI-gated stages + unified DB + learn-why | framework,recon,beginner |
| 6 | https://github.com/cloudflare/security-audit-skill | coverage-led AI audit | Six gated phases + coverage ledger + adversarial disprove verifiers | cloudflare,coverage-ledger |
| 7 | https://github.com/redhat-et/ripwire | agent context compression | Call-graph/blast-radius map before dumping files into agent context | ripwire,mcp,context |
| 8 | https://hackerone.com/blog/oath-bug-bounty-program-update-1m-payouts-and-expansion-program | program policy (historical) | Track payout tables + newly unified scopes; prioritize top-ranked classes | hackerone,policy |
| 9 | https://infosecwriteups.com/my-complete-bug-bounty-hunting-workflow-every-command-i-use-step-by-step-68484276471f | BB workflow | Fixed pipeline: multi-source enum → param buckets → business logic → secrets → report | workflow,projectdiscovery |
| 10 | https://medium.com/@Seek404/when-a-simple-google-dork-led-to-an-s3-misconfiguration-and-sensitive-data-exposure-4d7d86f54b16 | S3 misconfig | Dork → bucket path → listing + unsigned serve chain | s3,cloud,dork |
| 11 | https://slcyber.io/research-center/exploit-brokers-pay-500000-for-a-wordpress-rce-i-found-one-with-gpt5-6/ | LLM-assisted code audit | Hunt batch validate/execute desync, array/scalar sanitizer gaps, privilege gadgets (no PoCs) | wordpress,desync,agentic |
| 12 | https://tsecbench.zc.tencent.com/#leaderboard | offensive-AI benchmarks | Calibrate harnesses via public agentic red-team leaderboards | tsecbench,benchmark |

## Posts (12/12 OK)
| Source | Class | Idea (1-line) | Tags |
|--------|-------|---------------|------|
| https://x.com/zseano/status/2105766060398162315 | program intel | Prioritize by public H1 activity/payout signals | hackerone,prioritization |
| https://x.com/bountywriteups/status/2103890018670616715 | DAST tooling | Crawl+JS+API+replay evidence in one workflow | DAST,crawling |
| https://x.com/GoogleVRP/status/2099890989775093810 | broken authz / internal API | Test whether library wrappers enforce caller authz at every entry | authorization,Google-VRP |
| https://x.com/ethical_h4ck3r_/status/2099352309834588200 | 403 / header trust | Challenge spoofable IP/forwarding headers on 403 paths | 403-bypass,access-control |
| https://x.com/adnanthekhan/status/2099136955250352428 | multi-program orchestration | Parallel agents only help if triage/dedupe quality keeps up | automation,orchestration |
| https://x.com/whotfbunny/status/2098862073057038746 | JS graveyard → authz | Mine dead /api|/admin routes then authz-diff, not status alone | JS-recon,IDOR,BOLA |
| https://x.com/payloadartist/status/2098056402954580039 | agentic ROI | Track token burn vs bounty — technical win can be negative ROI | agentic,ROI |
| https://x.com/orenyomtov/status/2097366728321749080 | cloud multi-tenant | Isolation must cover query text/metadata, not only results | AWS,Athena,multi-tenant |
| https://x.com/Hac10101/status/2097134370775818604 | Azure residue | Blob versions + Entra recon + vault/AKS loot paths | Azure,Entra,secrets |
| https://x.com/UK_Daniel_Card/status/2096709936449212502 | ops | Mobile-first remote session continuity for sustained triage | ops,mobile |
| https://x.com/0x0SojalSec/status/2096639626706649149 | local cyber LLM | Local models assist hypotheses; human verify + stay in scope | LLM,tooling |
| https://x.com/7h3h4ckv157/status/2096488638456717430 | CLI model routing | Proxy agentic CLIs to cheaper backends for iteration cost | Claude-Code,proxy |

## Blocked
None.

## Fetch notes
- Infosec Write-ups: WebFetch Cloudflare 403 → recovered via curl.
- Tsecbench: empty SPA WebFetch → recovered via curl + `/api/v1/benchmark-sets`.

@Orchester: ready to merge. Patterns only — no PoCs.
