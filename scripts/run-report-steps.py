#!/usr/bin/env python3
"""Extract a report's reproduction shell blocks verbatim and (optionally) run them against a clean lab.

Usage: run-report-steps.py <report.md> <outdir> [--run] [VAR=VALUE ...]
- Takes every ```sh fenced block between the "## Steps to reproduce" heading and the next "## " heading, in order.
- Replaces only lines that START with `VAR=` for each VAR=VALUE given (the report's placeholder lines, e.g. WP= and AUTH=).
- Writes <outdir>/steps.sh with a "===== block N =====" marker before each block; with --run, executes it with bash and
  writes <outdir>/report-steps.txt. Compare the output against the report's "# expected:" comments yourself.
Run it only against a lab you control. It sends whatever the report's commands send.
"""
import re, sys, subprocess, pathlib
args = sys.argv[1:]
if len(args) < 2: sys.exit(__doc__)
report, outdir = pathlib.Path(args[0]), pathlib.Path(args[1]); run = '--run' in args
subs = dict(a.split('=', 1) for a in args[2:] if '=' in a and not a.startswith('--'))
text = report.read_text()
m = re.search(r'^## Steps to reproduce.*?$(.*?)(?=^## )', text, re.S | re.M)
if not m: sys.exit('no "## Steps to reproduce" section found')
blocks = re.findall(r'```sh\n(.*?)```', m.group(1), re.S)
lines = ['set -u', f"echo '# steps extracted verbatim from {report.name}; replaced: {', '.join(subs) or 'nothing'}'"]
for i, b in enumerate(blocks, 1):
    lines.append(f"echo '===== block {i} ====='")
    for line in b.rstrip('\n').split('\n'):
        for k, v in subs.items():
            if line.startswith(k + '='): line = f'{k}={v}'
        lines.append(line)
outdir.mkdir(parents=True, exist_ok=True)
(outdir / 'steps.sh').write_text('\n'.join(lines) + '\n')
print(f'{len(blocks)} shell blocks -> {outdir / "steps.sh"}')
if run:
    with open(outdir / 'report-steps.txt', 'w') as f:
        rc = subprocess.run(['bash', str(outdir / 'steps.sh')], cwd=outdir, stdout=f, stderr=subprocess.STDOUT).returncode
    print(f'ran: exit {rc} -> {outdir / "report-steps.txt"}')
