# Researchy lane — Posts (deepened, non-repro)

**Audience:** Akshat (authorized / in-scope hunting only)  
**Lane:** Researchy (`/workspace/bb-bookmark-lane-researchy/`)  
**Items:** 12 tip / methodology posts  
**Constraint:** Expanded from existing lane extracts only. **No** reproduction steps, payloads, PoCs, exploit recipes, or attack procedures.

**Quality rollup:** ok=11 · thin=1 · blocked-recovered=0

---

### P.1 @zseano — Program intel / hunting prioritization

- **Root-cause class:** Program intel / hunting prioritization
- **Affected component:** Bug-bounty program policy / scope (operator-side historical)
- **Impact:** Better hunt ROI via program activity, payout tables, and newly unified scopes (ops/planning impact, not a vuln).
- **Conditions called out:** Access to public HackerOne program metadata / community dashboards
- **What the write-up/tweet teaches (abstract):** Use public-program activity and payout distribution signals to prioritize where researchers are currently succeeding, rather than hunting only by personal preference. Extract note: Teases public H1 program stats; points to forthcoming BugBountyHunter site. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** hackerone, program-intel, prioritization, bugbountyhunter
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://x.com/zseano/status/2105766060398162315](https://x.com/zseano/status/2105766060398162315)
- **Notes:** Teases public H1 program stats; points to forthcoming BugBountyHunter site.

---

### P.2 @bountywriteups — DAST / crawl-assisted recon tooling

- **Root-cause class:** DAST / crawl-assisted recon tooling
- **Affected component:** Authorized HTTP/browser targets (DAST workflow)
- **Impact:** Evidence-oriented findings vs one-off scans when crawl/JS/API/replay stay in one workflow.
- **Conditions called out:** Authorized target; ability to run local CLI scanner
- **What the write-up/tweet teaches (abstract):** Combine HTTP + browser-assisted crawling, JS analysis, API import, and replayable evidence into one workflow so findings stay evidence-oriented instead of one-off scans. Extract note: Promotes AKCA Go DAST scanner (github.com/akha-security/akca). Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** DAST, crawling, JS-analysis, AKCA, tooling
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://x.com/bountywriteups/status/2103890018670616715](https://x.com/bountywriteups/status/2103890018670616715)
- **Notes:** Promotes AKCA Go DAST scanner (github.com/akha-security/akca).

---

### P.3 @GoogleVRP — Broken authorization / internal API privilege boundary

- **Root-cause class:** Broken authorization / internal API privilege boundary
- **Affected component:** Internal library wrappers around storage/filesystem APIs (Google VRP surface as named)
- **Impact:** Lower-trust API paths reaching higher-trust file/storage operations when caller authz is missing at an entrypoint.
- **Conditions called out:** Access to in-scope Google surfaces; interest in internal API / library trust boundaries
- **What the write-up/tweet teaches (abstract):** When an internal library wraps storage/filesystem APIs, test whether caller authz is enforced at every entrypoint—or whether a lower-trust API path can reach higher-trust file operations. Extract note: Points to brutecat writeup on GFile / internal filesystems (~$100k). Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** authorization, internal-API, GFile, Google-VRP, writeup
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://x.com/GoogleVRP/status/2099890989775093810](https://x.com/GoogleVRP/status/2099890989775093810)
- **Notes:** Points to brutecat writeup on GFile / internal filesystems (~$100k).

---

### P.4 @ethical_h4ck3r_ — Access-control bypass via trusted client IP headers

- **Root-cause class:** Access-control bypass via trusted client IP headers
- **Affected component:** Paths returning 403 where app/WAF may trust forwarding headers
- **Impact:** Access-control decisions that trust spoofable identity/forwarding headers may incorrectly allow restricted paths.
- **Conditions called out:** Target returns 403 on sensitive paths; app or WAF may trust forwarding headers
- **What the write-up/tweet teaches (abstract):** On 403 responses, systematically challenge whether access decisions trust spoofable client-IP / forwarding headers (and similar identity headers) instead of true network identity. Extract note: Tip only; not always applicable—treat as header-trust differential test. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** 403-bypass, header-injection, IP-spoofing, access-control
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://x.com/ethical_h4ck3r_/status/2099352309834588200](https://x.com/ethical_h4ck3r_/status/2099352309834588200)
- **Notes:** Tip only; not always applicable—treat as header-trust differential test.

