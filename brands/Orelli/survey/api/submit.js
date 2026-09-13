// Orelli WTP survey intake — writes each submission as a row in the Notion
// responses database. Select option names are kept comma-free (Notion selects
// reject commas), so answers map by index to these canonical names.
const LABELS = {
  gender: ['Female', 'Male', 'Prefer not to say'],
  age: ['18-24', '25-34', '35-44', '45-54', '55+'],
  q1: ['Every single time', 'Certain pills only', 'Big pills only'],
  q2: ['Definitely', 'If it tastes decent'],
  q4: ['Definitely (2-3 bottles)', 'Very likely', 'Reviews first', 'Not at that price']
};
// payload key stays "q4" (legacy in-flight sessions) but the Notion column is
// numbered Q3 — it is the third question since the old fair-price Q3 was retired
const PROP = { gender: 'Gender', age: 'Age', q1: 'Q1 Pill Struggle', q2: 'Q2 Keep In Cabinet', q4: 'Q3 At $29.99' };

// Google Sheets mirror ("Orelli Emails" sheet) — completed submissions only.
// Auth via OAuth refresh token (btorradre@btoecventures.com). Access token is
// cached across warm invocations; failures never block the Notion write.
let gToken = null; // { token, exp }
async function sheetsAccessToken() {
  if (gToken && Date.now() < gToken.exp - 60000) return gToken.token;
  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: process.env.GOOGLE_CLIENT_ID,
      client_secret: process.env.GOOGLE_CLIENT_SECRET,
      refresh_token: process.env.GOOGLE_REFRESH_TOKEN,
      grant_type: 'refresh_token'
    })
  });
  if (!r.ok) throw new Error(`google token ${r.status}: ${(await r.text()).slice(0, 200)}`);
  const j = await r.json();
  gToken = { token: j.access_token, exp: Date.now() + (j.expires_in || 3600) * 1000 };
  return gToken.token;
}

async function appendToSheet(row) {
  if (!process.env.GOOGLE_REFRESH_TOKEN || !process.env.SHEET_ID) return;
  const token = await sheetsAccessToken();
  const r = await fetch(
    `https://sheets.googleapis.com/v4/spreadsheets/${process.env.SHEET_ID}/values/A:J:append?valueInputOption=RAW&insertDataOption=INSERT_ROWS`,
    {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ values: [row] })
    }
  );
  if (!r.ok) throw new Error(`sheets append ${r.status}: ${(await r.text()).slice(0, 300)}`);
}

// "Orelli — Emails" Notion DB — the email-list duplicate of the sheet.
// Dedupes by email (title property) so repeat submissions don't double-list.
async function appendToEmailsDb(email, ts, creator, answerLabels, src) {
  if (!process.env.NOTION_EMAILS_DB_ID) return;
  const headers = {
    Authorization: `Bearer ${process.env.NOTION_TOKEN}`,
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
  };
  const byEmail = () => fetch(`https://api.notion.com/v1/databases/${process.env.NOTION_EMAILS_DB_ID}/query`, {
    method: 'POST', headers,
    body: JSON.stringify({ page_size: 5, filter: { property: 'Email', title: { equals: email } } })
  }).then(r => r.ok ? r.json() : { results: [] }).then(j => j.results);
  if ((await byEmail()).length) return;

  const props = {
    Email: { title: [{ text: { content: email } }] },
    Timestamp: { date: { start: ts } }
  };
  if (creator) props.Creator = { rich_text: [{ text: { content: creator } }] };
  if (src) props.Source = { rich_text: [{ text: { content: src } }] };
  for (const q of Object.keys(PROP)) {
    if (answerLabels[q]) props[PROP[q]] = { select: { name: answerLabels[q] } };
  }
  const r = await fetch('https://api.notion.com/v1/pages', {
    method: 'POST', headers,
    body: JSON.stringify({ parent: { database_id: process.env.NOTION_EMAILS_DB_ID }, properties: props })
  });
  if (!r.ok) throw new Error(`emails db ${r.status}: ${(await r.text()).slice(0, 300)}`);

  // self-heal concurrent double-creates of the same email: keep the oldest
  const dups = await byEmail();
  if (dups.length > 1) {
    const sorted = dups.slice().sort((a, b) =>
      (a.created_time + a.id < b.created_time + b.id ? -1 : 1));
    for (const loser of sorted.slice(1)) {
      await fetch(`https://api.notion.com/v1/pages/${loser.id}`, {
        method: 'PATCH', headers, body: JSON.stringify({ archived: true })
      });
    }
  }
}

