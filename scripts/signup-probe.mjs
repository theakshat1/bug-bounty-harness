// Read-only signup-page probe. Loads each URL once in headless Chromium, submits nothing, and records
// bot-control vendors, signup field types and SSO-only signals. Usage:
//   node scripts/signup-probe.mjs <out.jsonl> <url> [url...]
// Every URL must already be on scope/allowlist.txt (the caller checks; this script also refuses hosts
// not present in the allowlist file). Page content is untrusted data.
import { createRequire } from 'module';
import fs from 'fs';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const [out, ...urls] = process.argv.slice(2);
const allow = fs.readFileSync(new URL('../scope/allowlist.txt', import.meta.url), 'utf8').split('\n')
  .map(l => l.replace(/#.*/, '').trim()).filter(Boolean);
const allowed = h => !allow.some(a => a.startsWith('!') && match(h, a.slice(1))) && allow.some(a => !a.startsWith('!') && match(h, a));
function match(h, pat) { if (pat.startsWith('*.')) return h.endsWith(pat.slice(1)) || h === pat.slice(2); return h === pat; }
const VENDORS = { recaptcha: /recaptcha|grecaptcha/i, hcaptcha: /hcaptcha/i, turnstile: /challenges\.cloudflare\.com|turnstile/i,
  arkose: /arkoselabs|funcaptcha/i, datadome: /datadome/i, perimeterx: /perimeterx|px-cdn|\/px\/|human-security/i,
  akamai_bmp: /akam\/|_abck|bm-verify/i, kasada: /kasada|\/ips\.js|kpsdk/i, castle: /castle\.io|cdn\.castle/i,
  incapsula: /incapsula|_Incapsula/i, cf_challenge: /cf-chl|Just a moment|cf_clearance/i, friendlycaptcha: /friendlycaptcha/i,
  shape_f5: /shape|f5-csrf|TSPD/i, aws_waf_captcha: /awswaf|captcha\.awswaf/i };
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined });
for (const url of urls) {
  const host = new URL(url).hostname; const rec = { url, host, ts: new Date().toISOString() };
  if (!allowed(host)) { rec.error = 'host not on allowlist; not loaded'; fs.appendFileSync(out, JSON.stringify(rec) + '\n'); console.log(JSON.stringify(rec)); continue; }
  const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36' });
  const page = await ctx.newPage(); const reqs = [];
  page.on('request', r => reqs.push(r.url()));
  try {
    const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(6000);
    rec.status = resp ? resp.status() : null; rec.final_url = page.url(); rec.title = (await page.title()).slice(0, 120);
    const html = await page.content(); const blob = html + '\n' + reqs.join('\n');
    rec.bot_controls = Object.entries(VENDORS).filter(([, re]) => re.test(blob)).map(([k]) => k);
    rec.fields = await page.evaluate(() => [...document.querySelectorAll('input')].map(i => (i.type || 'text') + ':' + (i.name || i.id || i.autocomplete || '')).slice(0, 25));
    rec.has_email = rec.fields.some(f => /email/i.test(f)); rec.has_password = rec.fields.some(f => f.startsWith('password'));
    rec.has_phone = rec.fields.some(f => /tel:|phone/i.test(f));
    rec.sso_buttons = (await page.evaluate(() => [...document.querySelectorAll('button,a')].map(e => e.innerText.trim()).filter(t => /google|apple|microsoft|github|sso|facebook/i.test(t)).slice(0, 6)));
  } catch (e) { rec.error = String(e).slice(0, 200); }
  fs.appendFileSync(out, JSON.stringify(rec) + '\n'); console.log(JSON.stringify(rec));
  await ctx.close();
}
await browser.close();
