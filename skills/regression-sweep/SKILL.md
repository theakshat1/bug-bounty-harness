---
name: regression-sweep
description: Retest resolved reports and shipped fixes for bypasses, sibling-endpoint variants, and incomplete patches. Use when starting work on a program with public disclosures, or revisiting a target you have reported on before. Highest ROI surface available and almost nobody works it.
argument-hint: "[program-or-report-url]"
---

# Regression Sweep

> A fix is new code, written under time pressure, often by someone who didn't write
> the original — and you already have full context on how the bug worked. Resolved
> reports are the highest-ROI surface in bug bounty, and almost nobody works them.

Bypasses of shipped fixes are **often paid in full** and are duplicate-resistant,
because reproducing them requires the original context.

## Sources of leads

**Start with the private corpus:**
`corpus/x-bookmarks-2026-09/bb-research/x-bookmarks-2026-09-detailed/10-n-day-patch.md`
holds n-day and patch-diff pattern cards — including the authz-filter-vs-dispatcher
normalization mismatch class and version-fingerprint triage. Read it before working a
target with public advisories.


1. **The program's public disclosures** (HackerOne/Bugcrowd disclosed reports).
2. **Your own resolved reports** — the HackerOne MCP is read-only and good for this.
3. **The changelog / release notes / security advisories** — a terse "fixed an
   authorization issue in exports" is a map.
4. **CVE and advisory feeds** for the components and versions in scope.
5. **Public commits**, where the target is source-available: a security fix commit
   tells you the sink, the guard, and often the exact input class.

## The five regression patterns

Work them in this order — cheapest and highest-hit-rate first.

### 1. Sibling endpoint
The fix landed on the endpoint that was reported. Did it land on the others that
reach the same sink?

- The same resource via a different route (`/api/export` vs `/api/v2/export`)
- The REST route fixed, the GraphQL resolver not
- The single-item route fixed, the **batch/bulk** variant not
- The UI's path fixed, the mobile/API path not
- **A fix on one backend is not a fix if siblings remain.**

### 2. Sibling parameter
Same handler, different input. If the fix validated `filename`, does it validate
`template`, `path`, `url`, `redirect`, `callback`? Patches are frequently
parameter-specific rather than sink-specific.

### 3. Incomplete normalization
The classic patch failure. If the fix added a blocklist or a single-pass strip:
- does it survive **double** encoding?
- does it strip once where the input contains two instances?
- is the check before or after the framework's own normalization?
- does truncation at a buffer boundary drop the filter's suffix while leaving a
  dangerous prefix?

Map each test to how the runtime **and** the reverse proxy normalize before the
access check. This is a normalization-mismatch problem across proxy, app and OS.

### 4. Guard in the wrong layer
The fix added a check in the controller, but the sink is reachable from a service
method another controller also calls. Trace **every** caller of the sink, not just
the reported one.

### 5. Reverted or regressed fix
Fixes get lost in merges, refactors and reverts. If you reported it a year ago,
test it again — plainly. This happens more than anyone admits.

## Method

For each resolved report:

1. **Reconstruct the original** — the sink, the input, the guard that was missing,
   the entrypoint.
2. **Confirm the fix works** on the original path. (If it doesn't, you're done —
   that's a straightforward regression.)
3. **Enumerate siblings** across the five patterns above. Write them down as a list
   before testing, so coverage is deliberate rather than opportunistic.
4. **Test each** against the normal gate ladder. A regression finding is still a
   finding and still needs the full `validate-finding` treatment — being "the same
   bug as before" is not evidence it's exploitable now.
5. **Record coverage** in `recon/coverage.md` so a later run doesn't redo it.

## Advisory sweep (version-driven)

Where you can fingerprint a product and version in scope:
- Cross-reference against CVE/KEV feeds for that product and version range.
- Prioritize **authorization flaws and stored XSS reachable by low-privilege users**
  — those map most reliably onto bounty impact.
- Map bulletin CVEs to version fingerprints before testing anything, so you're not
  probing for bugs the deployed version never had.
- When vendor pages block scrapers, CERT mirrors and CVE aggregators carry enough
  for scope triage.

**Confirm the version actually deployed.** Reporting an n-day the target already
patched is a signal-score hit.

## Reporting a regression

**Say it's a bypass in the summary, and link the original.** This:
- pre-empts a duplicate close
- reads as competence rather than recycling
- gives triage the context to route it to the right engineer immediately

Structure the summary as: *"This bypasses the fix for \<original report/CVE\>. The
patch addressed \<X\>; the same boundary fails via \<Y\>, which the patch does not
cover."*

Then state explicitly **why the original fix doesn't cover your path** — that single
sentence is what makes a regression report land.

## Honesty requirements

- If the original fix **does** hold on your path, record that in the coverage ledger
  and move on. A verified-clean regression check is useful work.
- Don't inflate a partial bypass into a full one.
- If you can only reach it with different (harder) preconditions than the original,
  say so and expect a lower severity.
