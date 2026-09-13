// Contribution-margin dashboard.
//
// Serves one self-contained page behind HTTP Basic Auth. The snapshot is
// bundled at deploy time by a static require, so there is no runtime fetch and
// no database. run_nightly.py rewrites data.json and redeploys.
//
// Auth FAILS CLOSED: with DASH_USER/DASH_PASS unset the page is never served,
// because the payload is the company's full P&L.

let snapshot;
try {
  snapshot = require('../data.json');
} catch (e) {
  snapshot = null;
}

const C = {
  cogs: { light: '#2a78d6', dark: '#3987e5', label: 'COGS' },
  variable: { light: '#eb6834', dark: '#d95926', label: 'Shipping, fees & chargebacks' },
  ad: { light: '#1baf7a', dark: '#199e70', label: 'Ad spend' },
  fixed: { light: '#4a3aa7', dark: '#9085e9', label: 'Fixed costs' },
  net: { light: '#008300', dark: '#008300', label: 'Net profit' },
};

const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

const usd = (n, d = 0) => (n == null || Number.isNaN(n))
  ? '—'
  : (n < 0 ? '-' : '') + '$' + Math.abs(n).toLocaleString('en-US',
      { minimumFractionDigits: d, maximumFractionDigits: d });

const pct = (n) => (n == null || Number.isNaN(n)) ? '—' : n.toFixed(1) + '%';

function unauthorized(res) {
  res.statusCode = 401;
  res.setHeader('WWW-Authenticate', 'Basic realm="Margin", charset="UTF-8"');
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.end('Authentication required.');
}

function checkAuth(req) {
  // DASH_PUBLIC=true serves the dashboard to anyone with the URL. Set
  // deliberately; unset it (or set anything else) to restore the login.
  if (process.env.DASH_PUBLIC === 'true') return true;
  const user = process.env.DASH_USER;
  const pass = process.env.DASH_PASS;
  if (!user || !pass) return false; // fail closed
  const hdr = req.headers.authorization || '';
  if (!hdr.startsWith('Basic ')) return false;
  let decoded = '';
  try { decoded = Buffer.from(hdr.slice(6), 'base64').toString('utf8'); }
  catch (e) { return false; }
  const i = decoded.indexOf(':');
  if (i < 0) return false;
  const u = decoded.slice(0, i), p = decoded.slice(i + 1);
  // constant-ish time compare
  const eq = (a, b) => {
    if (a.length !== b.length) return false;
    let r = 0;
    for (let k = 0; k < a.length; k++) r |= a.charCodeAt(k) ^ b.charCodeAt(k);
    return r === 0;
  };
  return eq(u, user) && eq(p, pass);
}

// ---------------------------------------------------------------- components

function statTile(label, value, sub, tone) {
  const toneClass = tone ? ` tone-${tone}` : '';
  return `<div class="tile${toneClass}">
    <div class="tile-label">${esc(label)}</div>
    <div class="tile-value">${esc(value)}</div>
    ${sub ? `<div class="tile-sub">${esc(sub)}</div>` : ''}
  </div>`;
}

/** 100% stacked horizontal bar: where every dollar of net revenue goes. */
function compositionBar(t) {
  const nr = t.net_revenue || 0;
  if (nr <= 0) return '<p class="empty">No revenue in range.</p>';
  const c = t.costs;
  const segs = [
    { k: 'cogs', v: c.cogs },
    { k: 'variable', v: (c.shipping || 0) + (c.payment_fees || 0) + (c.chargebacks || 0) },
    { k: 'ad', v: c.ad_spend },
    { k: 'fixed', v: c.fixed },
    { k: 'net', v: t.ladder.net },
  ].filter((s) => s.v > 0);
  const total = segs.reduce((a, s) => a + s.v, 0) || 1;

  let x = 0;
  const rects = segs.map((s) => {
    const w = (s.v / total) * 100;
    const r = `<div class="seg" style="width:${w}%;background:var(--c-${s.k})"
        title="${esc(C[s.k].label)}: ${esc(usd(s.v))}"></div>`;
    x += w;
    return r;
  }).join('');

  const legend = segs.map((s) => `<div class="lg">
      <span class="sw" style="background:var(--c-${s.k})"></span>
      <span class="lg-label">${esc(C[s.k].label)}</span>
      <span class="lg-val">${esc(usd(s.v))}</span>
      <span class="lg-pct">${((s.v / total) * 100).toFixed(1)}%</span>
    </div>`).join('');

  const negative = t.ladder.net < 0
    ? `<p class="warn-inline">Net profit is negative (${esc(usd(t.ladder.net))}); it is omitted from the bar above.</p>`
    : '';

  return `<div class="compbar">${rects}</div><div class="legend">${legend}</div>${negative}`;
}

