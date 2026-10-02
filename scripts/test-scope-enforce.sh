#!/usr/bin/env bash
# Regression tests for the scope-enforce PreToolUse hook.
#
# The hook is the only control that actually stops an agent leaving scope, so it
# gets tests. Run it after any change to scripts/scope-enforce.py:
#
#   bash scripts/test-scope-enforce.sh
#
# Exit 0 = all pass.

set -uo pipefail

HOOK="$(cd "$(dirname "$0")" && pwd)/scope-enforce.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass=0
fail=0

# check <expected-exit> <json> <description>
check() {
  local want="$1" json="$2" desc="$3" got
  echo "$json" | CLAUDE_PROJECT_DIR="$PWD" python3 "$HOOK" >/dev/null 2>&1
  got=$?
  if [ "$got" = "$want" ]; then
    printf '  ok   %s\n' "$desc"
    pass=$((pass + 1))
  else
    printf '  FAIL %s (wanted exit %s, got %s)\n' "$desc" "$want" "$got"
    fail=$((fail + 1))
  fi
}

mkdir -p "$TMP/withscope/scope"
cat > "$TMP/withscope/scope/allowlist.txt" <<'EOF'
# test allowlist
*.example.com
api.target.io
!blog.example.com
EOF

cd "$TMP/withscope"

echo "Blocked (exit 2):"
check 2 '{"tool_name":"WebFetch","tool_input":{"url":"https://evil.test/x"}}'            'WebFetch to off-allowlist host'
check 2 '{"tool_name":"WebFetch","tool_input":{"url":"https://blog.example.com/"}}'      'explicit denylist overrides wildcard'
check 2 '{"tool_name":"Bash","tool_input":{"command":"curl -s https://evil.test/a"}}'    'Bash curl to off-allowlist host'
check 2 '{"tool_name":"Bash","tool_input":{"command":"httpx -u notmine.org"}}'           'bare hostname passed to recon CLI'
check 2 '{"tool_name":"Bash","tool_input":{"command":"nuclei -u https://api.example.com -u https://other.net"}}' 'mixed hosts, one off-allowlist'
check 2 '{"tool_name":"Bash","tool_input":{"command":"curl https://api.example.com.evil.net/"}}' 'suffix-confusion domain'

echo "Allowed (exit 0):"
check 0 '{"tool_name":"WebFetch","tool_input":{"url":"https://api.example.com/v1"}}'     'wildcard match'
check 0 '{"tool_name":"WebFetch","tool_input":{"url":"https://example.com/"}}'           'apex covered by *.example.com'
check 0 '{"tool_name":"WebFetch","tool_input":{"url":"https://deep.a.b.example.com/"}}'  'multi-level subdomain'
check 0 '{"tool_name":"WebFetch","tool_input":{"url":"https://api.target.io/x"}}'        'exact host match'
check 0 '{"tool_name":"Bash","tool_input":{"command":"curl http://127.0.0.1:8080/"}}'    'localhost permitted'
check 0 '{"tool_name":"Bash","tool_input":{"command":"ls -la && cat notes.md"}}'         'command with no network activity'
check 0 '{"tool_name":"Read","tool_input":{"file_path":"/etc/hosts"}}'                   'non-network tool ignored'
check 0 '{"tool_name":"WebSearch","tool_input":{"query":"example.com bug bounty"}}'      'WebSearch does not contact target'
check 0 '{"tool_name":"Bash","tool_input":{"command":"cat subdomains.txt | wc -l"}}'     'filename not misread as hostname'

echo "Fail-closed:"
mkdir -p "$TMP/noscope"
cd "$TMP/noscope"
check 2 '{"tool_name":"WebFetch","tool_input":{"url":"https://anything.com/"}}'          'no allowlist file blocks all egress'
check 2 'not json at all'                                                               'unparseable hook input blocks'

echo
printf '%s passed, %s failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
