#!/usr/bin/env bash
# Regression tests for the findings schema validator and the Stop gate.
#
#   bash scripts/test-findings-gate.sh
#
# Exit 0 = all pass.

set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
VALIDATE="$HERE/validate-findings.py"
STOPGATE="$HERE/stop-gate.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass=0; fail=0

# vcheck <expected-exit> <json-record> <description>
vcheck() {
  local want="$1" rec="$2" desc="$3" got
  printf '%s\n' "$rec" > "$TMP/one.jsonl"
  python3 "$VALIDATE" "$TMP/one.jsonl" >/dev/null 2>&1; got=$?
  if [ "$got" = "$want" ]; then printf '  ok   %s\n' "$desc"; pass=$((pass+1))
  else printf '  FAIL %s (wanted %s, got %s)\n' "$desc" "$want" "$got"; fail=$((fail+1)); fi
}

# scheck <expected-exit> <description>   (runs stop-gate against $TMP/proj)
scheck() {
  local want="$1" desc="$2" extra="${3:-}" got
  got=$(printf '{"hook_event_name":"Stop","cwd":"%s"%s}' "$TMP/proj" "$extra" \
        | CLAUDE_PROJECT_DIR="$TMP/proj" python3 "$STOPGATE" >/dev/null 2>&1; echo $?)
  if [ "$got" = "$want" ]; then printf '  ok   %s\n' "$desc"; pass=$((pass+1))
  else printf '  FAIL %s (wanted %s, got %s)\n' "$desc" "$want" "$got"; fail=$((fail+1)); fi
}

GOOD_CONFIRMED='{"verdict":"confirmed","fingerprint":"export-tenant-filter-missing","class":"idor","location":"POST /api/v2/reports/export","target":"api.example.com","date":"2026-10-03","root_cause":"export worker builds its own query without the tenant middleware","trace":[{"kind":"entrypoint","file":"router.go","line":142,"scope":"public","description":"POST /api/v2/reports/export"},{"kind":"sink","file":"worker/export.go","line":67,"scope":"worker","description":"raw query executed without tenant scope"}],"evidence":[{"file":"worker/export.go","line":67,"description":"query built from filter with no tenant predicate"}],"conditions":[{"kind":"authentication_level","detail":"any authenticated user","prevalence":"default"}],"impact_sentence":"An authenticated attacker in tenant A can read report rows belonging to tenant B.","severity":"high","confidence":"high","remediation":"route the export worker through the same scoped repository method as the sync path","gate_6_human_reviewed":false}'

GOOD_REJECTED='{"verdict":"rejected","fingerprint":"invoice-idor-v2","class":"idor","location":"GET /v2/invoices/{id}","target":"api.example.com","date":"2026-10-03","claimed_root_cause":"invoice id not authorized against session tenant","reason":"middleware/tenant.go:88 validates the id against the session tenant before the handler runs","gate_failed":2,"reopen_if":"the middleware is removed or a route bypasses it"}'

GOOD_NEEDS_VAL='{"verdict":"needs_validation","fingerprint":"webhook-ssrf-egress","class":"ssrf","location":"POST /api/v2/webhooks/test","target":"api.example.com","date":"2026-10-03","claimed_root_cause":"webhook test endpoint fetches a user-supplied URL","trace":[{"kind":"entrypoint","file":"router.go","line":88,"scope":"public","description":"POST /api/v2/webhooks/test"},{"kind":"sink","file":"svc/webhook.go","line":31,"scope":"service","description":"http.Get on user-supplied url"}],"evidence":[{"file":"svc/webhook.go","line":31,"description":"no host allowlist before the fetch"}],"blockers":["cannot observe whether egress filtering exists at the network layer from source alone"],"validation_plan":{"deployment":["point the webhook at an OOB host with a nonce and check for the callback"]}}'

echo "Validator — well-formed records accepted:"
vcheck 0 "$GOOD_CONFIRMED"  'confirmed record with full trace and evidence'
vcheck 0 "$GOOD_REJECTED"   'rejected record with reason and gate_failed'
vcheck 0 "$GOOD_NEEDS_VAL"  'needs_validation with blockers and a concrete plan'