/** The ladder, as descending rows with the deduction that caused each drop. */
function ladderRows(t) {
  const c = t.costs;
  const nr = t.net_revenue;
  const steps = [
    ['Net revenue', nr, null, null],
    ['− COGS', -c.cogs, 'CM1', t.ladder.cm1, t.ladder.cm1_pct],
    ['− Shipping, fees, chargebacks',
      -((c.shipping || 0) + (c.payment_fees || 0) + (c.chargebacks || 0)),
      'CM2', t.ladder.cm2, t.ladder.cm2_pct],
    ['− Ad spend', -c.ad_spend, 'CM3', t.ladder.cm3, t.ladder.cm3_pct],
    ['− Fixed costs (amortized)', -c.fixed, 'Net profit', t.ladder.net, t.ladder.net_pct],
  ];
  return `<table class="ladder">
    <thead><tr><th>Step</th><th class="num">Amount</th><th>Result</th>
      <th class="num">Value</th><th class="num">% of net rev</th></tr></thead>
    <tbody>${steps.map((s, i) => {
      const [label, amt, resName, resVal, resPct] = s;
      const neg = amt < 0;
      return `<tr${i === steps.length - 1 ? ' class="final"' : ''}>
        <td>${esc(label)}</td>
        <td class="num ${neg ? 'neg' : ''}">${esc(usd(amt))}</td>
        <td class="res">${esc(resName || '')}</td>
        <td class="num strong">${resName ? esc(usd(resVal)) : ''}</td>
        <td class="num">${resName ? esc(pct(resPct)) : ''}</td>
      </tr>`;
    }).join('')}</tbody></table>`;
}

