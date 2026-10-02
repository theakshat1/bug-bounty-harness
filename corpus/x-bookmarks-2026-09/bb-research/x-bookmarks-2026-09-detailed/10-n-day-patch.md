# N-day / Patch-diff / Kernel & enterprise patterns

**Cluster file:** `10-n-day-patch.md`  
**Audience:** Akshat (authorized / in-scope hunting only)  
**Constraint:** Abstract methodology only — **no** reproduction steps, payloads, PoCs, exploit recipes, Intruder setups, or attack procedures.  
**Items in this cluster:** 3

---

### 10.1 AI accelerates known kernel pattern classes (RCU/UAF)

- **Root-cause class:** Kernel `net/sched` use-after-free from **lock mismatch**: lookup under RCU vs free without RCU grace period (“raw free with RCU access”); race windows widened by error-path structure and contending locks; similar pattern class also seen around perf/events.
- **Affected component:** Linux kernel networking traffic-control (`clsact`/`flower` unlocked paths); related subsystems searchable by the same RCU/free mismatch pattern; local LPE-research lab context.
- **Impact:** Kernel UAF / LPE-research class (CVE-2026-53264 tagged in extract); AI accelerates finding siblings of known pattern classes so fresh bugs behave like accelerated n-days.
- **Conditions called out:** Unprivileged user namespaces; CONFIG with clsact/flower unlocked paths; local kernel research lab (**authorized**).
- **What the source teaches (abstract):** AI accelerates discovery of known pattern classes (RCU/UAF lock mismatches) — treat fresh bugs like accelerated n-days. Hunt code that looks up under RCU but frees without grace period. Race reliability comes from window-widening + restructuring to cheaper error paths + isolation of contending locks (analysis of *why* races become reliable — not reproduction steps). Still need deep subsystem judgment for AI blind spots. Pattern search (“raw free with rcu access”) can yield sibling bugs in other subsystems.
- **Tags:** kernel, net/sched, UAF, race, AI-assisted, LPE-research, CVE-2026-53264
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://starlabs.sg/blog/2026/07-when-ai-makes-0-days-feel-like-n-days/
- **Notes:** [Researcher:11] ok

---

### 10.2 Protocol state-machine rollback UAF family (SCTP)

- **Root-cause class:** Kernel SCTP protocol state-machine flaw: use-after-free arising from stale COOKIE-ECHO rollback that frees stream/session state without invalidating a cached stream-scheduler pointer (and related queue caches). Classic “rollback frees tables but leaves dangling caches.”
- **Affected component:** Linux kernel SCTP association / stream scheduler path; Ubuntu 7.0.0-28–class kernels historically named in the folder.
- **Impact:** Kernel UAF in SCTP path (LPE-research class per extract tags); severity/details limited to advisory-level synopsis in extract — not expanded here.
- **Conditions called out:** Unpatched kernel with SCTP; ability to drive SCTP association state (Stale Cookie ERROR rollback path); Ubuntu 7.0.0-28 class kernels historically listed in folder name.
- **What the source teaches (abstract):** Protocol state-machine rollbacks often free tables without invalidating cached pointers or purging queues. Hunt for “rollback/restart” paths that free/rebuild stream or session state but leave scheduler/outqueue caches dangling. Cross-check n-day kernel advisories against still-live distro versions in scope. **Do not reuse public exploit trees in unauthorized environments.**
- **Tags:** kernel, SCTP, UAF, LPE-research, CVE-2026-52924
- **Lane:** Researcher
- **Quality:** thin (GitHub folder no README; synopsis from Ubuntu/OpenCVE only; exploit sources not used)
- **Sources:**
  - https://github.com/NebuSec/CyberMeowfia/tree/main/security-research/Linux-CVE-2026-52924-ubuntu-7.0.0-28/
- **Notes:** [Researcher:04] thin — GitHub tree has Makefile/C sources but no README (404). CVE synopsis from Ubuntu/OpenCVE advisories only; **exploit source was not reviewed or summarized as PoC.** Gap: no author narrative, no defensive write-up in-tree. | Thin because in-tree documentation is missing; this entry stays at advisory + pattern level only.

---

### 10.3 AEM n-day triage: authZ + stored XSS by version fingerprint

- **Root-cause class:** AEM privilege escalation; security-feature bypass; stored XSS / incorrect authorization (CWE-863) / improper input validation — multi-CVE Priority 2 bulletin (design/authorization and input-validation failures across AEM surfaces).
- **Affected component:** Adobe Experience Manager — Cloud Service, 6.5 LTS, and 6.5 classic lines as versioned in the bulletin.
- **Impact:** Multi-CVE bulletin (Priority 2); NotCVE lists e.g. Incorrect Authorization at CVSS 9.9 among 107 CVEs — high authorization and XSS risk on outdated AEM.
- **Conditions called out:** AEM Cloud Service ≤2026.7.0, 6.5 LTS ≤SP2, or 6.5 ≤SP24 in scope (per extract). Upgrade path noted: CS 2026.8.0 / 6.5 LTS SP3 / 6.5 SP25.
- **What the source teaches (abstract):** On AEM targets, prioritize authZ flaws (CWE-863) and stored XSS in form fields reachable by low-priv users; map bulletin CVEs to version fingerprints. When primary vendor pages block scrapers, use CERT mirrors + CVE aggregators for scope triage. — Version triage only; no exploit procedures.
- **Tags:** AEM, Adobe, XSS, priv-esc, n-day, APSB26-98
- **Lane:** Researcher
- **Quality:** blocked-recovered (helpx EdgeSuite 403; recovered via HKCERT/NotCVE)
- **Sources:**
  - https://helpx.adobe.com/security/products/experience-manager/apsb26-98.html
- **Notes:** [Researcher:08] blocked — helpx returned EdgeSuite Access Denied. Ideas recovered via HKCERT/NotCVE/search already cited in extract; vendor HTML body not scraped.

