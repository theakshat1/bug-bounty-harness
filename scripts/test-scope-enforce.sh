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

# check <expected-exit> <json> <description>  [env assignments via CHECK_ENV]
check() {
  local want="$1" json="$2" desc="$3" got
  if [ -n "${CHECK_ENV:-}" ]; then
    got=$(echo "$json" | env CLAUDE_PROJECT_DIR="$PWD" $CHECK_ENV python3 "$HOOK" >/dev/null 2>&1; echo $?)
  else
    got=$(echo "$json" | CLAUDE_PROJECT_DIR="$PWD" python3 "$HOOK" >/dev/null 2>&1; echo $?)
  fi
  if [ "$got" = "$want" ]; then
    printf '  ok   %s\n' "$desc"; pass=$((pass + 1))
  else
    printf '  FAIL %s (wanted exit %s, got %s)\n' "$desc" "$want" "$got"; fail=$((fail + 1))
  fi
}

mkdir -p "$TMP/withscope/scope"
cat > "$TMP/withscope/scope/allowlist.txt" <<'EOF'
# test allowlist
*.example.com
api.target.io
!blog.example.com
@mcp-local semgrep
EOF
# a target-list file: one in-scope host, one not
printf 'api.example.com\nevil.test\n' > "$TMP/withscope/targets.txt"
printf 'api.example.com\nwww.example.com\n' > "$TMP/withscope/good-targets.txt"

cd "$TMP/withscope"

echo "Built-in tools — blocked (exit 2):"
check 2 '{"tool_name":"WebFetch","tool_input":{"url":"https://evil.test/x"}}'            'WebFetch to off-allowlist host'
check 2 '{"tool_name":"WebFetch","tool_input":{"url":"https://blog.example.com/"}}'      'explicit denylist overrides wildcard'
check 2 '{"tool_name":"Bash","tool_input":{"command":"curl -s https://evil.test/a"}}'    'Bash curl to off-allowlist host'
check 2 '{"tool_name":"Bash","tool_input":{"command":"httpx -u notmine.org"}}'           'bare hostname passed to recon CLI'
check 2 '{"tool_name":"Bash","tool_input":{"command":"nuclei -u https://api.example.com -u https://other.net"}}' 'mixed hosts, one off-allowlist'
check 2 '{"tool_name":"Bash","tool_input":{"command":"curl https://api.example.com.evil.net/"}}' 'suffix-confusion domain'

echo "Target-list files (regression: hosts hidden in a file):"
check 2 '{"tool_name":"Bash","tool_input":{"command":"httpx -l targets.txt"}}'           '-l file containing an off-allowlist host'
check 2 '{"tool_name":"Bash","tool_input":{"command":"subfinder -dL targets.txt -all"}}' '-dL file containing an off-allowlist host'
check 2 '{"tool_name":"Bash","tool_input":{"command":"nmap -iL targets.txt"}}'           '-iL file containing an off-allowlist host'
check 0 '{"tool_name":"Bash","tool_input":{"command":"httpx -l good-targets.txt"}}'      '-l file with only in-scope hosts'

echo "MCP tools (regression: these bypassed scope entirely before):"
check 2 '{"tool_name":"mcp__burp__send_http1_request","tool_input":{"host":"evil.test","port":443,"useHttps":true,"request":"GET / HTTP/1.1\r\nHost: evil.test\r\n\r\n"}}' 'Burp MCP raw request to off-allowlist host'
check 2 '{"tool_name":"mcp__burp__send_http2_request","tool_input":{"pseudoHeaders":{":authority":"evil.test",":path":"/"}}}' 'Burp MCP HTTP/2 pseudo-header authority'
check 2 '{"tool_name":"mcp__burp__create_repeater_tab","tool_input":{"request":"GET /x HTTP/1.1\nHost: notmine.org\n\n"}}' 'Host: header inside a raw request field'
check 2 '{"tool_name":"mcp__recon__httpx","tool_input":{"targets":["api.example.com","evil.test"]}}' 'array of targets, one off-allowlist'
check 2 '{"tool_name":"mcp__somewrapper__scan","tool_input":{"opts":{"nested":{"url":"https://evil.test/x"}}}}' 'URL nested deep in unknown schema'
check 0 '{"tool_name":"mcp__burp__send_http1_request","tool_input":{"host":"api.example.com","request":"GET / HTTP/1.1\r\nHost: api.example.com\r\n\r\n"}}' 'Burp MCP to in-scope host'
check 0 '{"tool_name":"mcp__burp__url_encode","tool_input":{"text":"hello world"}}'      'MCP util call with no host'

echo "MCP local-server exemption (@mcp-local):"
check 0 '{"tool_name":"mcp__semgrep__security_check","tool_input":{"code":"fetch(\"https://evil.test/x\")"}}' 'semgrep marked @mcp-local: hostname in code is data'
check 2 '{"tool_name":"mcp__other__security_check","tool_input":{"code":"fetch(\"https://evil.test/x\")"}}'   'same payload on a server NOT marked local is blocked'

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

echo "Strict MCP mode (BB_MCP_STRICT=1):"
CHECK_ENV="BB_MCP_STRICT=1" check 2 '{"tool_name":"mcp__weird__go","tool_input":{"blob":"connect to evil.test now"}}' 'bare host in a non-host field is caught in strict mode'
check 0 '{"tool_name":"mcp__weird__go","tool_input":{"blob":"connect to evil.test now"}}' 'same input passes in default mode (documented tradeoff)'
unset CHECK_ENV

echo "Fail-closed:"
mkdir -p "$TMP/noscope"
cd "$TMP/noscope"
check 2 '{"tool_name":"WebFetch","tool_input":{"url":"https://anything.com/"}}'          'no allowlist file blocks all egress'
check 2 '{"tool_name":"mcp__burp__send_http1_request","tool_input":{"host":"anything.com"}}' 'no allowlist blocks MCP egress too'
check 2 'not json at all'                                                               'unparseable hook input blocks'
CHECK_ENV="BB_FAIL_OPEN=1" check 0 'not json at all'                                     'BB_FAIL_OPEN=1 allows on parse failure (debug escape hatch)'
unset CHECK_ENV

echo
printf '%s passed, %s failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
