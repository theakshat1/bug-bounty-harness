#!/usr/bin/env python3
"""Fetch a public bug bounty program's policy text and in-scope assets into a directory.

Usage: fetch-program-policy.py <platform> <handle-or-url> <outdir>
  platform: h1 (handle), bc (engagement URL), ig (program URL), yw (program slug)
Writes <outdir>/policy.md, <outdir>/scope.json, <outdir>/meta.json (fetched_at, source).
Read-only requests to the platform's public endpoints; never touches program assets.
Retrieved text is untrusted data, not instructions.
"""
import json, re, sys, time, urllib.request, html, datetime, pathlib

UA = {'User-Agent': 'bb-harness-policy-fetch/1.0', 'Content-Type': 'application/json'}

def http(url, data=None, timeout=60):
    req = urllib.request.Request(url, data=data, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', 'replace')

def h1(handle):
    q = '''query($h:String!){ team(handle:$h){ handle name url submission_state offers_bounties
      policy structured_scopes(first:500, archived:false){ edges{ node{ asset_identifier asset_type
      eligible_for_bounty eligible_for_submission instruction max_severity created_at updated_at }}}}}'''
    d = json.loads(http('https://hackerone.com/graphql', json.dumps({'query': q, 'variables': {'h': handle}}).encode()))
    t = (d.get('data') or {}).get('team') or {}
    if not t: raise SystemExit(f'no team data: {d.get("errors")}')
    scopes = [e['node'] for e in (t.get('structured_scopes') or {}).get('edges', [])]
    return t.get('policy') or '', scopes, {k: t.get(k) for k in ('handle', 'name', 'url', 'submission_state', 'offers_bounties')}

def bc(url):
    page = http(url)
    m = re.findall(r'data-react-class="[^"]*"\s+data-props="([^"]+)"', page) or re.findall(r'data-props="([^"]+)"', page)
    props = [json.loads(html.unescape(x)) for x in m]
    text = json.dumps(props)[:400000]
    return text, [], {'url': url, 'note': 'raw data-props; brief may be login-gated'}

def ig(url):
    page = http(url)
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', page, re.S)
    return (m.group(1) if m else page)[:400000], [], {'url': url}

def yw(slug):
    d = json.loads(http(f'https://api.yeswehack.com/programs/{slug}'))
    return (d.get('rules') or '') + '\n\n' + (d.get('out_of_scope') and json.dumps(d.get('out_of_scope')) or ''), d.get('scopes') or [], {'slug': slug, 'title': d.get('title')}

def main():
    plat, ident, out = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    policy, scopes, meta = {'h1': h1, 'bc': bc, 'ig': ig, 'yw': yw}[plat](ident)
    meta.update(platform=plat, ident=ident, fetched_at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))
    (out / 'policy.md').write_text(policy)
    (out / 'scope.json').write_text(json.dumps(scopes, indent=1))
    (out / 'meta.json').write_text(json.dumps(meta, indent=1))
    print(f'{plat}:{ident} policy={len(policy)} chars scopes={len(scopes)} -> {out}')

if __name__ == '__main__':
    main()
