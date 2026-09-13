// The three lifecycle URLs Intuit requires alongside the redirect URI.
//
//   /connect     connect / reconnect URL — starts the OAuth flow
//   /disconnect  disconnect URL — where Intuit sends users who unlink the app
//   /launch      launch URL — where users land from the QuickBooks app tile
//
// Public by design. /connect only builds a URL from the client id, which is not
// a secret and is visible in every OAuth request anyway.

const CLIENT_ID = process.env.QBO_CLIENT_ID || '';
const SCOPE = 'com.intuit.quickbooks.accounting';

const STYLE = `
:root{color-scheme:light dark;--bg:#fcfcfb;--card:#fff;--ink:#0b0b0b;--ink2:#52514e;
--muted:#898781;--line:rgba(11,11,11,.12);--accent:#2a78d6}
@media(prefers-color-scheme:dark){:root{--bg:#141414;--card:#1a1a19;--ink:#fff;
--ink2:#c3c2b7;--line:rgba(255,255,255,.12);--accent:#3987e5}}
body{margin:0;background:var(--bg);color:var(--ink);min-height:100vh;display:flex;
align-items:center;justify-content:center;padding:24px;line-height:1.6;
font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;
padding:30px 32px;max-width:560px;width:100%}
h1{font-size:21px;margin:0 0 8px;letter-spacing:-.01em}
p{color:var(--ink2);font-size:14.5px;margin:0 0 16px}
a.btn{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;
padding:10px 18px;border-radius:8px;font-size:14px;font-weight:600}
a{color:var(--accent)}
.small{font-size:12.5px;color:var(--muted);margin-top:20px;padding-top:16px;
border-top:1px solid var(--line)}
`;

const page = (title, body) => `<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>${title}</title>
<style>${STYLE}</style></head><body><div class="card">${body}
<div class="small"><a href="/privacy">Privacy Policy</a> · <a href="/eula">Terms</a></div>
</div></body></html>`;

module.exports = (req, res) => {
  const host = req.headers.host;
  const path = (req.url || '').split('?')[0].replace(/\/+$/, '');
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex, nofollow');

  if (path.includes('connect') && !path.includes('disconnect')) {
    if (!CLIENT_ID) {
      res.statusCode = 500;
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      return res.end(page('Not configured', `<h1>Not configured</h1>
        <p>QBO_CLIENT_ID is not set on this deployment, so the authorization URL
        cannot be built.</p>`));
    }
    const u = new URL('https://appcenter.intuit.com/connect/oauth2');
    u.searchParams.set('client_id', CLIENT_ID);
    u.searchParams.set('redirect_uri', `https://${host}/qbo/callback`);
    u.searchParams.set('response_type', 'code');
    u.searchParams.set('scope', SCOPE);
    u.searchParams.set('state', 'btofin');
    res.statusCode = 302;
    res.setHeader('Location', u.toString());
    return res.end();
  }

  if (path.includes('disconnect')) {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    return res.end(page('Disconnected', `<h1>QuickBooks disconnected</h1>
      <p>This app no longer has access to the QuickBooks company. Stored access
      and refresh tokens for that connection are invalidated and no further
      accounting data will be retrieved.</p>
      <p>Financial reporting will continue using its other data sources, with
      operating-expense figures falling back to configured estimates.</p>
      <p><a class="btn" href="/connect">Reconnect QuickBooks</a></p>`));
  }

  // /launch — Intuit's reviewer visits this, so it must not be a bare 401.
  // Public landing page that explains the app and links into the gated dashboard.
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.end(page('BTO Financials', `<h1>BTO Financials</h1>
    <p>Internal contribution-margin reporting for BTO EC Ventures. It reads our
    QuickBooks accounting records, Shopify orders and advertising spend, and
    reports true profitability after cost of goods, fulfilment, payment fees and
    marketing.</p>
    <p>Access to the reporting dashboard is restricted to authorized staff and
    requires credentials issued by BTO EC Ventures.</p>
    <p><a class="btn" href="/">Open dashboard</a></p>`));
};
