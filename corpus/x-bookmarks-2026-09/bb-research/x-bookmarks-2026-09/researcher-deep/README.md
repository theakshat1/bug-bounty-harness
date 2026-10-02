# Researcher Lane — Deep NON-REPRO Docs

**Primary document:** [`RESEARCHER_DEEP.md`](./RESEARCHER_DEEP.md) — all 23 items as H2 sections.  
**Source extract (only):** `/workspace/researcher-lane-extract-2026-10.md`  
**Lane exclusivity:** Researcher items only. Do **not** merge other agents’ KB entries.  
**Built:** 2026-10-02 (Asia/Calcutta)

## Counts

| Status | Count |
|--------|------:|
| ok | 20 |
| blocked | 2 (#03, #08) |
| thin | 1 (#04) |
| **Total** | **23** |

## Hard constraints (cyber / offensive)

- **NO** reproduction steps, attack procedures, payloads, PoCs, exploit commands, wordlist contents, Intruder setups, or “how to hit new surfaces” walkthroughs.
- **NO** reconstructing attack steps even if the original write-up had them.
- Methodology / pattern / design-root-cause language only. Educational authorized BB framing.
- Do **not** open primary URLs to pull attack detail. Work from the extract + non-step metadata already there. If extract is thin, say what’s missing rather than inventing.
- Stay exclusive to Researcher lane items in that extract file.

## Per-item schema

Each item in `RESEARCHER_DEEP.md` includes only:

1. **Title**
2. **Source URL(s)** — primary + any alternate already noted for blocked/thin
3. **Status** — `ok` / `blocked` / `thin` + honesty notes
4. **Root-cause class** — design/logic failure mode (not how to exploit)
5. **Affected component / surface**
6. **Impact** — high-level, as described in source
7. **Conditions / preconditions** — environmental facts, not attack steps
8. **Generalized defensive / hunt-planning idea** — from extract; non-procedural
9. **Tags**
10. **Lane:** Researcher

## Index — Articles (1–11)

| # | File anchor | Title | Status |
|---|-------------|-------|--------|
| 01 | [SubMap](./RESEARCHER_DEEP.md#01--submap--subdomain-discovery--ip-intelligence-platform) | SubMap — Subdomain Discovery & IP Intelligence Platform | ok |
| 02 | [PageBreak (blog.google)](./RESEARCHER_DEEP.md#02--agentic-hacks-real-proofs-inside-googles-pagebreak-project) | Agentic Hacks, Real Proofs: Inside Google's PageBreak Project | ok |
| 03 | [PageBreak real-world findings](./RESEARCHER_DEEP.md#03--pagebreak-real-world-findings-companion-post-primary-url-gated) | PageBreak real-world findings (primary gated) | **blocked** |
| 04 | [CVE-2026-52924 SCTP](./RESEARCHER_DEEP.md#04--linux-cve-2026-52924-ubuntu-700-28-nebusec--cybermeowfia) | Linux-CVE-2026-52924-ubuntu-7.0.0-28 | **thin** |
| 05 | [StrikeAgent](./RESEARCHER_DEEP.md#05--strikeagent_atkbrain-flash-yean-sec-ai-pentest-agent) | StrikeAgent_AtkBrain-Flash | ok |
| 06 | [Claude-BugHunter skills](./RESEARCHER_DEEP.md#06--claude-bughunter-skill-bundle-83-skills-h1-pattern-driven) | Claude-BugHunter skill bundle | ok |
| 07 | [Quarry](./RESEARCHER_DEEP.md#07--quarry--agentic-bb-console-with-hackerone-integration) | Quarry — agentic BB console + H1 | ok |
| 08 | [APSB26-98 AEM](./RESEARCHER_DEEP.md#08--apsb26-98--security-updates-for-adobe-experience-manager) | APSB26-98 — Adobe Experience Manager | **blocked** |
| 09 | [Local LLM vuln detection](./RESEARCHER_DEEP.md#09--can-local-open-weight-llms-detect-vulnerabilities) | Can Local Open-Weight LLMs Detect Vulnerabilities? | ok |
| 10 | [IDOR → priv-esc](./RESEARCHER_DEEP.md#10--2000-bounty--idor-to-privilege-escalation-from-admin-to-internal-employee) | €2000 IDOR to Privilege Escalation | ok |
| 11 | [STAR Labs AI 0-days](./RESEARCHER_DEEP.md#11--when-ai-makes-0-days-feel-like-n-days-star-labs) | When AI Makes 0-Days Feel Like N-Days | ok |

## Index — Posts (12–23)

| # | File anchor | Title | Status |
|---|-------------|-------|--------|
| 12 | [@aacle_ under-tested](./RESEARCHER_DEEP.md#12--crowded-login-pages-vs-boring-features-aacle_) | Crowded login pages vs boring features | ok |
| 13 | [@crusader_sec](./RESEARCHER_DEEP.md#13--autonomous-bug-hunting-with-poc-confirmation-crusader_sec) | Autonomous bug hunting with PoC confirmation | ok |
| 14 | [@adnanthekhan swarm](./RESEARCHER_DEEP.md#14--multi-model-agent-swarm--ssrfrcek8s-takeover-claimed-adnanthekhan) | Multi-model agent swarm (claimed chain) | ok (unverified claim) |
| 15 | [@ethical_h4ck3r_ XSS tip](./RESEARCHER_DEEP.md#15--xss-filter-bypass-wordlist-tip-html-entity--javascript-uri-pattern-ethical_h4ck3r_) | XSS filter-bypass wordlist tip | ok |
| 16 | [@aacle_ GCP RCE lessons](./RESEARCHER_DEEP.md#16--148k-google-cloud-rce-chains--methodology-takeaways-aacle_) | $148k Google Cloud RCE chains — takeaways | ok |
| 17 | [@ethical_h4ck3r_ blind SSRF](./RESEARCHER_DEEP.md#17--blind-ssrf-via-header-bruteforce--collaborator-ethical_h4ck3r_) | Blind SSRF via header surface + OOB | ok |
| 18 | [@OpenAI Defense Factory](./RESEARCHER_DEEP.md#18--defense-factory-playbook--find--validate--verify-fixes-openai) | Defense Factory — find → validate → verify | ok |
| 19 | [@dirtycoder0124 Android](./RESEARCHER_DEEP.md#19--android-apk-hunt-workflow-automation-dirtycoder0124) | Android APK hunt workflow automation | ok |
| 20 | [@AdamShao agentized BB](./RESEARCHER_DEEP.md#20--fully-agentized-bb-workflow-ai--flounder--codex-report-adamshao) | Fully agentized BB workflow (culture signal) | ok (satirical) |
| 21 | [@three_cube AD](./RESEARCHER_DEEP.md#21--speeding-up-ad-pentests-with-adscan-and-adpulse-three_cube) | ADScan / ADPulse AD pentest speedup | ok |
| 22 | [@n0aziXss XSS regex](./RESEARCHER_DEEP.md#22--xss-regex-bypass-payload-gallery-n0azixss) | XSS regex-bypass (mismatch classes only) | ok |
| 23 | [@zack0x01_ JWT](./RESEARCHER_DEEP.md#23--jwt-attacks-as-high-roi-bb-class-zack0x01_) | JWT as high-ROI BB class | ok |

## Thin / blocked due to source gaps

- **#03 blocked** — Google Bug Hunters sign-in wall; content from CyberKendra alternate already in extract.
- **#08 blocked** — Adobe helpx EdgeSuite 403; content from HKCERT / NotCVE already in extract.
- **#04 thin** — GitHub folder has no README; advisory-level SCTP UAF synopsis only; exploit sources not used.

## Related (structure only — do not copy other lanes)

Merged multi-lane KB (for structure reference only): `/workspace/bb-research/x-bookmarks-2026-09/Bug-Bounty-Ideas-KB.md`