---

### P.5 @adnanthekhan — Multi-program automated hunting orchestration

- **Root-cause class:** Multi-program automated hunting orchestration
- **Affected component:** Multiple authorized BB programs (agent orchestration)
- **Impact:** Scale without triage/dedupe quality increases duplicate and false-positive load.
- **Conditions called out:** Authorized programs; compute for parallel agent runs; triage capacity for duplicates
- **What the write-up/tweet teaches (abstract):** Orchestrate parallel hunt agents across several programs, then invest in dedupe/triage quality—scale helps only if duplicate rate and false positives are managed. Extract note: Wild Hunt hack-bot orchestrator; claims RCEs/ATOs with high duplication. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** automation, orchestration, RCE, ATO, Wild-Hunt
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://x.com/adnanthekhan/status/2099136955250352428](https://x.com/adnanthekhan/status/2099136955250352428)
- **Notes:** Wild Hunt hack-bot orchestrator; claims RCEs/ATOs with high duplication.

---

### P.6 @whotfbunny — JS graveyard endpoint mining → authz testing

- **Root-cause class:** JS graveyard endpoint mining → authz testing
- **Affected component:** Historical frontend JS bundles / forgotten API routes
- **Impact:** Authorization failures (IDOR/BOLA, forgotten admin) on reachable historical routes the UI no longer links.
- **Conditions called out:** Readable JS bundles; authenticated and unauthenticated test accounts preferred
- **What the write-up/tweet teaches (abstract):** Mine historical frontend bundles for /api|/admin|/internal routes the UI no longer links, validate reachability, then focus authorization differentials (IDOR/BOLA, broken auth, forgotten admin) rather than status-code alone. Extract note: Strong reusable recon→authz pattern. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** JS-recon, dead-endpoints, IDOR, BOLA, API
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://x.com/whotfbunny/status/2098862073057038746](https://x.com/whotfbunny/status/2098862073057038746)
- **Notes:** Strong reusable recon→authz pattern.

---

### P.7 @payloadartist — Browser / Chromium RCE via autonomous agents (economics)

- **Root-cause class:** Browser / Chromium RCE via autonomous agents (economics)
- **Affected component:** Autonomous exploit-agent economics (meta)
- **Impact:** Technical agent success can still be negative economic ROI when token/cost burn exceeds bounty.
- **Conditions called out:** Interest in agentic hunting ROI, not a specific target recipe
- **What the write-up/tweet teaches (abstract):** When evaluating autonomous exploit agents, track token/cost burn against bounty outcome—technical success can still be negative ROI. Extract note: Commentary on $250k Chrome RCE by Xbow; cost question. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** Chrome, RCE, Xbow, agentic-hunting, ROI
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://x.com/payloadartist/status/2098056402954580039](https://x.com/payloadartist/status/2098056402954580039)
- **Notes:** Commentary on $250k Chrome RCE by Xbow; cost question.

---

### P.8 @orenyomtov — Cloud multi-tenant isolation failure (Athena query leakage)

- **Root-cause class:** Cloud multi-tenant isolation failure (Athena query leakage)
- **Affected component:** AWS Athena / multi-tenant query-analytics platforms
- **Impact:** Cross-tenant leakage of query text/metadata (not only result sets) on shared analytics platforms.
- **Conditions called out:** Authorized cloud research scope; interest in shared analytics/query services
- **What the write-up/tweet teaches (abstract):** For multi-tenant query/analytics platforms, test whether tenant boundaries apply to metadata and query text (INSERT/WHERE values), not only result sets—cross-customer isolation bugs often hide in secondary surfaces. Extract note: LLM-assisted discovery; writeup at act.security. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** AWS, Athena, multi-tenant, data-exfiltration, cloud
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://x.com/orenyomtov/status/2097366728321749080](https://x.com/orenyomtov/status/2097366728321749080)
- **Notes:** LLM-assisted discovery; writeup at act.security.

