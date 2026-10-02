# JS / Sourcemap recon & client secrets

**Cluster file:** `02-js-secrets.md`  
**Audience:** Akshat (authorized / in-scope hunting only)  
**Constraint:** Abstract methodology only — **no** reproduction steps, payloads, PoCs, exploit recipes, Intruder setups, or attack procedures.  
**Items in this cluster:** 2

---

### 2.1 Secret hunting by key *names* near assignments

- **Root-cause class:** Secret / credential pattern matching (static secret hunting)
- **Affected component:** Source, configs, CI env dumps, JS bundles, public repos in scope
- **Impact:** Leaked credentials/secrets in readable sources when name-based detectors catch misnamed keys format-only tools miss.
- **Conditions called out:** Readable source, configs, CI env dumps, JS bundles, or public repos in scope
- **What the source teaches (abstract):** Hunt leaked credentials by matching high-signal key *names* (api_key, aws_secret, client_secret, db_password, cloudflare_api_key, etc.) near assignment operators rather than only known token formats. Broad name-based regexes catch misnamed or vendor-specific secrets that format-only detectors miss; combine with entropy/format validators and rotate-on-find hygiene. Useful as one layer in JS/env/.git history secret sweeps during recon. Extract note: Popular gist (129 forks / 60 comments); single large case-insensitive OR-list of credential-ish identifiers. Methodology extract only—do not treat as an exploit kit. Use as an authorized-hunting pattern or process cue only: map the trust boundary or workflow stage the source highlights; do not treat this entry as a reproduction guide.
- **Tags:** secrets, regex, credential-leak, recon, gist, static-analysis
- **Lane:** Researchy
- **Quality:** ok
- **Sources:**
  - https://gist.github.com/h4x0r-dz/be69c7533075ab0d3f0c9b97f7c93a59
  - https://x.com/i/web/status/2097741657684971786
- **Notes:** [Researchy:A.4] Popular gist (129 forks / 60 comments); single large case-insensitive OR-list of credential-ish identifiers. Methodology extract only—do not treat as an exploit kit.

---

### 2.2 Cognito / Identity Pool client config in JS & source maps

- **Root-cause class:** Client-side secret exposure; Cognito User/Identity Pool misconfiguration → temporary cloud credentials
- **Affected component:** SPA/dev JS bundles and source maps exposing Cognito User Pool / Identity Pool client configuration
- **Impact:** Exposure enabling temporary AWS credentials via over-permissioned identity-pool IAM roles (authorized proof scope only)
- **Conditions called out:** JS bundles (especially source maps) on in-scope hosts exposing Cognito pool/client/identity IDs; Cognito flows that allow signup/auth and identity pools with usable IAM roles for authenticated users; Authorized bug-bounty testing of the affected program
- **What the source teaches (abstract):** Writeup on mining SPA/dev JS and reconstructed source maps for Cognito userPoolId, clientId, and identityPoolId configuration. Client IDs alone are common; impact rises when identity pools mint usable temporary AWS credentials through over-permissioned IAM roles. The extract stresses reporting exposure and role over-permission, and not using obtained access beyond authorized proof. Misconfigs often cluster across sibling subdomains. Pattern: On SPA/dev hosts, mine JS and source maps for cloud identity client config; assess whether open signup/auth plus identity pools can mint temporary cloud credentials and what those roles grant—report exposure, stay within authorized proof.
- **Tags:** aws, cognito, js-secrets, sourcemaps, credential-exposure, bug-bounty, misconfiguration
- **Lane:** Deep Research
- **Quality:** ok
- **Sources:**
  - https://medium.com/@mohameddiv77/how-i-got-aws-secret-keys-from-exposed-variables-in-js-file-c67f61039da6
  - https://x.com/i/web/status/2098083417644491166
- **Notes:** [Deep Research:10] High-level misconfiguration/impact only; no credential values or attack procedures.

