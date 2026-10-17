#!/usr/bin/env python3
"""Rank surveyed programs. Reads recon/survey-*/h1-*/ (from fetch-program-policy.py).

Usage: screen-programs.py <survey_dir> <as_of YYYY-MM-DD> [recent_days=120]
Output TSV (stdout): score, handle, new_assets, src_assets, web_assets, ai_policy, alias_req, max_usd, new_asset_sample
Signals are heuristics for triage only; a human/agent reads the policy before any testing.
"""
import json, re, sys, pathlib, datetime

d0 = pathlib.Path(sys.argv[1]); asof = datetime.date.fromisoformat(sys.argv[2]); days = int(sys.argv[3]) if len(sys.argv) > 3 else 120
AI_BAN = re.compile(r'(AI|LLM|ChatGPT|GPT|machine)[- ]?(generated|written|assisted|tool)s?[^.]{0,80}(not|no|prohibit|reject|ban|disallow|will be closed|invalid)|(not|no|prohibit|reject|ban)[^.]{0,60}(AI|LLM|ChatGPT)[- ]?(generated|written|assisted|tools)', re.I)
AI_ANY = re.compile(r'\b(AI-generated|AI generated|LLM|ChatGPT|artificial intelligence|AI tools?|AI-assisted)\b', re.I)
ALIAS = re.compile(r'@wearehackerone\.com|hackerone email alias|X-HackerOne|X-Bug-Bounty|bugbounty header|must use your .{0,30}alias', re.I)
NOACCT = re.compile(r'(do not|don\'t|must not) (create|register|sign up)[^.]{0,40}account', re.I)
USD = re.compile(r'\$\s?([0-9]{1,3}(?:,[0-9]{3})+|[0-9]{3,6})')
rows = []
for p in sorted(d0.glob('h1-*')):
    try:
        meta = json.loads((p / 'meta.json').read_text()); scopes = json.loads((p / 'scope.json').read_text()); pol = (p / 'policy.md').read_text()
    except Exception:
        continue
    elig = [s for s in scopes if s.get('eligible_for_bounty')]
    new = [s for s in elig if s.get('created_at') and (asof - datetime.date.fromisoformat(s['created_at'][:10])).days <= days]
    src = [s for s in elig if s['asset_type'] == 'SOURCE_CODE']
    web = [s for s in elig if s['asset_type'] in ('URL', 'WILDCARD', 'API', 'CIDR', 'IP_ADDRESS')]
    ai = 'BAN' if AI_BAN.search(pol) else ('mentions' if AI_ANY.search(pol) else '-')
    alias = 'alias' if ALIAS.search(pol) else ('no-acct' if NOACCT.search(pol) else '-')
    usd = max([int(x.replace(',', '')) for x in USD.findall(pol)] or [0])
    crit_new = sum(1 for s in new if s.get('max_severity') in ('critical', 'high'))
    score = 3 * crit_new + len(new) + (2 if src else 0) + min(len(web), 5) / 5 + (min(usd, 50000) / 25000) - (5 if ai == 'BAN' else 0)
    sample = '; '.join(f"{s['asset_type'][:4]}:{(s['asset_identifier'] or '')[:40]}({(s['created_at'] or '')[:10]},{s.get('max_severity')})" for s in new[:4])
    rows.append((round(score, 1), meta.get('handle'), len(new), len(src), len(web), ai, alias, usd, sample))
print('score\thandle\tnew\tsrc\tweb\tai\talias\tmax_usd\tnew_assets')
for r in sorted(rows, key=lambda r: -r[0]):
    print('\t'.join(str(x) for x in r))
