# XSS / Encoding / WAF filter catalogs

**Cluster file:** `07-xss-encoding.md`  
**Audience:** Akshat (authorized / in-scope hunting only)  
**Constraint:** Abstract methodology only — **no** reproduction steps, payloads, PoCs, exploit recipes, Intruder setups, or attack procedures.  
**Items in this cluster:** 2

---

### 7.1 Encoding-variant catalogs for scheme/URL sinks

- **Root-cause class:** Naive blacklist filters that ban literal scheme strings (e.g. `javascript:`) but still accept alternate encodings the browser interprets — **filter/parser mismatch**, not a novel XSS sink class.
- **Affected component:** Reflection into URL/JS contexts protected by naive blacklist filters.
- **Impact:** Filter evasion enabling XSS where literal-string bans were assumed sufficient (class-level; no payload gallery reproduced).
- **Conditions called out:** Reflection into URL/JS contexts with naive blacklist filters.
- **What the source teaches (abstract):** When filters ban `javascript:` literally, test alternate encodings (entities, mixed case, whitespace) that the browser still interprets. Maintain encoding-variant wordlists for URL/scheme sinks — **do not paste live payloads into unauthorized targets.** Prefer mismatch-class catalogs over payload spam. **No wordlist contents or weaponized strings included here.**
- **Tags:** XSS, filter-bypass, wordlist, encoding
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://x.com/ethical_h4ck3r_/status/2099347683987046887
- **Notes:** [Researcher:15] ok

---

### 7.2 XSS regex/WAF mismatch family catalog

- **Root-cause class:** Regex-based WAF/filter **parser mismatch** — filters miss alternate event handlers, `data:` documents, unicode escapes in identifiers, and malformed tags the browser still accepts.
- **Affected component:** HTML sinks guarded by regex-based filters/WAFs.
- **Impact:** XSS where regex filters were assumed sufficient (class-level). **No payload gallery or weaponized strings reproduced.**
- **Conditions called out:** HTML sink with regex-based filter/WAF.
- **What the source teaches (abstract):** Maintain a catalog of parser/WAF mismatch classes (event-handler variety, `data:` documents, unicode in identifiers, malformed tags the browser still accepts). Test methodology: classify filter type → pick mismatch family — **without dumping live weaponized strings into out-of-scope apps.**
- **Tags:** XSS, WAF-bypass, regex, filter-mismatch
- **Lane:** Researcher
- **Quality:** ok
- **Sources:**
  - https://x.com/n0aziXss/status/2096524472601768217
- **Notes:** [Researcher:22] ok