/** Daily stacked cost bars with a net-revenue reference line. One axis: dollars. */
function dailyChart(rows) {
  const data = rows.filter((r) => r.net_revenue > 0 || r.costs.ad_spend > 0);
  if (!data.length) return '<p class="empty">No daily data in range.</p>';

  const W = 1000, H = 320, PADL = 64, PADR = 16, PADT = 16, PADB = 42;
  const iw = W - PADL - PADR, ih = H - PADT - PADB;

  const stackOf = (r) => [
    r.costs.cogs,
    (r.costs.shipping || 0) + (r.costs.payment_fees || 0) + (r.costs.chargebacks || 0),
    r.costs.ad_spend,
    r.costs.fixed,
  ];
  const maxCost = Math.max(...data.map((r) => stackOf(r).reduce((a, b) => a + b, 0)));
  const maxRev = Math.max(...data.map((r) => r.net_revenue));
  const max = Math.max(maxCost, maxRev) * 1.08 || 1;

  const bw = Math.max(2, (iw / data.length) * 0.62);
  const step = iw / data.length;
  const x = (i) => PADL + step * i + (step - bw) / 2;
  const y = (v) => PADT + ih - (v / max) * ih;

  const keys = ['cogs', 'variable', 'ad', 'fixed'];
  let bars = '';
  data.forEach((r, i) => {
    const vals = stackOf(r);
    let acc = 0;
    vals.forEach((v, k) => {
      if (v <= 0) return;
      const y0 = y(acc + v), y1 = y(acc);
      const h = Math.max(0, y1 - y0 - 2); // 2px surface gap between segments
      bars += `<rect x="${x(i).toFixed(1)}" y="${y0.toFixed(1)}" width="${bw.toFixed(1)}"
        height="${h.toFixed(1)}" rx="1.5" fill="var(--c-${keys[k]})"><title>${esc(r.date)} — ${esc(C[keys[k]].label)}: ${esc(usd(v))}</title></rect>`;
      acc += v;
    });
  });

  const pts = data.map((r, i) => `${(x(i) + bw / 2).toFixed(1)},${y(r.net_revenue).toFixed(1)}`).join(' ');
  const dots = data.map((r, i) => `<circle cx="${(x(i) + bw / 2).toFixed(1)}"
      cy="${y(r.net_revenue).toFixed(1)}" r="3" fill="var(--text-primary)"><title>${esc(r.date)} — net revenue ${esc(usd(r.net_revenue))}</title></circle>`).join('');

  const ticks = 4;
  let grid = '';
  for (let i = 0; i <= ticks; i++) {
    const v = (max / ticks) * i, yy = y(v);
    grid += `<line x1="${PADL}" x2="${W - PADR}" y1="${yy.toFixed(1)}" y2="${yy.toFixed(1)}"
      stroke="var(--grid)" stroke-width="1"/>
      <text x="${PADL - 10}" y="${(yy + 4).toFixed(1)}" class="axis" text-anchor="end">${esc(usd(v))}</text>`;
  }

  const every = Math.max(1, Math.ceil(data.length / 12));
  const xlabels = data.map((r, i) => (i % every === 0)
    ? `<text x="${(x(i) + bw / 2).toFixed(1)}" y="${H - PADB + 18}" class="axis" text-anchor="middle">${esc(r.date.slice(5))}</text>`
    : '').join('');

  return `<svg viewBox="0 0 ${W} ${H}" class="chart" role="img"
    aria-label="Daily cost composition with net revenue reference line">
    ${grid}${bars}
    <polyline points="${pts}" fill="none" stroke="var(--text-primary)" stroke-width="2"
      stroke-linejoin="round" stroke-linecap="round"/>
    ${dots}${xlabels}
  </svg>
  <div class="legend">
    ${keys.map((k) => `<div class="lg"><span class="sw" style="background:var(--c-${k})"></span><span class="lg-label">${esc(C[k].label)}</span></div>`).join('')}
    <div class="lg"><span class="sw line"></span><span class="lg-label">Net revenue</span></div>
  </div>`;
}

function channelTable(channels) {
  const rows = Object.entries(channels || {});
  if (!rows.length) return '<p class="empty">No channel spend in range.</p>';
  return `<table class="grid"><thead><tr>
      <th>Channel</th><th class="num">Spend</th><th class="num">Impressions</th>
      <th class="num">Clicks</th><th class="num">Reported revenue</th><th class="num">ROAS</th>
    </tr></thead><tbody>${rows.map(([k, v]) => `<tr>
      <td>${esc(k)}</td>
      <td class="num">${esc(usd(v.spend))}</td>
      <td class="num">${v.impressions.toLocaleString('en-US')}</td>
      <td class="num">${v.clicks.toLocaleString('en-US')}</td>
      <td class="num">${esc(usd(v.reported_revenue))}</td>
      <td class="num strong">${v.roas == null ? '—' : v.roas.toFixed(2)}</td>
    </tr>`).join('')}</tbody></table>`;
}

function dailyTable(rows) {
  return `<table class="grid tight"><thead><tr>
      <th>Date</th><th class="num">Orders</th><th class="num">Net rev</th>
      <th class="num">COGS</th><th class="num">Fees+CB</th><th class="num">Ad spend</th>
      <th class="num">Fixed</th><th class="num">CM1</th><th class="num">CM3</th>
      <th class="num">Net</th><th class="num">Net %</th>
    </tr></thead><tbody>${rows.slice().reverse().map((r) => `<tr>
      <td>${esc(r.date)}</td>
      <td class="num">${r.orders}</td>
      <td class="num">${esc(usd(r.net_revenue))}</td>
      <td class="num">${esc(usd(r.costs.cogs))}</td>
      <td class="num">${esc(usd((r.costs.shipping || 0) + (r.costs.payment_fees || 0) + (r.costs.chargebacks || 0)))}</td>
      <td class="num">${esc(usd(r.costs.ad_spend))}</td>
      <td class="num">${esc(usd(r.costs.fixed))}</td>
      <td class="num">${esc(usd(r.ladder.cm1))}</td>
      <td class="num">${esc(usd(r.ladder.cm3))}</td>
      <td class="num ${r.ladder.net < 0 ? 'neg' : ''}">${esc(usd(r.ladder.net))}</td>
      <td class="num">${esc(pct(r.ladder.net_pct))}</td>
    </tr>`).join('')}</tbody></table>`;
}

