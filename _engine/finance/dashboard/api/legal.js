// Public legal pages required by Intuit's production checklist.
//
// These MUST stay outside the dashboard's Basic Auth: Intuit's review process
// fetches them unauthenticated, and a 401 fails the checklist.
//
// Routed from vercel.json:  /eula  and  /privacy

const COMPANY = 'BTO EC Ventures';
const APP = 'BTO Financials';
const CONTACT = 'btorradre@gmail.com';
const UPDATED = 'August 8, 2026';

const STYLE = `
:root{color-scheme:light dark;--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;
--line:rgba(11,11,11,.12);--accent:#2a78d6}
@media(prefers-color-scheme:dark){:root{--bg:#141414;--ink:#fff;--ink2:#c3c2b7;
--muted:#898781;--line:rgba(255,255,255,.12);--accent:#3987e5}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);line-height:1.65;
font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:760px;margin:0 auto;padding:56px 22px 88px}
h1{font-size:30px;margin:0 0 6px;letter-spacing:-.02em}
h2{font-size:17px;margin:34px 0 10px;letter-spacing:-.01em}
h3{font-size:15px;margin:22px 0 6px;color:var(--ink2)}
p,li{color:var(--ink2);font-size:15px}
li{margin-bottom:7px}
ul{padding-left:22px}
.meta{color:var(--muted);font-size:13.5px;margin:0 0 8px}
.lede{font-size:16px;color:var(--ink2);border-left:3px solid var(--accent);
padding-left:16px;margin:22px 0 30px}
a{color:var(--accent)}
.foot{margin-top:52px;padding-top:20px;border-top:1px solid var(--line);
color:var(--muted);font-size:13px}
.nav{margin-bottom:30px;font-size:13.5px}
.nav a{margin-right:16px}
strong{color:var(--ink)}
`;

function shell(title, body) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title} · ${APP}</title><style>${STYLE}</style></head>
<body><div class="wrap">
<div class="nav"><a href="/privacy">Privacy Policy</a><a href="/eula">Terms of Service</a></div>
${body}
<div class="foot">${COMPANY} · Questions: <a href="mailto:${CONTACT}">${CONTACT}</a></div>
</div></body></html>`;
}

const PRIVACY = shell('Privacy Policy', `
<h1>Privacy Policy</h1>
<p class="meta">Last updated ${UPDATED}</p>

<p class="lede">${APP} is a private, internal financial reporting tool operated by
${COMPANY} for its own staff. It is not offered to the public, has no consumer
users, and no one outside ${COMPANY} can create an account.</p>

<h2>1. Who this covers</h2>
<p>This policy describes how ${COMPANY} ("we", "us") handles information within
${APP} ("the App"). The only people who use the App are employees and contractors
of ${COMPANY} who have been given credentials by us.</p>

<h2>2. What the App accesses</h2>
<p>The App reads business records belonging to ${COMPANY} from systems we already
own or subscribe to, in order to calculate our own profitability. Specifically:</p>
<ul>
  <li><strong>QuickBooks Online</strong> — our own accounting records, read-only.
      This includes profit-and-loss reports and expense account totals for the
      company whose books we connect. We request the accounting scope only.</li>
  <li><strong>Shopify</strong> — our own store's orders, product costs, refunds
      and payment disputes.</li>
  <li><strong>Triple Whale</strong> — our own advertising spend and channel
      performance figures.</li>
</ul>
<p>All of this data is our own company's business and financial information.</p>

<h2>3. What the App does not do</h2>
<ul>
  <li>We do not collect personal information from members of the public.</li>
  <li>We do not sell, rent, license or trade any data, to anyone, for any purpose.</li>
  <li>We do not use QuickBooks data for advertising, profiling, model training,
      or any purpose other than producing our own internal financial reports.</li>
  <li>We do not share QuickBooks data with third parties, other than the hosting
      provider described below that stores it on our behalf.</li>
  <li>The App is read-only against QuickBooks. It does not create, modify or
      delete anything in your accounting records.</li>
</ul>

<h2>4. Customer information</h2>
<p>Order records retrieved from our store may include limited customer details
such as an internal customer identifier and whether an order was a first
purchase. The App uses these solely to count new versus returning orders. It does
not display customer names, email addresses, shipping addresses or payment
details, and it does not build customer profiles.</p>

<h2>5. Where data is stored</h2>
<p>Calculated figures are stored in two places: on company-controlled computers,
and as a static data file deployed to our hosting provider, Vercel Inc., which
serves the dashboard. Access credentials for connected services are stored on
company-controlled machines and are never included in the deployed dashboard.</p>

<h2>6. Who can see it</h2>
<p>The dashboard is protected by authentication and is not publicly readable.
Only authorized ${COMPANY} personnel holding credentials issued by us can view
it. Pages are served with no-index directives and are not listed by search
engines.</p>

<h2>7. How long we keep it</h2>
<p>Calculated daily figures are retained for approximately 90 days in rolling
archives, and the current reporting window is refreshed nightly. Access tokens
are retained only while the connection remains active.</p>

