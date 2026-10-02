# Path normalization / Password-reset / Filter mismatches

**Cluster file:** `06-path-filter.md`  
**Audience:** Akshat (authorized / in-scope hunting only)  
**Constraint:** Abstract methodology only — **no** reproduction steps, payloads, PoCs, exploit recipes, Intruder setups, or attack procedures.  
**Items in this cluster:** 3

---

### 6.1 Path traversal filter mistake classes

- **Root-cause class:** Path-traversal filter bypass via normalization mismatches (termination, strip-evasion, nested decoding, truncation)
- **Affected component:** Apps that accept user-controlled file/path parameters with naive blacklist/normalization
- **Impact:** Potential unauthorized file path access when filter and downstream consumer disagree on path meaning
- **Conditions called out:** App accepts user-controlled file/path parameters and applies naive blacklist/normalization; Downstream consumer may stop at NUL, re-decode, strip '../' once, or truncate long paths
- **What the source teaches (abstract):** X tip cataloging classes of path-filter mistakes: early string termination, single-pass strip of traversal markers, incomplete multi-layer URL decoding, and fixed-buffer truncation that drops a filter suffix while leaving a dangerous prefix. Frames traversal hunting as a normalization-mismatch problem across proxy, app, and OS. Extract advises documenting observed normalization behavior and not pasting raw bypass strings into public writeups. Pattern: Treat path/file-param filtering as a multi-layer normalization problem; map filter mistakes (termination, single-pass strip, incomplete decoding, truncation) to how language/runtime and reverse proxy normalize before access checks.
- **Tags:** path-traversal, lfi, filter-bypass, encoding, null-byte, truncation, bug-bounty
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://x.com/BRuteLogic/status/2105307679640223925
- **Notes:** [Deep Research:12] Technique-class tip only; no bypass payloads included.

---

### 6.2 Password-reset JSON email control-character / newline injection

- **Root-cause class:** Newline / control-character injection in JSON email fields (multi-recipient mail parsing flaw)
- **Affected component:** Password-reset (or similar) APIs accepting JSON email strings and downstream mail layers
- **Impact:** Account-takeover risk if reset material is delivered to unintended additional recipients
- **Conditions called out:** Password-reset (or similar) API accepts JSON with an email string; backend or mail layer may split on newlines/control chars without validating a single address
- **What the source teaches (abstract):** Bug-bounty tip showing that control characters (especially newlines) inside a JSON email string can cause mailer/parser layers to treat multiple addresses as recipients. Post media indicated simultaneous reset mail to two disposable inboxes. Impact signal is reset link/token delivery beyond the intended single recipient; confirmation should use researcher-controlled inboxes under program rules. Pattern: On auth flows that take email in JSON, check whether control characters inside the string cause multi-recipient delivery; confirm only via unintended delivery to an inbox you control under program rules.
- **Tags:** password-reset, JSON-injection, newline-injection, ATO, input-validation, bug-bounty-tips
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://x.com/wtf_yodhha/status/2099388849772466557
- **Notes:** [Deep Research:14] High-level input-validation/ATO theme; no payloads or broadcast instructions.

---

### 6.3 Authz filter vs dispatcher path-normalization mismatches (n-day / patch-diff)

- **Root-cause class:** N-day / patch-diff research with LLM harness; authz filter vs dispatcher path-normalization mismatches
- **Affected component:** Enterprise print-management software (Papercut NG) auth/filter and dispatcher path handling (lab methodology context)
- **Impact:** Illustrates how incomplete auth checks and context confusion can enable chained access issues in enterprise software; article framed as methodology, not a public attack guide
- **Conditions called out:** Public advisory/IoCs and access to vulnerable vs patched builds for authorized lab analysis; Isolated lab (VM snapshots) plus RE tools orchestrated carefully; Human skepticism: challenge agent assumptions and demand end-to-end lab validation
- **What the source teaches (abstract):** Methodology piece on using an LLM harness with an isolated lab to accelerate advisory→root-cause→validation loops for a freshly patched, actively exploited product. High-level themes include patch-diff from IoC strings to changed auth/SQL sinks, and hunting systematic mismatches between filter normalization and router semantics or page/service context. Humans must force proof against live lab instances and avoid publishing attack guides; residual same-class bypasses may remain after vendor patches. Pattern: For freshly patched N-days: compare vulnerable vs patched labs, hunt auth-check mismatches (normalization vs router semantics; wrong-context checks), re-sweep the class post-patch, validate end-to-end in lab, disclose via vendor channels—without publishing attack guides.
- **Tags:** n-day, patch-diff, llm-harness, auth-bypass-patterns, java, enterprise-software, methodology
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://techanarchy.net/from-patch-to-exploit-using-claude-code-to-reverse-engineer-a-zero-day-in-papercut-ng/
  - https://x.com/i/web/status/2096977246531559872
- **Notes:** [Deep Research:11] Extract explicitly high-level methodology only; no exploit PoC retained.

