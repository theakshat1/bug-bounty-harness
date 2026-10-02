# 00 — Overview (merged multi-doc KB)

**Audience:** Akshat (authorized / in-scope hunting only)  
**Generated:** 2026-10-02 (Asia/Calcutta)  
**Constraint:** Methodology / abstract hunting ideas only — **no** reproduction steps, payloads, PoCs, exploit recipes, Intruder setups, weaponized strings, or attack procedures.

## Stats

| Metric | Count |
|--------|------:|
| Total source items ingested (3 lanes) | **69** |
| Unique hunting ideas after dedupe | **68** |
| Explicit merges | **1** (Adverserial / CyberKimi) |
| Clusters | **14** |
| Thin (preserved honesty) | **6** (9.4, 10.2, 13.3, 14.1, 14.2, 14.3) |
| Blocked-recovered | **2** (4.6, 10.3) |
| Blocked unrecovered | **0** |
| Researchy items | **24** |
| Researcher items | **23** |
| Deep Research items | **22** |

## High-diversity reusable patterns

- **Validate before report.** Treat LLM or scanner hypotheses as untrusted until a separate oracle, second agent, or live impact check proves them (PageBreak, Cloudflare audit skill, Crusader, StrikeAgent, Jenny hallucination→promote, Xalgorix detect-then-prove, OpenAI Defense Factory, Claude-BugHunter 7-Question Gate).
- **UI allowlist ≠ server allowlist.** Diff what the UI exposes vs what APIs enumerate (hidden role UUIDs, JWT claims, signature sibling endpoints, dead `/api|/admin` routes in JS).
- **JS / sourcemap recon as surface map.** Harvest bundles and source maps for hidden domains, full route maps, Cognito/AWS client config, and object IDs that pivot into IDOR/BOLA.
- **Authz at every entrypoint.** Internal library wrappers, filter-vs-dispatcher path normalization, and caller trust boundaries often miss one path.
- **Regression is first-class.** Retest shipped fixes, sibling backends, and the same bug class after vendor patches (Quarry, Google Cloud multi-backend lessons, Papercut-style n-day sweeps).
- **Under-tested utility surfaces.** Prefer export/PDF, email digests, file previews, debug/test endpoints, and header-driven SSRF over crowded login pages.
- **Multi-tenant isolation beyond results.** Query text, metadata, blob versions, and shared analytics often leak across tenants when only result sets are gated.
- **Filter mismatch catalogs, not payload spam.** Organize XSS/SSRF/path tests by mismatch class (encoding depth, strip order, truncation, entity/scheme variants, header namespace).
- **Orchestration > model choice.** Scoped stages, coverage ledgers, adversarial disprove verifiers, call-graph context compression, and token budgets beat dumping whole repos into prompts.
- **Program intel + ROI.** Prioritize by public payout/activity signals; track token burn vs bounty outcome; feed negatives into RAG so campaigns skip hardened dead-ends.
- **PoC hygiene for takeovers.** Minimal public proof surface; evidence in private report; platform handle to deter claim-theft.
- **Codify past wins into skills.** Turn personal IDOR/authz lessons into reusable agent skills pointed at live JS/API surfaces.


## Cluster map

| # | File | Theme | Items |
|---|------|-------|------:|
| 01 | [`01-idor-bola.md`](./01-idor-bola.md) | IDOR / BOLA / Authorization mismatches | **7** |
| 02 | [`02-js-secrets.md`](./02-js-secrets.md) | JS / Sourcemap recon & client secrets | **2** |
| 03 | [`03-cloud-multi-tenant.md`](./03-cloud-multi-tenant.md) | Cloud / Multi-tenant / Storage misconfig | **3** |
| 04 | [`04-llm-hunting-process.md`](./04-llm-hunting-process.md) | LLM & agent hunting process | **23** |
| 05 | [`05-mcp-tooling.md`](./05-mcp-tooling.md) | MCP / Agent tooling meta | **7** |
| 06 | [`06-path-filter.md`](./06-path-filter.md) | Path normalization / Password-reset / Filter mismatches | **3** |
| 07 | [`07-xss-encoding.md`](./07-xss-encoding.md) | XSS / Encoding / WAF filter catalogs | **2** |
| 08 | [`08-ssrf-headers.md`](./08-ssrf-headers.md) | SSRF / Header trust / 403 bypass | **3** |
| 09 | [`09-recon-workflows.md`](./09-recon-workflows.md) | Classic recon → hunt workflows | **6** |
| 10 | [`10-n-day-patch.md`](./10-n-day-patch.md) | N-day / Patch-diff / Kernel & enterprise patterns | **3** |
| 11 | [`11-web3.md`](./11-web3.md) | Web3 audit corpora | **1** |
| 12 | [`12-disclosure-hygiene.md`](./12-disclosure-hygiene.md) | PoC hygiene & responsible disclosure | **1** |
| 13 | [`13-program-intel.md`](./13-program-intel.md) | Program intel / Prioritization / Ops | **3** |
| 14 | [`14-thin-tangential.md`](./14-thin-tangential.md) | Thin / Outcome-only / Tangential | **4** |

## Dedupe / honesty notes

- **Merged:** Adverserial / CyberKimi product docs (`adverserial.ai` + `adverserial.ai/docs.html`) into idea `4.16`; both lanes cited.
- **Related but kept separate:** JS graveyard (`1.2`), MTN sourcemap→IDOR (`1.3`), and report-trained IDOR skill (`1.4`); zsec harnessing-harnesses (`4.1`) vs bullyingllms (`4.2`); two `@adnanthekhan` posts (`4.13` vs `4.14`).
- **Anecdotal / unverified:** Agent-swarm SSRF→RCE→K8s claim (`4.14`); fully-agentized workflow (`4.21`) marked culture signal.
- **Blocked-recovered:** PageBreak findings (`4.6`) and AEM APSB26-98 (`10.3`) — primary URLs gated/403; content limited to alternate summaries already in Researcher extract.
- **Thin preserved:** SCTP folder (`10.2`), BugBountyHunting FAQ (`9.4`), mobile ops (`13.3`), crypto/WAF title-only (`14.1`), RCE outcome-only (`14.2`), DeerFlow (`14.3`). Cadence (`14.4`) kept as tangential tooling (ok/tangential).
- **No invented findings.** Built only from the three exclusive lane SoTs + prior cluster structure hints.

## How to use

1. Skim this overview for patterns and the cluster map.
2. Open a cluster file for per-idea methodology cards.
3. Trace provenance via [`BY-LANE.md`](./BY-LANE.md) and [`SOURCES.md`](./SOURCES.md).
4. For full lane-native wording, open the absolute paths in BY-LANE.