function qualityPanel(snap, brand, rows) {
  const items = [];
  const totalUnits = rows.reduce((a, r) => a + (r.data_quality.units_costed + r.data_quality.units_uncosted), 0);
  const costed = rows.reduce((a, r) => a + r.data_quality.units_costed, 0);
  const uncostedRev = rows.reduce((a, r) => a + r.data_quality.uncosted_revenue, 0);
  const cov = totalUnits ? (costed / totalUnits) * 100 : null;

  if (cov != null && cov < 99.5) {
    items.push({
      tone: cov < 90 ? 'critical' : 'warning',
      title: `COGS coverage ${cov.toFixed(1)}%`,
      body: `${esc(usd(uncostedRev))} of revenue has no unit cost set in Shopify, so CM1 and everything below it are overstated. Set "Cost per item" on the products below.`,
    });
  }
  if (snap.config && snap.config.shipping_configured && snap.config.shipping_configured[brand] === false) {
    items.push({
      tone: 'warning',
      title: 'Shipping cost not configured',
      body: 'Triple Whale reports $0 shipping and Shopify carries 0g weights, so no shipping cost is being subtracted. Set shipping_cost_per_order_usd in costs.json.',
    });
  }
  if (snap.quickbooks && !snap.quickbooks.available) {
    items.push({
      tone: 'warning',
      title: 'QuickBooks not connected',
      body: `Fixed costs are estimates from the historical P&L, not live QuickBooks actuals. ${esc(snap.quickbooks.reason || '')}`,
    });
  }
  (snap.errors || []).forEach((e) => items.push({
    tone: 'critical', title: `${e.brand} / ${e.source} failed`, body: e.error,
  }));

  if (!items.length) {
    items.push({ tone: 'good', title: 'All sources healthy', body: 'Every cost line was measured, not estimated.' });
  }

  const gaps = (snap.cost_gaps && snap.cost_gaps[brand]) || [];
  const gapTable = gaps.length ? `<table class="grid"><thead><tr>
      <th>Product with no cost set</th><th class="num">Units</th><th class="num">Uncosted revenue</th>
    </tr></thead><tbody>${gaps.map((g) => `<tr>
      <td>${esc(g.product)}</td><td class="num">${g.units}</td>
      <td class="num">${esc(usd(g.revenue))}</td></tr>`).join('')}</tbody></table>` : '';

  return items.map((i) => `<div class="note tone-${i.tone}">
      <div class="note-title">${esc(i.title)}</div>
      <div class="note-body">${esc(i.body)}</div>
    </div>`).join('') + gapTable;
}

// -------------------------------------------------------------------- render