// "Orelli — Quiz Answers" Notion DB — one row per session, upserted so a
// partial upgrades in place to complete instead of adding a second row.
async function upsertAnswersDb(session, status, email, creator, answerLabels, src) {
  if (!process.env.NOTION_ANSWERS_DB_ID || !session) return;
  const headers = {
    Authorization: `Bearer ${process.env.NOTION_TOKEN}`,
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
  };
  const props = {
    Session: { title: [{ text: { content: session } }] },
    Status: { select: { name: status } },
    'Last Updated': { date: { start: new Date().toISOString() } }
  };
  if (email) props.Email = { email };
  if (creator) props.Creator = { rich_text: [{ text: { content: creator } }] };
  if (src) props.Source = { rich_text: [{ text: { content: src } }] };
  for (const q of Object.keys(PROP)) {
    if (answerLabels[q]) props[PROP[q]] = { select: { name: answerLabels[q] } };
  }

  const bySession = () => fetch(`https://api.notion.com/v1/databases/${process.env.NOTION_ANSWERS_DB_ID}/query`, {
    method: 'POST', headers,
    body: JSON.stringify({ page_size: 5, filter: { property: 'Session', title: { equals: session } } })
  }).then(r => r.ok ? r.json() : { results: [] }).then(j => j.results);

  const existing = (await bySession())[0];
  if (existing) {
    // never downgrade: a late partial beacon must not overwrite a Complete row
    const exStatus = (existing.properties.Status.select || {}).name;
    if (exStatus === 'Complete' && status !== 'Complete') return;
    const r = await fetch(`https://api.notion.com/v1/pages/${existing.id}`, {
      method: 'PATCH', headers, body: JSON.stringify({ properties: props })
    });
    if (!r.ok) throw new Error(`answers db ${r.status}: ${(await r.text()).slice(0, 300)}`);
    return;
  }

  const r = await fetch('https://api.notion.com/v1/pages', {
    method: 'POST', headers,
    body: JSON.stringify({ parent: { database_id: process.env.NOTION_ANSWERS_DB_ID }, properties: props })
  });
  if (!r.ok) throw new Error(`answers db ${r.status}: ${(await r.text()).slice(0, 300)}`);

  // self-heal: two simultaneous first-submissions for one session can both pass
  // the lookup and both create. Re-check and archive all but one deterministic
  // survivor (Complete beats Partial, then oldest, then smallest id) — both
  // racers converge on the same winner, and double-archiving is idempotent.
  const dups = await bySession();
  if (dups.length > 1) {
    const rank = p => [
      (p.properties.Status.select || {}).name === 'Complete' ? 0 : 1,
      p.created_time, p.id
    ];
    const sorted = dups.slice().sort((a, b) => (rank(a) < rank(b) ? -1 : 1));
    for (const loser of sorted.slice(1)) {
      await fetch(`https://api.notion.com/v1/pages/${loser.id}`, {
        method: 'PATCH', headers, body: JSON.stringify({ archived: true })
      });
    }
  }
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ ok: false });

  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch { b = null; } }
  if (!b || typeof b !== 'object') return res.status(400).json({ ok: false });

  const status = b.status === 'complete' ? 'Complete' : 'Partial';
  const emailRaw = typeof b.email === 'string' ? b.email.trim().slice(0, 120) : '';
  const email = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(emailRaw) ? emailRaw : '';
  const session = String(b.session || '').slice(0, 64);

  const props = {
    Respondent: { title: [{ text: { content: email || `anon-${session.slice(0, 8) || 'unknown'}` } }] },
    Status: { select: { name: status } },
    Submitted: { date: { start: new Date().toISOString() } },
    Session: { rich_text: [{ text: { content: session } }] }
  };
  if (email) props.Email = { email };

  const a = (b.answers && typeof b.answers === 'object') ? b.answers : {};
  const answerLabels = {};
  for (const q of Object.keys(PROP)) {
    const v = a[q];
    const i = v && Number.isInteger(v.i) ? v.i : -1;
    if (i >= 0 && i < LABELS[q].length) {
      answerLabels[q] = LABELS[q][i];
      props[PROP[q]] = { select: { name: LABELS[q][i] } };
    }
  }

  const creator = String(b.creator || '').slice(0, 80);
  if (creator) props.Creator = { rich_text: [{ text: { content: creator } }] };
  const src = [String(b.source || ''), String(b.referrer || '')].filter(Boolean).join(' | ').slice(0, 400);
  if (src) props.Source = { rich_text: [{ text: { content: src } }] };

  // Mirrors run alongside the primary Notion responses write but never decide
  // the response. Completed submissions with an email only.
  const ts = new Date().toISOString();
  const mirrorJobs = [
    upsertAnswersDb(session, status, email, creator, answerLabels, src)
      .catch(e => console.error('answers db error', e.message))
  ];
  if (status === 'Complete' && email) {
    mirrorJobs.push(
      appendToSheet([
        email, ts, creator,
        answerLabels.q1 || '', answerLabels.q2 || '',
        // column F stays a blank spacer where retired Q3 lived, so A-J alignment holds
        '', answerLabels.q4 || '',
        src,
        // Gender/Age appended as columns I/J so legacy A-H alignment is untouched
        answerLabels.gender || '', answerLabels.age || ''
      ]).catch(e => console.error('sheet error', e.message)),
      appendToEmailsDb(email, ts, creator, answerLabels, src)
        .catch(e => console.error('emails db error', e.message))
    );
  }
  const mirrors = Promise.allSettled(mirrorJobs);

  try {
    const r = await fetch('https://api.notion.com/v1/pages', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${process.env.NOTION_TOKEN}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ parent: { database_id: process.env.NOTION_DB_ID }, properties: props })
    });
    await mirrors;
    if (!r.ok) {
      const t = await r.text();
      console.error('notion error', r.status, t.slice(0, 300));
      return res.status(502).json({ ok: false });
    }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('submit error', e);
    await mirrors;
    return res.status(500).json({ ok: false });
  }
};
