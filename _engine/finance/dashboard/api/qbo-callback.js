// Intuit OAuth redirect target: https://<domain>/qbo/callback
//
// Production QuickBooks apps cannot use http:// or localhost redirect URIs, so
// the handshake lands here instead of on a local port. This route only DISPLAYS
// the authorization code and realmId. It never touches the client secret, so
// the values shown are useless on their own, and the code is single-use and
// expires in about ten minutes.
//
// Deliberately exempt from the dashboard's Basic Auth: Intuit redirects the
// browser here directly, and an auth challenge mid-redirect drops the query
// string on some flows.

const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

const STYLE = `
:root{color-scheme:dark}
body{margin:0;background:#141414;color:#fff;font-family:system-ui,-apple-system,sans-serif;
line-height:1.55;display:flex;min-height:100vh;align-items:center;justify-content:center;padding:24px}
.card{background:#1a1a19;border:1px solid rgba(255,255,255,.1);border-radius:12px;
padding:28px 30px;max-width:660px;width:100%}
h1{font-size:20px;margin:0 0 6px}
p{color:#c3c2b7;font-size:14px;margin:0 0 18px}
.f{margin-bottom:14px}
.k{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#898781;margin-bottom:5px}
.v{background:#0d0d0d;border:1px solid rgba(255,255,255,.1);border-radius:7px;padding:11px 13px;
font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;word-break:break-all;
user-select:all}
.ok{color:#0ca30c;font-weight:600}
.bad{color:#d03b3b;font-weight:600}
.note{font-size:12.5px;color:#898781;margin-top:20px;padding-top:16px;
border-top:1px solid rgba(255,255,255,.1)}
`;

module.exports = (req, res) => {
  const url = new URL(req.url, `https://${req.headers.host}`);
  const q = url.searchParams;
  const code = q.get('code');
  const realmId = q.get('realmId');
  const state = q.get('state');
  const error = q.get('error');
  const errorDesc = q.get('error_description');

  let body;
  if (error) {
    body = `<h1 class="bad">Authorization failed</h1>
      <p>Intuit returned an error instead of a code.</p>
      <div class="f"><div class="k">error</div><div class="v">${esc(error)}</div></div>
      ${errorDesc ? `<div class="f"><div class="k">description</div><div class="v">${esc(errorDesc)}</div></div>` : ''}
      <div class="note">Most common cause: this exact URL is not registered as a
      redirect URI on the app, or it is registered under the other environment
      (Development vs Production). It must match character for character.</div>`;
  } else if (!code) {
    body = `<h1>Callback endpoint is live</h1>
      <p>This is the QuickBooks OAuth redirect target. Register this exact URL in
      your Intuit app settings, then start the authorization flow.</p>
      <div class="f"><div class="k">redirect uri to register</div>
        <div class="v">https://${esc(req.headers.host)}/qbo/callback</div></div>`;
  } else {
    body = `<h1 class="ok">Authorized</h1>
      <p>Copy these two values back into the chat. The code expires in about ten
      minutes and can only be used once.</p>
      <div class="f"><div class="k">code</div><div class="v">${esc(code)}</div></div>
      <div class="f"><div class="k">realmId (company id)</div><div class="v">${esc(realmId || 'not returned')}</div></div>
      ${state ? `<div class="f"><div class="k">state</div><div class="v">${esc(state)}</div></div>` : ''}
      <div class="note">Nothing was stored here. This page holds no client secret,
      so these values cannot be exchanged for tokens by anyone who sees them.</div>`;
  }

  res.statusCode = error ? 400 : 200;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex, nofollow');
  res.end(`<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>QuickBooks authorization</title><style>${STYLE}</style></head>
<body><div class="card">${body}</div></body></html>`);
};