function page(snap) {
  if (!snap) {
    return `<main class="wrap"><h1>No data yet</h1>
      <p class="empty">Run <code>python3 _engine/finance/run_nightly.py</code> to generate the first snapshot.</p></main>`;
  }
  const brand = snap.brands[0];
  const rows = snap.series[brand] || [];
  const t30 = snap.totals[brand].last_30;
  const t7 = snap.totals[brand].last_7;
  const tr = snap.totals[brand].range;
  const gen = new Date(snap.generated_at);

  const tiles = [
    statTile('Net revenue', usd(t30.net_revenue), 'last 30 days'),
    statTile('Net profit', usd(t30.ladder.net),
      `${pct(t30.ladder.net_pct)} margin`, t30.ladder.net < 0 ? 'critical' : 'good'),
    statTile('CM1 (after COGS)', pct(t30.ladder.cm1_pct), usd(t30.ladder.cm1)),
    statTile('CM3 (after ads)', pct(t30.ladder.cm3_pct), usd(t30.ladder.cm3)),
    statTile('MER', t30.efficiency.mer == null ? '—' : t30.efficiency.mer.toFixed(2),
      'net revenue ÷ ad spend'),
    statTile('CAC', usd(t30.efficiency.cac, 2), 'per new customer'),
    statTile('AOV', usd(t30.efficiency.aov, 2), `${t30.orders} orders`),
    statTile('Ad spend', usd(t30.costs.ad_spend), `${pct(t30.efficiency.ad_spend_pct)} of net rev`),
  ].join('');

  const tiles7 = [
    statTile('Net revenue', usd(t7.net_revenue), 'last 7 days'),
    statTile('Net profit', usd(t7.ladder.net), pct(t7.ladder.net_pct),
      t7.ladder.net < 0 ? 'critical' : 'good'),
    statTile('MER', t7.efficiency.mer == null ? '—' : t7.efficiency.mer.toFixed(2), ''),
    statTile('CAC', usd(t7.efficiency.cac, 2), ''),
  ].join('');

  return `<main class="wrap">
    <header class="head">
      <div>
        <h1>${esc(brand)} · Contribution Margin</h1>
        <p class="sub">${esc(snap.range.start)} to ${esc(snap.range.end)} ·
          updated ${esc(gen.toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' }))}</p>
      </div>
    </header>

    <section>
      <h2>Last 30 days</h2>
      <div class="tiles">${tiles}</div>
    </section>

    <section>
      <h2>Last 7 days</h2>
      <div class="tiles four">${tiles7}</div>
    </section>

    <section>
      <h2>Where every dollar goes <span class="h-sub">last 30 days</span></h2>
      ${compositionBar(t30)}
    </section>

    <section>
      <h2>The margin ladder <span class="h-sub">last 30 days</span></h2>
      ${ladderRows(t30)}
    </section>

    <section>
      <h2>Daily costs vs net revenue</h2>
      ${dailyChart(rows)}
    </section>

    <section>
      <h2>Channels <span class="h-sub">${esc(snap.range.start)} to ${esc(snap.range.end)}</span></h2>
      ${channelTable(snap.channels)}
    </section>

    <section>
      <h2>Data quality</h2>
      ${qualityPanel(snap, brand, rows)}
    </section>

    <section>
      <h2>Daily detail</h2>
      <div class="scroll">${dailyTable(rows)}</div>
    </section>

    <footer class="foot">
      COGS is scraped per order from Shopify. Ad spend, payment fees and channel
      data come from Triple Whale. Chargebacks come from Shopify Payments disputes.
      Fixed costs are ${snap.quickbooks && snap.quickbooks.available ? 'live QuickBooks actuals' : 'monthly estimates'}
      amortized to a daily rate. Range totals: ${esc(usd(tr.net_revenue))} net revenue,
      ${esc(usd(tr.ladder.net))} net profit.
    </footer>
  </main>`;
}

