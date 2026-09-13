# Built-in Functions Reference (n8n Code Node, JavaScript)

## `$helpers.httpRequest()` — make HTTP calls directly from code

Without a separate HTTP Request node:
```javascript
const response = await $helpers.httpRequest({
  method: 'POST',                 // GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
  url: 'https://api.example.com/users',
  headers: { 'Authorization': 'Bearer token123', 'Content-Type': 'application/json' },
  body: { name: 'John Doe', email: 'john@example.com' },
  qs: { page: 1, limit: 10 },     // query-string params
  timeout: 10000,                 // ms; default is no timeout
  json: true,                     // auto-parse JSON response (default true)
  simple: false,                  // don't throw on 4xx/5xx (default true throws)
  resolveWithFullResponse: false  // return only the body by default
});
```

Auth patterns:
```javascript
// Bearer token
headers: { 'Authorization': `Bearer ${$env.API_TOKEN}` }

// API key header
headers: { 'X-API-Key': $env.API_KEY }

// Basic auth (manual)
const credentials = Buffer.from(`${username}:${password}`).toString('base64');
headers: { 'Authorization': `Basic ${credentials}` }
```

Error handling:
```javascript
try {
  const response = await $helpers.httpRequest({ method: 'GET', url: 'https://api.example.com/users', simple: false });
  if (response.statusCode >= 200 && response.statusCode < 300) {
    return [{ json: { success: true, data: response.body } }];
  } else {
    return [{ json: { success: false, status: response.statusCode, error: response.body } }];
  }
} catch (error) {
  return [{ json: { success: false, error: error.message } }];
}
```

Full response (headers + status), when needed:
```javascript
const response = await $helpers.httpRequest({ url: 'https://api.example.com/data', resolveWithFullResponse: true });
return [{ json: { statusCode: response.statusCode, headers: response.headers, body: response.body, rateLimit: response.headers['x-ratelimit-remaining'] } }];
```

## `DateTime` (Luxon) — date/time operations

```javascript
const now = DateTime.now();
const nowTokyo = DateTime.now().setZone('Asia/Tokyo');
const today = DateTime.now().startOf('day');

// Formatting
now.toISO();                          // "2025-01-20T15:30:00.000Z"
now.toSQL();                          // "2025-01-20 15:30:00.000"
now.toHTTP();                         // "Mon, 20 Jan 2025 15:30:00 GMT"
now.toFormat('yyyy-MM-dd');           // "2025-01-20"
now.toFormat('MMMM dd, yyyy');        // "January 20, 2025"
now.toFormat('EEEE, MMMM dd, yyyy');  // "Monday, January 20, 2025"

// Parsing
DateTime.fromISO('2025-01-20T15:30:00');
DateTime.fromFormat('01/20/2025', 'MM/dd/yyyy');
DateTime.fromSQL('2025-01-20 15:30:00');
DateTime.fromSeconds(1737384600);
DateTime.fromMillis(1737384600000);

// Arithmetic
now.plus({ days: 1 });  now.plus({ weeks: 1 });  now.plus({ months: 1 });  now.plus({ hours: 2 });
now.minus({ days: 1 }); now.minus({ weeks: 1 }); now.minus({ months: 1 }); now.minus({ hours: 2 });

// Comparisons
const targetDate = DateTime.fromISO('2025-12-31');
targetDate > now;                       // isFuture
targetDate < now;                       // isPast
targetDate.equals(now);
targetDate.diff(now, 'days').days;      // daysUntil
targetDate.diff(now, ['months', 'days', 'hours']).toObject();  // detailed diff

// Timezones
now.setZone('Asia/Tokyo').toISO();
now.setZone('America/New_York').toISO();
now.toUTC().toISO();
now.zoneName;   // "America/Los_Angeles"
now.offset;     // offset in minutes
now.toFormat('ZZ'); // "+08:00"

// Start/end of period
now.startOf('day'); now.endOf('day');
now.startOf('week'); now.endOf('week');
now.startOf('month'); now.endOf('month');
now.startOf('year'); now.endOf('year');

// Weekday / month info
now.weekday;       // 1 = Monday ... 7 = Sunday
now.weekdayLong;   // "Monday"
now.month;         // 1-12
now.monthLong;     // "January"
now.quarter;       // 1-4
now.daysInMonth;   // 28-31
```

## `$jmespath()` — query JSON structures with JMESPath syntax

```javascript
const data = $input.first().json;
const names = $jmespath(data, 'users[*].name');
const adults = $jmespath(data, 'users[?age >= `18`]');
const firstUser = $jmespath(data, 'users[0]');

// Sort/slice/nested extraction/projection
const top5 = $jmespath(data, 'users | sort_by(@, &score) | reverse(@) | [0:5]');
const emails = $jmespath(data, 'users[*].contact.email');
const simplified = $jmespath(data, 'users[*].{name: name, email: contact.email}');
const premium = $jmespath(data, 'users[?subscription.tier == `premium`]');

// Aggregate functions
const sumPrice = $jmespath(data, 'sum(products[*].price)');
const maxPrice = $jmespath(data, 'max(products[*].price)');
const count = $jmespath(data, 'length(products)');
```

## `$getWorkflowStaticData()` — persistent storage across workflow executions

```javascript
// Simple counter
const staticData = $getWorkflowStaticData();
if (!staticData.counter) staticData.counter = 0;
staticData.counter++;
return [{ json: { executionCount: staticData.counter } }];

// Rate limiting
const now = Date.now();
if (!staticData.lastRun) {
  staticData.lastRun = now; staticData.runCount = 1;
} else {
  if (now - staticData.lastRun < 60000) {
    return [{ json: { error: 'Rate limit: wait 1 minute between runs' } }];
  }
  staticData.lastRun = now; staticData.runCount++;
}

// Tracking last-processed id, to only act on new items
const lastId = staticData.lastProcessedId || 0;
const newItems = $input.all().filter(item => item.json.id > lastId);
if (newItems.length > 0) {
  staticData.lastProcessedId = Math.max(...newItems.map(item => item.json.id));
}
return newItems;
```

## Standard JavaScript globals available

`Math` (round/floor/ceil/max/min/random/abs/sqrt/pow), `JSON` (parse/stringify, `JSON.stringify(obj, null, 2)` for pretty-print), `console` (log/error/warn/info — visible in the browser console), `Object` (keys/values/entries/assign, `'key' in obj`), standard Array methods (map/filter/reduce/some/every/find/includes/join).

## Available Node.js modules

```javascript
// crypto — hashing and random values
const crypto = require('crypto');
const hash = crypto.createHash('sha256').update('my secret text').digest('hex');
const md5 = crypto.createHash('md5').update('my text').digest('hex');
const randomBytes = crypto.randomBytes(16).toString('hex');

// Buffer — base64/hex encoding
const encoded = Buffer.from('Hello World').toString('base64');
const decoded = Buffer.from(encoded, 'base64').toString();
const hex = Buffer.from('Hello').toString('hex');

// URL / URLSearchParams
const url = new URL('https://example.com/path?param1=value1&param2=value2');
const params = new URLSearchParams({ search: 'query', page: 1, limit: 10 });
```

## What's NOT available

External npm packages of any kind — no `axios`, `lodash`, `moment` (use `DateTime`/Luxon instead), `request`, or anything else that would need `npm install`. Workaround: use `$helpers.httpRequest()` for HTTP calls, or bring data in via a dedicated HTTP Request node upstream.
