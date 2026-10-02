# SSRF / Header trust / 403 bypass

**Cluster file:** `08-ssrf-headers.md`  
**Audience:** Akshat (authorized / in-scope hunting only)  
**Constraint:** Abstract methodology only — **no** reproduction steps, payloads, PoCs, exploit recipes, Intruder setups, or attack procedures.  
**Items in this cluster:** 3

---

### 8.1 Blind SSRF via systematic header namespace + OOB

- **Root-cause class:** Applications honor unexpected or custom HTTP headers that influence outbound fetch/resolve behavior without adequate allowlisting — blind SSRF via **header trust surface**, not only classic `X-Forwarded-*` guesses.
- **Affected component:** HTTP request header handling that can trigger server-side requests; OOB collaborator / callback monitoring.
- **Impact:** Blind SSRF discovery when header-influenced outbound requests hit OOB listeners (class-level).
- **Conditions called out:** Burp Intruder/Collaborator (or similar OOB); request that may honor custom headers. — Tools named as environmental facts only.
- **What the source teaches (abstract):** Bruteforce header names with OOB callback values; pitchfork numerical prefixes; monitor hits with a collaborator aggregator. Systematic header surface for SSRF often beats guessing `X-Forwarded-*` alone. — **Methodology language only; no Intruder payloads, wordlists, or attack scripts reproduced.**
- **Tags:** SSRF, blind-SSRF, Burp, OOB, headers
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://x.com/ethical_h4ck3r_/status/2098744915001786871
- **Notes:** [Researcher:17] ok

---

### 8.2 403 paths that trust spoofable forwarding / IP headers

- **Root-cause class:** Access-control bypass via trusted client IP headers
- **Affected component:** Paths returning 403 where app/WAF may trust forwarding headers
- **Impact:** Access-control decisions that trust spoofable identity/forwarding headers may incorrectly allow restricted paths.
- **Conditions called out:** Target returns 403 on sensitive paths; app or WAF may trust forwarding headers
- **What the source teaches (abstract):** On 403 responses, systematically challenge whether access decisions trust spoofable client-IP / forwarding headers (and similar identity headers) instead of true network identity. Extract note: Tip only; not always applicable—treat as header-trust differential test. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** 403-bypass, header-injection, IP-spoofing, access-control
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://x.com/ethical_h4ck3r_/status/2099352309834588200
- **Notes:** [Researchy:P.4] Tip only; not always applicable—treat as header-trust differential test.

---

### 8.3 Under-tested features: export/PDF, digests, previews

- **Root-cause class:** Coverage bias — programs over-test auth entrypoints while utility features (export/PDF, digests, previews) retain classic SSRF/SSTI/IDOR/path issues due to low tester attention.
- **Affected component:** Export/PDF generation; email digests; file preview / filename handling; other low-attention authenticated utilities.
- **Impact:** Findings concentration on under-tested utilities rather than crowded login flows (methodology claim).
- **Conditions called out:** Crowded BB program; authenticated feature access.
- **What the source teaches (abstract):** Prefer features with few testers: Export/PDF → SSRF/SSTI; email digests → IDOR on recipient IDs; file previews → path traversal via filenames. Crowding on auth ≠ coverage of utilities. — Class mapping only; no how-to.
- **Tags:** methodology, SSRF, SSTI, IDOR, path-traversal
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://x.com/aacle_/status/2105641477187817799
- **Notes:** [Researcher:12] ok