const STYLE = `
:root{color-scheme:dark;--surface:#141414;--panel:#1a1a19;--text-primary:#fff;
--text-secondary:#c3c2b7;--muted:#898781;--grid:#2c2c2a;--border:rgba(255,255,255,.10);
--c-cogs:#3987e5;--c-variable:#d95926;--c-ad:#199e70;--c-fixed:#9085e9;--c-net:#008300;
--good:#0ca30c;--warning:#fab219;--critical:#d03b3b}
@media (prefers-color-scheme:light){:root:where(:not([data-theme="dark"])){
color-scheme:light;--surface:#f9f9f7;--panel:#fcfcfb;--text-primary:#0b0b0b;
--text-secondary:#52514e;--muted:#898781;--grid:#e1e0d9;--border:rgba(11,11,11,.10);
--c-cogs:#2a78d6;--c-variable:#eb6834;--c-ad:#1baf7a;--c-fixed:#4a3aa7;--c-net:#008300}}
:root[data-theme="light"]{color-scheme:light;--surface:#f9f9f7;--panel:#fcfcfb;
--text-primary:#0b0b0b;--text-secondary:#52514e;--grid:#e1e0d9;--border:rgba(11,11,11,.10);
--c-cogs:#2a78d6;--c-variable:#eb6834;--c-ad:#1baf7a;--c-fixed:#4a3aa7}
*{box-sizing:border-box}
body{margin:0;background:var(--surface);color:var(--text-primary);
font-family:system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.5}
.wrap{max-width:1200px;margin:0 auto;padding:32px 20px 64px}
.head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;
margin-bottom:8px}
h1{font-size:26px;margin:0 0 4px;letter-spacing:-.01em}
h2{font-size:15px;margin:0 0 12px;font-weight:600;color:var(--text-secondary);
text-transform:uppercase;letter-spacing:.06em}
.h-sub{text-transform:none;letter-spacing:0;color:var(--muted);font-weight:400}
.sub{margin:0;color:var(--muted);font-size:13px}
section{margin-top:34px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}
.tiles.four{grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.tile{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:14px 16px}
.tile-label{font-size:12px;color:var(--muted);margin-bottom:6px}
.tile-value{font-size:26px;font-weight:600;letter-spacing:-.02em}
.tile-sub{font-size:12px;color:var(--text-secondary);margin-top:4px}
.tile.tone-good .tile-value{color:var(--good)}
.tile.tone-critical .tile-value{color:var(--critical)}
.compbar{display:flex;width:100%;height:44px;border-radius:8px;overflow:hidden;gap:2px;
background:var(--surface)}
.seg{height:100%}
.legend{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:14px}
.lg{display:flex;align-items:center;gap:8px;font-size:13px}
.sw{width:12px;height:12px;border-radius:3px;flex:0 0 auto}
.sw.line{height:3px;border-radius:2px;background:var(--text-primary)}
.lg-label{color:var(--text-secondary)}
.lg-val{font-weight:600;font-variant-numeric:tabular-nums}
.lg-pct{color:var(--muted);font-variant-numeric:tabular-nums}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{padding:9px 10px;text-align:left;border-bottom:1px solid var(--border)}
th{font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);
font-weight:600}
.num{text-align:right;font-variant-numeric:tabular-nums}
.strong{font-weight:600}
.neg{color:var(--critical)}
.ladder .res{color:var(--text-secondary);font-weight:600}
.ladder tr.final td{border-top:1px solid var(--border);font-size:14.5px}
.grid.tight th,.grid.tight td{padding:7px 9px;font-size:12.5px}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
.chart{width:100%;height:auto;display:block;background:var(--panel);
border:1px solid var(--border);border-radius:10px;padding:8px}
.axis{fill:var(--muted);font-size:11px;font-family:inherit;
font-variant-numeric:tabular-nums}
.note{background:var(--panel);border:1px solid var(--border);border-left-width:3px;
border-radius:8px;padding:12px 14px;margin-bottom:10px}
.note-title{font-weight:600;font-size:14px;margin-bottom:3px}
.note-body{font-size:13px;color:var(--text-secondary)}
.note.tone-good{border-left-color:var(--good)}
.note.tone-warning{border-left-color:var(--warning)}
.note.tone-critical{border-left-color:var(--critical)}
.warn-inline{color:var(--critical);font-size:13px;margin:10px 0 0}
.empty{color:var(--muted);font-size:14px}
.foot{margin-top:44px;padding-top:18px;border-top:1px solid var(--border);
color:var(--muted);font-size:12.5px;max-width:78ch}
code{background:var(--panel);padding:2px 5px;border-radius:4px;font-size:12px}
@media(max-width:640px){.wrap{padding:20px 14px 48px}h1{font-size:21px}
.tile-value{font-size:22px}}
`;

module.exports = (req, res) => {
  if (!checkAuth(req)) return unauthorized(res);
  const html = `<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Contribution Margin</title><style>${STYLE}</style></head>
<body>${page(snapshot)}</body></html>`;
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex, nofollow');
  res.end(html);
};