echo "Validator — the forbidden-field rule (the point of the schema):"
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); r['severity']='critical'; print(json.dumps(r))" "$GOOD_NEEDS_VAL")" \
  'needs_validation carrying a severity is rejected'
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); r['severity']='high'; print(json.dumps(r))" "$GOOD_REJECTED")" \
  'rejected carrying a severity is rejected'
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); r['blockers']=['x']; print(json.dumps(r))" "$GOOD_CONFIRMED")" \
  'confirmed carrying blockers is rejected'

echo "Validator — Gate 2 trace integrity:"
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); r['trace'][0]['kind']='propagation'; print(json.dumps(r))" "$GOOD_CONFIRMED")" \
  'trace not starting at an entrypoint is rejected'
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); r['trace']=[r['trace'][0]]; print(json.dumps(r))" "$GOOD_CONFIRMED")" \
  'single-hop trace is rejected (no chain)'
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); r['trace'][1]['line']=0; print(json.dumps(r))" "$GOOD_CONFIRMED")" \
  'trace line number 0 is rejected'

echo "Validator — honest-writing rules:"
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); r['impact_sentence']='An attacker might probably be able to read other tenants data.'; print(json.dumps(r))" "$GOOD_CONFIRMED")" \
  'hedged impact_sentence on a confirmed record is rejected'
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); r['impact_sentence']='Bad.'; print(json.dumps(r))" "$GOOD_CONFIRMED")" \
  'impact_sentence too short to name who/what/whose is rejected'
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); r['conditions'][0]['prevalence']='sometimes'; print(json.dumps(r))" "$GOOD_CONFIRMED")" \
  'condition prevalence outside default/common/unusual is rejected'

echo "Validator — schema hygiene:"
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); r['extra_thing']=1; print(json.dumps(r))" "$GOOD_CONFIRMED")" \
  'unknown top-level field is rejected (closed schema)'
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); r['fingerprint']='has spaces'; print(json.dumps(r))" "$GOOD_CONFIRMED")" \
  'fingerprint with spaces is rejected'
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); r['verdict']='maybe'; print(json.dumps(r))" "$GOOD_CONFIRMED")" \
  'unknown verdict is rejected'
vcheck 1 "$(python3 -c "
import json,sys; r=json.loads(sys.argv[1]); del r['gate_failed']; print(json.dumps(r))" "$GOOD_REJECTED")" \
  'rejected without gate_failed is rejected'
vcheck 1 '{"verdict":"confirmed"' 'malformed JSON line is reported'

echo "Stop gate:"
mkdir -p "$TMP/proj/findings" "$TMP/proj/reports" "$TMP/proj/scripts"
cp "$VALIDATE" "$TMP/proj/scripts/"
scheck 0 'no findings dir content: allows'

printf '%s\n' "$GOOD_CONFIRMED" > "$TMP/proj/findings/confirmed.jsonl"
scheck 0 'unreviewed finding with NO report draft: allows (normal resting state)'

cat > "$TMP/proj/reports/2026-10-03-example-idor.md" <<'EOF'
# Report draft
fingerprint: export-tenant-filter-missing
EOF
scheck 2 'report draft referencing an unreviewed finding: BLOCKS'

scheck 0 'same state but stop_hook_active set: allows (no loop trap)' ',"stop_hook_active":true'

python3 - "$TMP/proj/findings/confirmed.jsonl" <<'PY'
import json,sys
p=sys.argv[1]; r=json.loads(open(p).read().strip()); r['gate_6_human_reviewed']=True
open(p,'w').write(json.dumps(r)+"\n")
PY
scheck 0 'after a human sets gate_6_human_reviewed: allows'

printf '{"verdict":"confirmed","fingerprint":"bad"}\n' > "$TMP/proj/findings/confirmed.jsonl"
scheck 2 'schema-violating findings file: BLOCKS'

echo
printf '%s passed, %s failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
