# Classic recon → hunt workflows

**Cluster file:** `09-recon-workflows.md`  
**Audience:** Akshat (authorized / in-scope hunting only)  
**Constraint:** Abstract methodology only — **no** reproduction steps, payloads, PoCs, exploit recipes, Intruder setups, or attack procedures.  
**Items in this cluster:** 6

---

### 9.1 Fixed pipeline: multi-source enum → param buckets → business logic → secrets → report

- **Root-cause class:** Repeatable BB workflow: recon → vuln hunt → business logic/API → secrets → reporting
- **Affected component:** Cloud object storage (S3-class) + app download/API path
- **Impact:** Leaked credentials/secrets in readable sources when name-based detectors catch misnamed keys format-only tools miss.
- **Conditions called out:** Authorized target; ProjectDiscovery suite + common recon tools installed; do not skip recon before exploitation
- **What the source teaches (abstract):** Execute a fixed pipeline every time: (1) multi-source subdomain enum (tool diversity + CT logs) → live host/tech-detect filter → deep URL collection (active crawl + historical indexes), (2) parameter extraction and pattern buckets (XSS/SQLi/SSRF/redirect/RCE-SSTI candidates) via templates and focused scanners—not random poking, (3) manual business-logic/API work (JWT/cookie trust, IDOR/UUID predictability, GraphQL introspection exposure), (4) secrets in JS bundles and leaked env/git artefacts, (5) evidence-first reporting. Core meta-rule: attack-surface size decides success odds; automation ends where business logic begins. Extracted as process patterns only—omit weaponized payload recipes. Extract note: WebFetch hit Cloudflare 403; recovered via curl (HTTP 200). Published ~2026-02-26 on InfoSec Write-ups. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** workflow, recon, projectdiscovery, idor, graphql, secrets, beginner, methodology
- **Lane:** Researchy
- **Quality:** ok (WebFetch Cloudflare 403 → recovered via curl)
- **Sources:**
  - https://infosecwriteups.com/my-complete-bug-bounty-hunting-workflow-every-command-i-use-step-by-step-68484276471f
  - https://x.com/i/web/status/2098351354309722129
- **Notes:** [Researchy:A.9] WebFetch hit Cloudflare 403; recovered via curl (HTTP 200). Published ~2026-02-26 on InfoSec Write-ups.

---

### 9.2 Methodology-as-product (Ars0n): UI-gated stages + unified DB

- **Root-cause class:** End-to-end bug-bounty workflow automation / attack-surface mapping platform
- **Affected component:** Azure / Entra ID tenant surfaces (blob, vault, AKS paths as named)
- **Impact:** Process/coverage improvement for authorized hunting; educational or platform meta rather than a single vuln impact.
- **Conditions called out:** Docker Compose host; optional API keys for OSINT providers (SecurityTrails, Censys, Shodan, Whoxy, etc.); authorized targets only
- **What the source teaches (abstract):** Force a correct hunting order via UI-gated stages wrapping 50+ common tools (Amass, Subfinder, httpx, Katana, Nuclei, ffuf, GAU, cloud_enum, Naabu, GitHub recon, etc.), store results in a central DB for attack-surface visualization, and pair each stage with ‘Help Me Learn!’ lessons so beginners absorb the *why*. Pattern: methodology-as-product—make skipping recon hard; unify tool output; add MCP/AI assistant hooks for triage. Compete with pros by breadth of passive+active asset discovery and consistent process, not by skipping steps. Extract note: README via raw.githubusercontent.com; beta 0.1.0; ‘Earn While You Learn’ framing. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** framework, bug-bounty, recon, docker, beginner, mcp, attack-surface, rs0n
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://github.com/R-s0n/ars0n-framework-v2
  - https://x.com/i/web/status/2097322316120437210
- **Notes:** [Researchy:A.5] README via raw.githubusercontent.com; beta 0.1.0; ‘Earn While You Learn’ framing.

---

### 9.3 Subdomain inventory + CVE/KEV + takeover signals early

