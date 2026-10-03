#!/usr/bin/env bash
# Run every check in the harness. Use this before committing a change to hooks,
# scripts, skills or agents.
#
#   bash scripts/test-all.sh
#
# Exit 0 = everything passes.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

fail=0
section() { printf '\n\033[1m== %s ==\033[0m\n' "$1"; }
ok()      { printf '  ok   %s\n' "$1"; }
bad()     { printf '  FAIL %s\n' "$1"; fail=1; }

section "Python syntax"
if python3 -m py_compile scripts/*.py 2>/dev/null; then ok "scripts compile"; else bad "scripts do not compile"; fi

section "JSON well-formedness"
for f in .claude-plugin/plugin.json .claude-plugin/marketplace.json hooks/hooks.json reference/mcp-examples/mcp.json; do
  if python3 -c "import json;json.load(open('$f'))" 2>/dev/null; then ok "$f"; else bad "$f"; fi
done

section "Plugin manifests"
if command -v claude >/dev/null 2>&1; then
  if claude plugin validate . 2>&1 | grep -q "Validation passed"; then ok "claude plugin validate"; else bad "claude plugin validate"; fi
else
  printf '  skip claude CLI not on PATH\n'
fi

section "Skill / agent frontmatter"
if python3 - <<'PY'
import glob, sys
try:
    import yaml
except ImportError:
    print("  skip pyyaml not installed"); sys.exit(0)
bad = []
n = 0
for f in sorted(glob.glob('skills/*/SKILL.md') + glob.glob('agents/*.md')):
    txt = open(f).read()
    if not txt.startswith('---\n'):
        bad.append(f"{f}: no frontmatter"); continue
    try:
        d = yaml.safe_load(txt.split('---\n', 2)[1])
    except Exception as e:
        bad.append(f"{f}: bad yaml: {e}"); continue
    for k in ('name', 'description'):
        if not d.get(k):
            bad.append(f"{f}: missing {k}")
    n += 1
if bad:
    print("\n".join("  " + b for b in bad)); sys.exit(1)
print(f"  {n} components have name + description")
PY
then ok "frontmatter"; else bad "frontmatter"; fi

section "Hook: scope enforcement"
if bash scripts/test-scope-enforce.sh >/tmp/bb-scope.$$ 2>&1; then
  ok "$(tail -1 /tmp/bb-scope.$$)"
else
  bad "scope hook"; grep -E '^\s+FAIL' /tmp/bb-scope.$$ | head -10
fi
rm -f /tmp/bb-scope.$$

section "Hook: findings schema + stop gate"
if bash scripts/test-findings-gate.sh >/tmp/bb-find.$$ 2>&1; then
  ok "$(tail -1 /tmp/bb-find.$$)"
else
  bad "findings gate"; grep -E '^\s+FAIL' /tmp/bb-find.$$ | head -10
fi
rm -f /tmp/bb-find.$$

section "Docs: internal links resolve"
if python3 - <<'PY'
import re, pathlib, sys
bad = []
for f in pathlib.Path('.').rglob('*.md'):
    s = str(f)
    if '.git' in s or s.startswith('corpus/'):
        continue
    for m in re.finditer(r'\]\((\.{1,2}/[^)#]+|[A-Za-z0-9_][^):#]*\.md)', f.read_text()):
        if not (f.parent / m.group(1)).resolve().exists():
            bad.append(f"{f} -> {m.group(1)}")
if bad:
    print("\n".join("  BROKEN " + b for b in bad)); sys.exit(1)
print("  all relative links resolve")
PY
then ok "links"; else bad "links"; fi

printf '\n'
if [ "$fail" -eq 0 ]; then printf '\033[1mALL CHECKS PASSED\033[0m\n'; else printf '\033[1mFAILURES ABOVE\033[0m\n'; fi
exit "$fail"
