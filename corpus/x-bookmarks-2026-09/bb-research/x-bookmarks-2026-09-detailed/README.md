# X Bookmarks Bug-Bounty Knowledge Base (detailed) — 2026-09 window

**Audience:** Akshat (authorized / in-scope hunting only)  
**Purpose:** Multi-doc methodology KB merged from three exclusive NON-REPRO deepened lanes.  
**Generated:** 2026-10-02 (Asia/Calcutta)

## Hard constraints (must obey)

- **Allowed:** title, source URLs, root-cause class, affected component (as stated), impact (as stated), conditions from sources, generalized abstract teaching, tags, lane provenance, quality (`ok` / `thin` / `blocked`), honest notes.
- **Forbidden everywhere:** step-by-step reproduction, payloads, exploit commands, PoC code, bypass recipes, Intruder setups, weaponized strings, “how to hit new surfaces” attack playbooks, reconstructed exploit detail.
- Thin / blocked extracts stay honest — **do not fabricate**.

## Index

| Doc | Role |
|-----|------|
| [`00-overview.md`](./00-overview.md) | Stats, high-diversity patterns, cluster map |
| [`01-idor-bola.md`](./01-idor-bola.md) | IDOR / BOLA / authorization mismatches |
| [`02-js-secrets.md`](./02-js-secrets.md) | JS / sourcemap recon & client secrets |
| [`03-cloud-multi-tenant.md`](./03-cloud-multi-tenant.md) | Cloud / multi-tenant / storage misconfig |
| [`04-llm-hunting-process.md`](./04-llm-hunting-process.md) | LLM & agent hunting process |
| [`05-mcp-tooling.md`](./05-mcp-tooling.md) | MCP / agent tooling meta |
| [`06-path-filter.md`](./06-path-filter.md) | Path normalization / password-reset / filter mismatches |
| [`07-xss-encoding.md`](./07-xss-encoding.md) | XSS / encoding / WAF filter catalogs |
| [`08-ssrf-headers.md`](./08-ssrf-headers.md) | SSRF / header trust / 403 bypass |
| [`09-recon-workflows.md`](./09-recon-workflows.md) | Classic recon → hunt workflows |
| [`10-n-day-patch.md`](./10-n-day-patch.md) | N-day / patch-diff / kernel & enterprise patterns |
| [`11-web3.md`](./11-web3.md) | Web3 audit corpora |
| [`12-disclosure-hygiene.md`](./12-disclosure-hygiene.md) | PoC hygiene & responsible disclosure |
| [`13-program-intel.md`](./13-program-intel.md) | Program intel / prioritization / ops |
| [`14-thin-tangential.md`](./14-thin-tangential.md) | Thin / outcome-only / tangential |
| [`SOURCES.md`](./SOURCES.md) | Every unique source URL (title, lane, quality) |
| [`BY-LANE.md`](./BY-LANE.md) | Rollup pointing at the three lane folders |

## Lane pointers (exclusive SoTs — kept as-is)

| Lane | Items | Absolute path |
|------|------:|---------------|
| Researchy | 24 | `/workspace/bb-research/x-bookmarks-2026-09-detailed/lanes/researchy/` |
| Researcher | 23 | `/workspace/bb-research/x-bookmarks-2026-09/researcher-deep/` |
| Deep Research | 22 | `/workspace/bb-research/x-bookmarks-2026-09/deep-research-deep/` |

Local Researchy mirror: [`lanes/researchy/`](./lanes/researchy/) (do not overwrite lane contents in this merge).

## Stats (quick)

| Metric | Count |
|--------|------:|
| Source items (3 lanes) | **69** |
| Unique ideas after dedupe | **68** |
| Clusters | **14** |
| Thin | **6** |
| Blocked-recovered | **2** |
| Explicit merges | **1** (Adverserial/CyberKimi → `4.16`) |

### Counts per cluster

| Cluster file | Items |
|--------------|------:|
| `01-idor-bola.md` | **7** |
| `02-js-secrets.md` | **2** |
| `03-cloud-multi-tenant.md` | **3** |
| `04-llm-hunting-process.md` | **23** |
| `05-mcp-tooling.md` | **7** |
| `06-path-filter.md` | **3** |
| `07-xss-encoding.md` | **2** |
| `08-ssrf-headers.md` | **3** |
| `09-recon-workflows.md` | **6** |
| `10-n-day-patch.md` | **3** |
| `11-web3.md` | **1** |
| `12-disclosure-hygiene.md` | **1** |
| `13-program-intel.md` | **3** |
| `14-thin-tangential.md` | **4** |

### Thin / blocked totals

- **Thin IDs:** 9.4, 10.2, 13.3, 14.1, 14.2, 14.3
- **Blocked-recovered IDs:** 4.6, 10.3
- **Blocked unrecovered:** 0

## Per-item template (cluster docs)

```
### {id} Title
- **Root-cause class:**
- **Affected component:**
- **Impact:**
- **Conditions called out:**
- **What the source teaches (abstract):**
- **Tags:**
- **Lane:**
- **Quality:**
- **Sources:**
- **Notes:**
```

## Absolute output root

`/workspace/bb-research/x-bookmarks-2026-09-detailed/`
