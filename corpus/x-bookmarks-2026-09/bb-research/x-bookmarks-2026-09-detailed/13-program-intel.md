# Program intel / Prioritization / Ops

**Cluster file:** `13-program-intel.md`  
**Audience:** Akshat (authorized / in-scope hunting only)  
**Constraint:** Abstract methodology only — **no** reproduction steps, payloads, PoCs, exploit recipes, Intruder setups, or attack procedures.  
**Items in this cluster:** 3

---

### 13.1 Prioritize by public H1 activity / payout signals

- **Root-cause class:** Program intel / hunting prioritization
- **Affected component:** Bug-bounty program policy / scope (operator-side historical)
- **Impact:** Better hunt ROI via program activity, payout tables, and newly unified scopes (ops/planning impact, not a vuln).
- **Conditions called out:** Access to public HackerOne program metadata / community dashboards
- **What the source teaches (abstract):** Use public-program activity and payout distribution signals to prioritize where researchers are currently succeeding, rather than hunting only by personal preference. Extract note: Teases public H1 program stats; points to forthcoming BugBountyHunter site. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** hackerone, program-intel, prioritization, bugbountyhunter
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://x.com/zseano/status/2105766060398162315
- **Notes:** [Researchy:P.1] Teases public H1 program stats; points to forthcoming BugBountyHunter site.

---

### 13.2 Historical program-policy signal (payout tables, unified scopes)

- **Root-cause class:** Bug-bounty program design / scope & payout policy (operator-side lessons for hunters)
- **Affected component:** Bug-bounty program policy / scope (operator-side historical)
- **Impact:** Better hunt ROI via program activity, payout tables, and newly unified scopes (ops/planning impact, not a vuln).
- **Conditions called out:** N/A for hunters beyond being invited to the (then) private Oath program covering Tumblr/Yahoo/AOL/EdgeCast brands
- **What the source teaches (abstract):** From a researcher planning angle: programs that publish payout tables, expand in-scope vuln types by CVSS/impact, shorten triage SLAs, and unify previously private brand scopes reward steady engagement over moonshot-only hunting. Prioritize classes programs explicitly top-rank (here: SQLi, RCE, XXE/XMLi) while watching for newly opened assets when private sub-programs merge into a unified program. Historical signal that live-hacking events + continuous private programs compound attack-surface reduction. Extract note: Aug 23, 2018 post by Katrina Dene / Chris Nims; historical program ops lessons, not a vuln writeup. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** hackerone, program-policy, oath, payouts, scope, historical
- **Lane:** Researchy
- **Quality:** ok (2018 historical)
- **Sources:**
  - https://hackerone.com/blog/oath-bug-bounty-program-update-1m-payouts-and-expansion-program
  - https://x.com/i/web/status/2100981796192338406
- **Notes:** [Researchy:A.8] Aug 23, 2018 post by Katrina Dene / Chris Nims; historical program ops lessons, not a vuln writeup.

---

### 13.3 Mobile-first remote session continuity (ops)

- **Root-cause class:** Mobile-driven pentest workflow (ops)
- **Affected component:** Remote pentest session continuity (ops)
- **Impact:** Process/coverage improvement for authorized hunting; educational or platform meta rather than a single vuln impact.
- **Conditions called out:** Remote testing setup reachable from phone
- **What the source teaches (abstract):** Treat mobile-first remote testing as an ops pattern (session continuity, lightweight tooling) rather than a vuln class—useful for sustained triage while away from desk. Extract note: Low technical depth; mainly lifestyle/ops image post. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** ops, mobile, pentesting-workflow
- **Lane:** Researchy
- **Quality:** thin
- **Sources:**
  - https://x.com/UK_Daniel_Card/status/2096709936449212502
- **Notes:** [Researchy:P.10] Low technical depth; mainly lifestyle/ops image post.