---

### P.9 @Hac10101 — Azure / Entra recon and secret residue hunting

- **Root-cause class:** Azure / Entra recon and secret residue hunting
- **Affected component:** Azure / Entra ID tenant surfaces (blob, vault, AKS paths as named)
- **Impact:** Leaked credentials/secrets in readable sources when name-based detectors catch misnamed keys format-only tools miss.
- **Conditions called out:** Authorized Azure assessment scope
- **What the write-up/tweet teaches (abstract):** Approach Azure holistically: unauthenticated blob/version residue checks, external Entra/tenant recon, then conditional-access/role/grant enum and vault/app/AKS loot paths—old storage versions often retain secrets. Extract note: Promotes azpt toolkit (github.com/hac01/azure-pentesting-suite). Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** Azure, Entra, blob, Key-Vault, BloodHound, azpt
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://x.com/Hac10101/status/2097134370775818604](https://x.com/Hac10101/status/2097134370775818604)
- **Notes:** Promotes azpt toolkit (github.com/hac01/azure-pentesting-suite).

---

### P.10 @UK_Daniel_Card — Mobile-driven pentest workflow (ops)

- **Root-cause class:** Mobile-driven pentest workflow (ops)
- **Affected component:** Remote pentest session continuity (ops)
- **Impact:** Process/coverage improvement for authorized hunting; educational or platform meta rather than a single vuln impact.
- **Conditions called out:** Remote testing setup reachable from phone
- **What the write-up/tweet teaches (abstract):** Treat mobile-first remote testing as an ops pattern (session continuity, lightweight tooling) rather than a vuln class—useful for sustained triage while away from desk. Extract note: Low technical depth; mainly lifestyle/ops image post. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** ops, mobile, pentesting-workflow
- **Lane:** Researchy
- **Quality:** thin
- **Sources:**
- [https://x.com/UK_Daniel_Card/status/2096709936449212502](https://x.com/UK_Daniel_Card/status/2096709936449212502)
- **Notes:** Low technical depth; mainly lifestyle/ops image post.

---

### P.11 @0x0SojalSec — Local cyber-offense LLM for vuln discovery (tooling)

- **Root-cause class:** Local cyber-offense LLM for vuln discovery (tooling)
- **Affected component:** Public offensive-AI agent benchmark platforms
- **Impact:** Methodology / tooling impact: lower false positives, better token use, and stronger validation gates — not a single product CVE.
- **Conditions called out:** Hardware for large MoE; authorized use only
- **What the write-up/tweet teaches (abstract):** Local security-tuned models can assist recon/hypotheses, but findings still need human verification and must stay within authorized scope—benchmarks ≠ production validity. Extract note: GLM-5.3 cybersecurity model promo; dual-use caution. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** LLM, local-models, CyberGym, tooling
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://x.com/0x0SojalSec/status/2096639626706649149](https://x.com/0x0SojalSec/status/2096639626706649149)
- **Notes:** GLM-5.3 cybersecurity model promo; dual-use caution.

---

### P.12 @7h3h4ckv157 — Agentic coding CLI routing (tooling economics)

- **Root-cause class:** Agentic coding CLI routing (tooling economics)
- **Affected component:** Local security-tuned LLM tooling
- **Impact:** Technical agent success can still be negative economic ROI when token/cost burn exceeds bounty.
- **Conditions called out:** Desire to run Claude Code against alternate model backends
- **What the write-up/tweet teaches (abstract):** Proxy agentic coding CLIs to free/local model backends to lower iteration cost for research tooling—orthogonal to vuln classes but affects hunt throughput. Extract note: free-claude-code proxy; not a vulnerability pattern. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** Claude-Code, proxy, OpenRouter, local-LLM, tooling
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
- [https://x.com/7h3h4ckv157/status/2096488638456717430](https://x.com/7h3h4ckv157/status/2096488638456717430)
- **Notes:** free-claude-code proxy; not a vulnerability pattern.
