# Cloud / Multi-tenant / Storage misconfig

**Cluster file:** `03-cloud-multi-tenant.md`  
**Audience:** Akshat (authorized / in-scope hunting only)  
**Constraint:** Abstract methodology only — **no** reproduction steps, payloads, PoCs, exploit recipes, Intruder setups, or attack procedures.  
**Items in this cluster:** 3

---

### 3.1 Google dork → S3 listing + unsigned object serve

- **Root-cause class:** Cloud storage misconfiguration / sensitive data exposure via public listing + unsigned object serving
- **Affected component:** Cloud object storage (S3-class) + app download/API path
- **Impact:** Sensitive data / export exposure via public listing combined with unsigned object serving (as stated in write-up; ~$2k bounty noted in extract).
- **Conditions called out:** In-scope web app using object storage; indexed public files revealing bucket naming; ability to probe listing/ACL without auth (authorized testing)
- **What the source teaches (abstract):** Start large scopes with lightweight Google dorks for indexed PDFs/uploads (`site:*.target TLD filetype` style) to surface CDN/S3 path patterns in URLs. When path segments look like bucket names, check whether listing is open and whether the app’s download/API path serves objects without time-limited signed URLs or auth. Chain: public listing (filename oracle) + unauthenticated content fetch = PII/export exposure even if direct object-store GET is partially restricted. Prefer signed URLs, least-privilege bucket policies, and separate sensitive exports from public assets. Extract note: Author Amrul / Seek404; ~$2k bounty; methodology only—no copy of exposed data or attack scripts. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** s3, misconfiguration, google-dork, sensitive-data, cloud, yeswehack, recon
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://medium.com/@Seek404/when-a-simple-google-dork-led-to-an-s3-misconfiguration-and-sensitive-data-exposure-4d7d86f54b16
  - https://x.com/i/web/status/2096270617205162368
- **Notes:** [Researchy:A.10] Author Amrul / Seek404; ~$2k bounty; methodology only—no copy of exposed data or attack scripts.

---

### 3.2 Multi-tenant query/analytics isolation (metadata & query text)

- **Root-cause class:** Cloud multi-tenant isolation failure (shared analytics/query services)
- **Affected component:** AWS Athena / multi-tenant query-analytics platforms
- **Impact:** Cross-tenant leakage of query text/metadata (not only result sets) on shared analytics platforms.
- **Conditions called out:** Authorized cloud research scope; interest in shared analytics/query services
- **What the source teaches (abstract):** For multi-tenant query/analytics platforms, test whether tenant boundaries apply to metadata and query text (INSERT/WHERE values), not only result sets—cross-customer isolation bugs often hide in secondary surfaces. Extract note: LLM-assisted discovery; writeup at act.security. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** AWS, Athena, multi-tenant, data-exfiltration, cloud
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://x.com/orenyomtov/status/2097366728321749080
- **Notes:** [Researchy:P.8] LLM-assisted discovery; writeup at act.security.

---

### 3.3 Azure / Entra residue & vault loot paths

- **Root-cause class:** Azure / Entra recon and secret residue hunting
- **Affected component:** Azure / Entra ID tenant surfaces (blob, vault, AKS paths as named)
- **Impact:** Leaked credentials/secrets in readable sources when name-based detectors catch misnamed keys format-only tools miss.
- **Conditions called out:** Authorized Azure assessment scope
- **What the source teaches (abstract):** Approach Azure holistically: unauthenticated blob/version residue checks, external Entra/tenant recon, then conditional-access/role/grant enum and vault/app/AKS loot paths—old storage versions often retain secrets. Extract note: Promotes azpt toolkit (github.com/hac01/azure-pentesting-suite). Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** Azure, Entra, blob, Key-Vault, BloodHound, azpt
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://x.com/Hac10101/status/2097134370775818604
- **Notes:** [Researchy:P.9] Promotes azpt toolkit (github.com/hac01/azure-pentesting-suite).