<h2>8. Disconnecting and deletion</h2>
<p>The QuickBooks connection can be revoked at any time from within QuickBooks
Online, or by contacting us. When a connection is revoked, we stop retrieving
data and delete the stored access and refresh tokens. To request deletion of
data already retrieved, email <a href="mailto:${CONTACT}">${CONTACT}</a> and we
will delete it and confirm.</p>

<h2>9. Security</h2>
<p>Connections to all services use encrypted HTTPS. The dashboard requires
authentication and denies access by default if its credentials are not
configured. Credentials and tokens are held in local configuration files
excluded from version control. No production secrets are stored in the deployed
application.</p>

<h2>10. Children</h2>
<p>The App is a business tool and is not directed to, or usable by, anyone under
18.</p>

<h2>11. Changes</h2>
<p>If this policy changes materially we will update this page and revise the date
above.</p>

<h2>12. Contact</h2>
<p>Questions about this policy or about data handled by the App:
<a href="mailto:${CONTACT}">${CONTACT}</a>.</p>
`);

const EULA = shell('Terms of Service', `
<h1>Terms of Service and End User License Agreement</h1>
<p class="meta">Last updated ${UPDATED}</p>

<p class="lede">${APP} is internal software operated by ${COMPANY} for its own
staff. By using it you agree to these terms. If you do not agree, do not use it.</p>

<h2>1. Who may use the App</h2>
<p>${APP} ("the App") is provided by ${COMPANY} solely for use by its employees
and contractors who have been issued credentials. It is not offered, sold or
licensed to the general public. If you have obtained access without authorization
from ${COMPANY}, you have no licence to use the App and must stop immediately.</p>

<h2>2. Licence</h2>
<p>${COMPANY} grants authorized users a limited, revocable, non-exclusive,
non-transferable right to access the App for internal business purposes only, for
as long as their authorization lasts. All rights not expressly granted are
reserved. No ownership is transferred.</p>

<h2>3. What the App does</h2>
<p>The App reads business and accounting records from services ${COMPANY} already
uses, including QuickBooks Online, Shopify and Triple Whale, and presents
calculated profitability reporting. Access to QuickBooks Online is read-only.</p>

<h2>4. Acceptable use</h2>
<p>You agree not to:</p>
<ul>
  <li>share your credentials, or allow anyone else to use your access;</li>
  <li>export, publish or disclose the financial information shown in the App to
      anyone outside ${COMPANY} without written authorization;</li>
  <li>attempt to bypass authentication or access data you are not authorized to see;</li>
  <li>interfere with, overload, reverse engineer or disrupt the App or the
      services it connects to.</li>
</ul>

<h2>5. Accuracy and reliance</h2>
<p>Figures shown in the App are automated calculations that depend on the
completeness and accuracy of data in the connected source systems. Some inputs
are estimates, and the App labels them as such where known. <strong>The App is a
management reporting aid. It is not accounting, tax, audit or investment advice,
and it is not a substitute for reviewed financial statements.</strong> Do not
rely on it for filings or for any legal or regulatory purpose.</p>

<h2>6. Third-party services</h2>
<p>The App connects to services operated by third parties, including Intuit,
Shopify, Triple Whale and Vercel. Your use of those services remains governed by
their own terms. ${COMPANY} is not responsible for their availability, accuracy
or conduct.</p>

<h2>7. Availability</h2>
<p>The App is provided without any guarantee of uptime. ${COMPANY} may modify,
suspend, restrict or discontinue it, in whole or in part, at any time and without
notice.</p>

<h2>8. Termination</h2>
<p>${COMPANY} may suspend or revoke access at any time, for any reason,
including on the end of employment or engagement. On termination your licence
ends and you must stop using the App and destroy any information exported from it.</p>

<h2>9. Disclaimer of warranties</h2>
<p>The App is provided "as is" and "as available", without warranties of any kind,
whether express, implied or statutory, including any implied warranties of
merchantability, fitness for a particular purpose, accuracy and non-infringement,
to the fullest extent permitted by law.</p>

<h2>10. Limitation of liability</h2>
<p>To the fullest extent permitted by law, ${COMPANY} shall not be liable for any
indirect, incidental, special, consequential, exemplary or punitive damages, or
for any loss of profits, revenue, data, goodwill or business, arising out of or
relating to the App or to any decision made in reliance on it, regardless of the
theory of liability and even if advised of the possibility of such damages.</p>

<h2>11. Confidentiality</h2>
<p>All information displayed in the App is confidential information of
${COMPANY}. You must protect it and use it only for authorized internal purposes.
This obligation survives termination of your access.</p>

<h2>12. Changes to these terms</h2>
<p>${COMPANY} may update these terms. Continued use after an update constitutes
acceptance of the revised terms.</p>

<h2>13. Contact</h2>
<p>Questions about these terms: <a href="mailto:${CONTACT}">${CONTACT}</a>.</p>
`);

module.exports = (req, res) => {
  const path = (req.url || '').split('?')[0].replace(/\/+$/, '');
  const isEula = path.includes('eula') || path.includes('terms');
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'public, max-age=300');
  res.end(isEula ? EULA : PRIVACY);
};