- **Root-cause class:** Incomplete attack-surface inventory and weak correlation between discovered hosts/products and known vulnerable (CVE/KEV) or takeover-prone DNS states — a visibility/prioritization gap rather than a single application bug.
- **Affected component:** Public DNS and subdomain estate; dangling DNS / takeover-prone records; product fingerprinting correlated to CVE/KEV intel (ASM-style).
- **Impact:** Missed or late discovery of exposed hosts, takeover candidates, and unpatched critically scored products before deeper application testing.
- **Conditions called out:** Target organization with public DNS/subdomains; optional paid features for auto-resolve and takeover checks (as noted by the platform).
- **What the source teaches (abstract):** Map full subdomain inventory early; cross-reference discovered hosts/products against CVE/KEV feeds; prioritize takeover-prone dangling DNS and unpatched critically scored products before deep app testing.
- **Tags:** recon, subdomain, takeover, CVE-intel, ASM
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://SubMap.net
- **Notes:** [Researcher:01] ok

---

### 9.4 Classic class taxonomy checklist (input→sink)

- **Root-cause class:** Educational FAQ covering XSS, IDOR, SSRF, SQLi, RCE classes
- **Affected component:** General web apps (educational taxonomy)
- **Impact:** Process/coverage improvement for authorized hunting; educational or platform meta rather than a single vuln impact.
- **Conditions called out:** Beginner / general web app hunting context; understanding input→output and access-control surfaces
- **What the source teaches (abstract):** Prioritize classic web classes by how user input reaches sinks: unencoded reflection (XSS variants stored/reflected/DOM), direct object identifiers without authz (IDOR), server-side URL fetchers (SSRF incl. cloud metadata), query construction from input (SQLi), and eval/command construction from strings/files (RCE). Treat FAQ-style class definitions as a checklist when mapping each endpoint’s trust boundaries. Extract note: Community-curated search/FAQ site; thin on novel research but useful class taxonomy for hunters. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** education, xss, idor, ssrf, sqli, rce, beginner, faq
- **Lane:** Researchy
- **Quality:** thin
- **Sources:**
  - https://BugBountyHunting.com
  - https://x.com/i/web/status/2098301017989558495
- **Notes:** [Researchy:A.1] Community-curated search/FAQ site; thin on novel research but useful class taxonomy for hunters.

---

### 9.5 Android: bulk APK ingest → exported activities → AI on ranked targets

- **Root-cause class:** Manual APK triage wastes effort on low-interest components; exported activities and related surfaces benefit from map-and-rank before deep analysis.
- **Affected component:** Android APK/XAPK/ZIP ingest; decompile; exported activities; ADB launch of ranked components; AI applied only after ranking.
- **Impact:** Faster mobile surface triage analogous to web “map & rank then hunt.”
- **Conditions called out:** APK/XAPK/ZIP inputs; decompiler; ADB for exported components.
- **What the source teaches (abstract):** Automate triage: extract main APK, enumerate exported activities, generate ADB launch commands, then apply AI only to ranked interesting components — mirrors web “map & rank then hunt.” — Workflow shape only; no exploit recipes for exported components.
- **Tags:** Android, APK, exported-activities, mobile, AI-assist
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://x.com/dirtycoder0124/status/2097280683924467834
- **Notes:** [Researcher:19] ok

---

### 9.6 AD baseline automation: communicate chainable risks, not DA-or-bust

- **Root-cause class:** “DA-or-bust” success metrics miss chainable risks (exposed data, weak configs); repetitive AD checks without automation slow communication of real risk.
- **Affected component:** Authorized Active Directory engagements; baseline automation (ADScan / ADPulse as named tools).
- **Impact:** Faster AD baseline and better risk communication beyond Domain Admin as sole success criterion. Useful contrast to Claude-BugHunter’s deliberate external-only scope.
- **Conditions called out:** Authorized AD engagement.
- **What the source teaches (abstract):** Automate repetitive AD checks; success = identifying/communicating chainable risks (exposed data, weak configs), not only Domain Admin. Useful contrast to Claude-BugHunter’s deliberate external-only scope.
- **Tags:** Active-Directory, automation, pentest-methodology
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://x.com/three_cube/status/2096695889259851867
- **Notes:** [Researcher:21] ok

