#!/usr/bin/env python3
"""Cross-check the PROGRESS.md findings table against files on disk.

Usage: check-deliverables.py [PROGRESS.md]
For every row of the summary table: each `reports/...md` path it names must exist, and rows whose status says
drafting / pending / NOT YET WRITTEN are listed as open. Also lists confirmed findings whose fingerprint prefix
(program part) has no report file at all. Exit 1 if a named report is missing.
Catches a deliverable lost when a background agent dies (rate limit, API error) after the table was updated.
"""
import re, sys, json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
prog = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / 'PROGRESS.md'
rows = [l for l in prog.read_text().split('\n') if re.match(r'^\| \d+ \|', l)]
missing, open_rows = [], []
for l in rows:
    num = l.split('|')[1].strip()
    for p in re.findall(r'reports/[\w.\-]+\.md', l):
        if not (root / p).exists():
            missing.append((num, p))
    if re.search(r'drafting|pending|NOT YET WRITTEN', l, re.I) and 'WITHDRAWN' not in l:
        open_rows.append(num)
print(f'{len(rows)} finding rows; {len(missing)} named reports missing; open rows: {", ".join(open_rows) or "none"}')
for n, p in missing:
    print(f'  MISSING  row {n}: {p}')
conf = root / 'findings' / 'confirmed.jsonl'
if conf.exists():
    reports = ' '.join(x.name for x in (root / 'reports').glob('*.md'))
    for line in conf.read_text().splitlines():
        if not line.strip():
            continue
        fp = json.loads(line)['fingerprint']; prog_part = fp.split(':')[0].split('-')[0]
        if prog_part not in reports:
            print(f'  NO REPORT for program prefix "{prog_part}": {fp}')
sys.exit(1 if missing else 0)
