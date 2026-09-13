# n8n JavaScript Code Node

Reference for writing JavaScript inside n8n's Code node — the node type used for custom data transformation, aggregation, filtering, API calls, and any logic too complex for n8n's simpler nodes (Set, Filter, IF/Switch, HTTP Request). Use this whenever a workflow needs a Code node: choosing between its two execution modes, accessing input data correctly, calling HTTP APIs from inside the node, working with dates, avoiding the handful of mistakes that cause the vast majority of Code node failures, or building any custom transformation logic (aggregation, filtering, format conversion, batch-processing logic).

## How to Use This

1. **Pick the execution mode first.** The Code node runs in one of two modes — get this right before writing anything, since it determines which data-access syntax is valid.
   - **Run Once for All Items** (the default, and correct choice ~95% of the time): the code executes once total, regardless of how many items came in. Access data via `$input.all()` (or the `items` array). Use this for aggregation, filtering, batch processing, transformations, sorting/ranking, deduplication, or any case where you're comparing or combining items across the dataset.
   - **Run Once for Each Item** (specialized cases only): the code executes separately per input item. Access the current item via `$input.item`. Use this only when each item genuinely needs independent handling — its own API call, its own validation with different error handling, or a transformation that depends on that item's own properties in a way that doesn't need to see other items.
   - Decision shortcut: need to look at multiple items at once → All Items mode. Each item is completely independent → Each Item mode. Not sure → default to All Items (you can always loop inside the code).

2. **Always return the correct format.** A Code node MUST return an array, and every element of that array MUST have a `json` property. This is the single most common source of failures.
   ```javascript
   // Correct — single result
   return [{ json: { field1: value1, field2: value2 } }];

   // Correct — multiple results
   return [
     { json: { id: 1, data: 'first' } },
     { json: { id: 2, data: 'second' } }
   ];

   // Correct — transformed array
   const transformed = $input.all()
     .filter(item => item.json.valid)
     .map(item => ({ json: { id: item.json.id, processed: true } }));
   return transformed;

   // Correct — empty result when there's nothing to return
   return [];
   ```
   Wrong formats that will break the workflow:
   ```javascript
   return { json: { field: value } };   // ✗ object, not array-wrapped
   return [{ field: value }];            // ✗ missing the json wrapper
   return "processed";                   // ✗ plain string
   return $input.all();                  // ✗ raw passthrough without mapping — risky, don't rely on existing structure
   return [{ data: value }];             // ✗ wrong key name — must be "json"
   ```

3. **Know that webhook data is nested under `.body`.** This is the single most common mistake. A Webhook node wraps everything — POST data, query parameters, JSON payloads — inside a `body` property.
   ```javascript
   // ✗ WRONG — returns undefined
   const name = $json.name;
   const email = $json.email;

   // ✓ CORRECT
   const name = $json.body.name;
   const email = $json.body.email;

   // or, extracting first
   const webhookData = $input.first().json.body;
   const name = webhookData.name;
   ```
   The full webhook output structure looks like:
   ```javascript
   {
     "headers": { "content-type": "application/json", "user-agent": "...", /* ... */ },
     "params": {},
     "query": {},
     "body": {
       // ← your actual data is here
       "name": "Alice",
       "email": "alice@example.com",
       "message": "Hello!"
     }
   }
   ```
   Also available on the same object: `webhook.query` (query-string parameters), `webhook.headers` (HTTP headers, e.g. `webhook.headers['content-type']`), and `webhook.method` / `webhook.url`.

4. **Use JavaScript directly — never n8n's `{{ }}` expression syntax inside a Code node.** The `{{ }}` templating syntax is for OTHER node types (Set, IF, HTTP Request). Inside a Code node, everything is plain JavaScript.
   ```javascript
   // ✗ WRONG
   const value = "{{ $json.field }}";           // literal string, not the value
   const message = `{{ $json.firstName }} {{ $json.lastName }}`;

   // ✓ CORRECT
   const value = $json.field;
   const message = `${$json.firstName} ${$json.lastName}`;  // template literal, backticks
   ```
   | Context | Syntax |
   |---|---|
   | Set node, IF node, HTTP Request URL, etc. | `{{ }}` expressions |
   | **Code node** | **plain JavaScript** |
   | Code node string interpolation | template literals with backticks: `` `Hello ${name}` `` |

5. **Guard against null/undefined before accessing nested data.** Use optional chaining (`?.`), nullish coalescing (`??`), default values (`||`), or explicit guard clauses — don't assume a field exists.
   ```javascript
   // ✗ crashes if item.json.user doesn't exist
   const value = item.json.user.email;

   // ✓ safe
   const value = item.json?.user?.email || 'no-email@example.com';

   // ✓ guard clause
   if (!item.json.user) { return []; }
   const value = item.json.user.email;
   ```

6. **Attach `pairedItem` when creating output items that don't map 1:1 to input items** — otherwise downstream Set nodes will fail with a `paired_item_no_info` error.
   ```javascript
   const results = [];
   for (let i = 0; i < $input.all().length; i++) {
     const item = $input.all()[i];
     results.push({
       json: { /* new data */ },
       pairedItem: { item: i }
     });
   }
   return results;
   ```

7. **Reference other nodes correctly.** Call `.first()` (or `.all()`) before `.json` — you cannot chain `.json` directly onto a node reference.
   ```javascript
   // ✗ WRONG
   const data = $('HTTP Request').json;

   // ✓ CORRECT
   const data = $('HTTP Request').first().json;
   const allData = $('HTTP Request').all();

   // Legacy-style but equivalent form using $node
   const webhookData = $node["Webhook"].json;
   ```

8. **Watch out for SplitInBatches loops.** The node has two outputs and the naming is counterintuitive: `main[0]` is "done" (fires once, after all batches finish) and `main[1]` is "each batch" (fires per batch — this is the loop body). Add a Limit-1 node after the "done" output as a safety net against edge cases where it fires with extra items.

9. **Accumulate data across loop iterations using workflow static data, not node references.** After a SplitInBatches loop, calling `.all()` on a node inside the loop returns only the LAST iteration's items, not the cumulative set — this silently drops data from every batch but the final one.
   ```javascript
   // BEFORE the loop (reset the accumulator)
   const staticData = $getWorkflowStaticData('global');
   staticData.results = [];
   return $input.all();

   // INSIDE the loop body (accumulate)
   const staticData = $getWorkflowStaticData('global');
   const results = [];
   for (const item of $input.all()) {
     const processed = { /* ... */ };
     results.push({ json: processed });
     staticData.results.push(processed);
   }
   return results;

   // AFTER the loop (read the full accumulated set)
   const staticData = $getWorkflowStaticData('global');
   const allResults = staticData.results || [];
   ```

10. **Round currency/price comparisons to cents before comparing** — floating-point noise causes false-positive "price changed" detections.
    ```javascript
    // ✗ unreliable
    if (newPrice !== oldPrice) { /* triggers on floating-point noise */ }

    // ✓ reliable
    if (Math.round(newPrice * 100) !== Math.round(oldPrice * 100)) {
      // real price change
    }
    ```

11. **Before finishing, run the checklist** under Rules & Standards below.

## Rules & Standards

### Top 5 error patterns (ranked by real-world frequency)

**#1 — Empty code or missing return statement (~38% of all failures, the single most common error).**
```javascript
// ✗ code executes but never returns
const items = $input.all();
for (const item of items) { console.log(item.json.name); }
// forgot to return!

// ✗ one path returns, another doesn't
if (items.length === 0) { return []; }
const processed = items.map(item => ({ json: item.json }));
// forgot to return processed!

// ✓ every path returns
const items = $input.all();
if (items.length === 0) {
  return [];
} else if (items.length === 1) {
  return [{ json: { single: true, data: items[0].json } }];
} else {
  return items.map(item => ({ json: item.json }));
}
```
Checklist: code field is not empty · a return statement exists · ALL code paths (every if/else branch) return · return format is correct · return happens even on the error path (use try/catch).

**#2 — Expression syntax confusion (~8% of failures)** — using `{{ }}` inside the Code node. Covered in step 4 above.

**#3 — Incorrect return wrapper (~5% of failures)** — covered in step 2 above. Quick reference for common scenarios:
```javascript
// Single object from an API response
const response = $input.first().json;
return [{ json: response }];          // ✓
// return {json: response};           // ✗

// Array of objects
const users = $input.all();
return users.map(user => ({ json: user.json })); // ✓
// return users;                      // ✗ risky — depends on existing structure

// Computed result
const total = $input.all().reduce((sum, item) => sum + item.json.amount, 0);
return [{ json: { total } }];         // ✓
// return {total};                    // ✗

// No results
return [];                            // ✓
// return null;                       // ✗
```

**#4 — Unmatched expression brackets (~6% of failures)** — usually from unbalanced quotes inside strings, multi-line strings with embedded quotes, or unescaped regex. Fix by preferring template literals (backticks) for anything multi-line or containing quotes:
```javascript
// ✗ risky
const message = "It's a nice day";
const html = "
  <div class="container"><p>Hello</p></div>
";

// ✓ safe — backticks handle multi-line and embedded quotes cleanly
const message = `It's a nice day`;
const html = `
  <div class="container">
    <p>Hello</p>
  </div>
`;
```
Escaping reference: `\'` for a single quote inside a single-quoted string, `\"` for a double quote inside a double-quoted string, `\\` for a literal backslash, `\n` for newline, `\t` for tab.

**#5 — Missing null checks / undefined access (very common runtime error).** Covered in step 5 above. Additional safe-access patterns:
```javascript
// Optional chaining (preferred)
const value = data?.nested?.property?.value;

// Logical OR with a default
const value = data.property || 'default';

// Nullish coalescing (only falls back on null/undefined, not on 0 or '')
const timeout = $json.settings?.advanced?.timeout ?? 30000;

// Guard clause
if (!data.property) { return []; }

// Try/catch for genuinely risky operations
try {
  const value = data.nested.property.value;
} catch (error) {
  const value = 'default';
}
```
Apply the same caution to webhook payloads (`const name = $json.body?.user?.name || 'Unknown';`) and to arrays (check `.length` before indexing, or use `$input.first()` which has built-in safety over `$input.all()[0]`).

### Quick-reference checklist before shipping a Code node

- [ ] Code is not empty and has meaningful logic
- [ ] A return statement exists on every code path
- [ ] Return format is `[{ json: {...} }]` — array of objects, each with a `json` key
- [ ] Data access uses `$input.all()`, `$input.first()`, or `$input.item` (matching the selected mode) — not bare `$json` used ambiguously
- [ ] No `{{ }}` expression syntax anywhere — plain JavaScript / template literals only
- [ ] Guard clauses or optional chaining protect every place null/undefined could appear
- [ ] Webhook data is accessed via `.body`
- [ ] Mode is "All Items" unless there's a specific reason for "Each Item"
- [ ] Prefer `.map()`/`.filter()`/`.reduce()` over manual loops where reasonable
- [ ] All code paths return the same shape of data

### When to use the Code node vs. a simpler node

Use Code node for: complex multi-step transformations, custom calculations/business logic, recursive operations, parsing complex API response structures, multi-step conditionals, cross-item aggregation.

Use a simpler node instead when: it's simple field mapping (→ Set node), basic filtering (→ Filter node), a simple conditional (→ IF or Switch node), or just an HTTP call with no transformation (→ HTTP Request node). The Code node's real strength is handling logic that would otherwise require chaining many simple nodes together.

## Templates & Examples

### Data access patterns

**`$input.all()` — the default, most common pattern.** Use for anything that needs to see multiple items at once: filtering, transforming, aggregating, sorting, grouping, deduplicating.
```javascript
// Filter
const activeItems = $input.all().filter(item => item.json.status === 'active');

// Transform / map
const transformed = $input.all().map(item => ({
  json: {
    id: item.json.id,
    fullName: `${item.json.firstName} ${item.json.lastName}`,
    email: item.json.email,
    processedAt: new Date().toISOString()
  }
}));

// Aggregate
const allItems = $input.all();
const total = allItems.reduce((sum, item) => sum + (item.json.amount || 0), 0);
return [{ json: { total, count: allItems.length, average: total / allItems.length } }];

// Sort and limit (top 5 by score)
const topFive = $input.all()
  .sort((a, b) => (b.json.score || 0) - (a.json.score || 0))
  .slice(0, 5);
return topFive.map(item => ({ json: item.json }));

// Group by category
const grouped = {};
for (const item of $input.all()) {
  const category = item.json.category || 'Uncategorized';
  if (!grouped[category]) grouped[category] = [];
  grouped[category].push(item.json);
}
return Object.entries(grouped).map(([category, items]) => ({
  json: { category, items, count: items.length }
}));

// Deduplicate by id
const seen = new Set();
const unique = [];
for (const item of $input.all()) {
  if (!seen.has(item.json.id)) { seen.add(item.json.id); unique.push(item); }
}
return unique;
```

**`$input.first()` — for single-object cases**, e.g. an API response that's a single object, or grabbing the first-in-first-out item.
```javascript
const response = $input.first().json;
return [{
  json: {
    userId: response.data.user.id,
    userName: response.data.user.name,
    status: response.status,
    fetchedAt: new Date().toISOString()
  }
}];
```

**`$input.item` — only valid in "Each Item" mode.**
```javascript
const item = $input.item;
return [{
  json: { ...item.json, processed: true, processedAt: new Date().toISOString() }
}];
```

**`$node["NodeName"]` / `$("NodeName")` — reference a specific other node**, useful when combining data from multiple named nodes or comparing across an execution.
```javascript
const oldData = $node["Get Old Data"].json;
const newData = $node["Get New Data"].json;
const changes = {
  added: newData.filter(n => !oldData.find(o => o.id === n.id)),
  removed: oldData.filter(o => !newData.find(n => n.id === o.id)),
  modified: newData.filter(n => {
    const old = oldData.find(o => o.id === n.id);
    return old && JSON.stringify(old) !== JSON.stringify(n);
  })
};
return [{ json: { changes, summary: {
  added: changes.added.length, removed: changes.removed.length, modified: changes.modified.length
} } }];
```

Decision tree: need ALL items → `$input.all()`. Need just the FIRST → `$input.first()`. In "Each Item" mode → `$input.item`. Need a specific named node's data → `$node["Name"]` / `$("Name")`. Default fallback → `$input.first()`.

### Ten production-tested patterns

**1. Multi-source data aggregation** — normalize and combine data from different APIs/feeds into one structure.
```javascript
const allItems = $input.all();
let processedArticles = [];
for (const item of allItems) {
  const sourceName = item.json.name || 'Unknown';
  const sourceData = item.json;
  if (sourceName === 'Hacker News' && sourceData.hits) {
    for (const hit of sourceData.hits) {
      processedArticles.push({ title: hit.title, url: hit.url, summary: hit.story_text || 'No summary', source: 'Hacker News', score: hit.points || 0, fetchedAt: new Date().toISOString() });
    }
  } else if (sourceName === 'Reddit' && sourceData.data?.children) {
    for (const post of sourceData.data.children) {
      processedArticles.push({ title: post.data.title, url: post.data.url, summary: post.data.selftext || 'No summary', source: 'Reddit', score: post.data.score || 0, fetchedAt: new Date().toISOString() });
    }
  } else if (sourceName === 'RSS' && sourceData.items) {
    for (const rssItem of sourceData.items) {
      processedArticles.push({ title: rssItem.title, url: rssItem.link, summary: rssItem.description || 'No summary', source: 'RSS Feed', score: 0, fetchedAt: new Date().toISOString() });
    }
  }
}
processedArticles.sort((a, b) => b.score - a.score);
return processedArticles.map(article => ({ json: article }));
```
Variations: apply per-source weighting to scores, filter by minimum score, or deduplicate by URL using a `Set`.

**2. Regex filtering & pattern matching** — extract mentions, keywords, emails, phone numbers, hashtags, URLs from text.
```javascript
const etfPattern = /\b([A-Z]{2,5})\b/g;
const knownETFs = ['VOO', 'VTI', 'VT', 'SCHD', 'QYLD', 'VXUS', 'SPY', 'QQQ'];
const etfMentions = {};
for (const item of $input.all()) {
  const data = item.json.data;
  if (!data?.children) continue;
  for (const post of data.children) {
    const combinedText = ((post.data.title || '') + ' ' + (post.data.selftext || '')).toUpperCase();
    const matches = combinedText.match(etfPattern);
    if (matches) {
      for (const match of matches) {
        if (knownETFs.includes(match)) {
          if (!etfMentions[match]) etfMentions[match] = { count: 0, totalScore: 0, posts: [] };
          etfMentions[match].count++;
          etfMentions[match].totalScore += post.data.score || 0;
          etfMentions[match].posts.push({ title: post.data.title, url: post.data.url, score: post.data.score });
        }
      }
    }
  }
}
return Object.entries(etfMentions)
  .map(([etf, data]) => ({ json: {
    etf, mentions: data.count, totalScore: data.totalScore,
    averageScore: data.totalScore / data.count,
    topPosts: data.posts.sort((a, b) => b.score - a.score).slice(0, 3)
  } }))
  .sort((a, b) => b.json.mentions - a.json.mentions);
```
Common sub-patterns:
```javascript
const emailPattern = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g;
const phonePattern = /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g;
const hashtagPattern = /#(\w+)/g;
const urlPattern = /https?:\/\/[^\s]+/g;
```

**3. Markdown/structured-text parsing** — turn formatted text into JSON.
```javascript
const markdown = $input.first().json.data.markdown;
const adRegex = /##\s*(.*?)\n(.*?)(?=\n##|\n---|$)/gs;
const ads = [];
let match;
function parseTimeToMinutes(timeStr) {
  if (!timeStr) return 999999;
  const hourMatch = timeStr.match(/(\d+)\s*hour/);
  const dayMatch = timeStr.match(/(\d+)\s*day/);
  const minMatch = timeStr.match(/(\d+)\s*min/);
  let totalMinutes = 0;
  if (dayMatch) totalMinutes += parseInt(dayMatch[1]) * 1440;
  if (hourMatch) totalMinutes += parseInt(hourMatch[1]) * 60;
  if (minMatch) totalMinutes += parseInt(minMatch[1]);
  return totalMinutes;
}
while ((match = adRegex.exec(markdown)) !== null) {
  const title = match[1]?.trim() || 'No title';
  const content = match[2]?.trim() || '';
  const districtMatch = content.match(/\*\*District:\*\*\s*(.*?)(?:\n|$)/);
  const salaryMatch = content.match(/\*\*Salary:\*\*\s*(.*?)(?:\n|$)/);
  const timeMatch = content.match(/Posted:\s*(.*?)\*/);
  ads.push({
    title, district: districtMatch?.[1].trim() || 'Unknown',
    salary: salaryMatch?.[1].trim() || 'Not specified',
    postedTimeAgo: timeMatch?.[1] || 'Unknown',
    timeInMinutes: parseTimeToMinutes(timeMatch?.[1]),
    fullContent: content, extractedAt: new Date().toISOString()
  });
}
ads.sort((a, b) => a.timeInMinutes - b.timeInMinutes);
return ads.map(ad => ({ json: ad }));
```

**4. JSON comparison & validation** — detect changes between two versions of data.
```javascript
const orderJsonKeys = (jsonObj) => {
  const ordered = {};
  Object.keys(jsonObj).sort().forEach(key => { ordered[key] = jsonObj[key]; });
  return ordered;
};
const allItems = $input.all();
const origWorkflow = JSON.parse(Buffer.from(allItems[0].json.content, 'base64').toString());
const currentWorkflow = allItems[1].json;
const orderedOriginal = orderJsonKeys(origWorkflow);
const orderedCurrent = orderJsonKeys(currentWorkflow);
const isSame = JSON.stringify(orderedOriginal) === JSON.stringify(orderedCurrent);
const differences = [];
for (const key of Object.keys(orderedOriginal)) {
  if (JSON.stringify(orderedOriginal[key]) !== JSON.stringify(orderedCurrent[key])) {
    differences.push({ field: key, original: orderedOriginal[key], current: orderedCurrent[key] });
  }
}
for (const key of Object.keys(orderedCurrent)) {
  if (!(key in orderedOriginal)) {
    differences.push({ field: key, original: null, current: orderedCurrent[key], status: 'new' });
  }
}
return [{ json: { identical: isSame, differenceCount: differences.length, differences, original: orderedOriginal, current: orderedCurrent, comparedAt: new Date().toISOString() } }];
```
A reusable deep-diff helper:
```javascript
function deepDiff(obj1, obj2, path = '') {
  const changes = [];
  for (const key in obj1) {
    const currentPath = path ? `${path}.${key}` : key;
    if (!(key in obj2)) { changes.push({ type: 'removed', path: currentPath, value: obj1[key] }); }
    else if (typeof obj1[key] === 'object' && typeof obj2[key] === 'object') { changes.push(...deepDiff(obj1[key], obj2[key], currentPath)); }
    else if (obj1[key] !== obj2[key]) { changes.push({ type: 'modified', path: currentPath, from: obj1[key], to: obj2[key] }); }
  }
  for (const key in obj2) {
    if (!(key in obj1)) { changes.push({ type: 'added', path: path ? `${path}.${key}` : key, value: obj2[key] }); }
  }
  return changes;
}
```

**5. CRM/lead data transformation** — normalize form submissions into a CRM-ready shape.
```javascript
const item = $input.all()[0];
const { name, email, phone, company, course_interest, message, timestamp } = item.json;
const nameParts = name.split(' ');
const firstName = nameParts[0] || '';
const lastName = nameParts.slice(1).join(' ') || 'Unknown';
const cleanPhone = phone.replace(/[^\d]/g, '');
const crmData = {
  data: { type: 'Contact', attributes: {
    first_name: firstName, last_name: lastName, email1: email, phone_work: cleanPhone,
    account_name: company,
    description: `Course Interest: ${course_interest}\n\nMessage: ${message}\n\nSubmitted: ${timestamp}`,
    lead_source: 'Website Form', status: 'New'
  } },
  metadata: { original_submission: timestamp, processed_at: new Date().toISOString() }
};
return [{ json: { ...item.json, crmData, processed: true } }];
```
A simple lead-scoring helper:
```javascript
function calculateLeadScore(data) {
  let score = 0;
  if (data.email) score += 10;
  if (data.phone) score += 10;
  if (data.company) score += 15;
  if (data.title?.toLowerCase().includes('director')) score += 20;
  if (data.title?.toLowerCase().includes('manager')) score += 15;
  if (data.message?.length > 100) score += 10;
  return score;
}
```

**6. Release/changelog processing** — filter and summarize versioned releases (e.g. from a GitHub-style API).
```javascript
const allReleases = $input.first().json;
const stableReleases = allReleases
  .filter(release => !release.prerelease && !release.draft)
  .slice(0, 10)
  .map(release => {
    const body = release.body || '';
    let highlights = 'No highlights available';
    if (body.includes('## Highlights:')) {
      highlights = body.split('## Highlights:')[1]?.split('##')[0]?.trim();
    } else {
      highlights = body.substring(0, 500) + '...';
    }
    return {
      tag: release.tag_name, name: release.name, published: release.published_at,
      publishedDate: new Date(release.published_at).toLocaleDateString(),
      author: release.author.login, url: release.html_url, changelog: body, highlights,
      assetCount: release.assets.length,
      assets: release.assets.map(asset => ({ name: asset.name, size: asset.size, downloadCount: asset.download_count, downloadUrl: asset.browser_download_url }))
    };
  });
return stableReleases.map(release => ({ json: release }));
```

**7. Array transformation with computed context fields** — add ranking, percentages, or category labels.
```javascript
// Ranking with medals
const items = $input.all()
  .sort((a, b) => b.json.score - a.json.score)
  .map((item, index) => ({ json: { ...item.json, rank: index + 1, medal: index < 3 ? ['🥇', '🥈', '🥉'][index] : '' } }));

// Percentage of total
const total = $input.all().reduce((sum, item) => sum + item.json.value, 0);
const itemsWithPercentage = $input.all().map(item => ({ json: { ...item.json, percentage: ((item.json.value / total) * 100).toFixed(2) + '%' } }));

// Category labels
const categorize = (value) => value > 100 ? 'High' : value > 50 ? 'Medium' : 'Low';
const categorized = $input.all().map(item => ({ json: { ...item.json, category: categorize(item.json.value) } }));
```

**8. Slack Block Kit message formatting** — build rich chat notifications.
```javascript
const date = new Date().toISOString().split('T')[0];
const data = $input.first().json;
return [{
  json: {
    text: `Daily Report - ${date}`,
    blocks: [
      { type: "header", text: { type: "plain_text", text: `📊 Daily Security Report - ${date}` } },
      { type: "section", text: { type: "mrkdwn", text: `*Status:* ${data.status === 'ok' ? '✅ All Clear' : '⚠️ Issues Detected'}\n*Alerts:* ${data.alertCount || 0}\n*Updated:* ${new Date().toLocaleString()}` } },
      { type: "divider" },
      { type: "section", fields: [
        { type: "mrkdwn", text: `*Failed Logins:*\n${data.failedLogins || 0}` },
        { type: "mrkdwn", text: `*API Errors:*\n${data.apiErrors || 0}` },
        { type: "mrkdwn", text: `*Uptime:*\n${data.uptime || '100%'}` },
        { type: "mrkdwn", text: `*Response Time:*\n${data.avgResponseTime || 'N/A'}ms` }
      ] },
      { type: "context", elements: [{ type: "mrkdwn", text: `Report generated automatically by n8n workflow` }] }
    ]
  }
}];
```

**9. Top-N filtering & ranking** — for RAG pipelines, leaderboards, relevance ranking.
```javascript
const ragResponse = $input.item.json;
const chunks = ragResponse.chunks || [];
const topChunks = chunks.sort((a, b) => (b.similarity || 0) - (a.similarity || 0)).slice(0, 6);
return [{ json: {
  query: ragResponse.query, topChunks, count: topChunks.length,
  maxSimilarity: topChunks[0]?.similarity || 0,
  minSimilarity: topChunks[topChunks.length - 1]?.similarity || 0,
  averageSimilarity: topChunks.reduce((sum, chunk) => sum + (chunk.similarity || 0), 0) / topChunks.length
} }];
```
Variations: filter by a minimum threshold before sorting/slicing; sort ascending for bottom-N/worst-performers; combine multiple weighted criteria into a composite score before ranking; compute a percentile cutoff and filter to it.

**10. String aggregation & report generation** — combine multiple items into one formatted report.
```javascript
const allItems = $input.all();
const messages = allItems.map(item => item.json.message);
const header = `🎯 **Daily Summary Report**\n📅 ${new Date().toLocaleString()}\n📊 Total Items: ${messages.length}\n\n`;
const divider = '\n\n---\n\n';
const footer = `\n\n---\n\n✅ Report generated at ${new Date().toISOString()}`;
const finalReport = header + messages.join(divider) + footer;
return [{ json: { report: finalReport, messageCount: messages.length, generatedAt: new Date().toISOString(), reportLength: finalReport.length } }];
```
Variations: numbered list, markdown table (`| Name | Status | Score |` header + row-mapped body), full HTML report, or a structured JSON summary with totals/average/max/min.

Pattern selection guide:
| Goal | Pattern |
|---|---|
| Combine multiple API responses | Multi-source aggregation |
| Extract mentions or keywords | Regex filtering |
| Parse formatted text | Markdown parsing |
| Detect changes in data | JSON comparison |
| Prepare form data for a CRM | CRM transformation |
| Process a release/changelog feed | Release processing |
| Add computed fields | Array transformation |
| Format a chat notification | Slack Block Kit formatting |
| Get top results | Top-N filtering |
| Create a text report | String aggregation |

### Built-in functions reference

**`$helpers.httpRequest()` — make HTTP calls directly from code**, without a separate HTTP Request node.
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

**`DateTime` (Luxon) — date/time operations.**
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

**`$jmespath()` — query JSON structures with JMESPath syntax.**
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

**`$getWorkflowStaticData()` — persistent storage across workflow executions.**
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

**Standard JavaScript globals available:** `Math` (round/floor/ceil/max/min/random/abs/sqrt/pow), `JSON` (parse/stringify, `JSON.stringify(obj, null, 2)` for pretty-print), `console` (log/error/warn/info — visible in the browser console), `Object` (keys/values/entries/assign, `'key' in obj`), standard Array methods (map/filter/reduce/some/every/find/includes/join).

**Available Node.js modules:**
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

**What's NOT available:** external npm packages of any kind — no `axios`, `lodash`, `moment` (use `DateTime`/Luxon instead), `request`, or anything else that would need `npm install`. Workaround: use `$helpers.httpRequest()` for HTTP calls, or bring data in via a dedicated HTTP Request node upstream.
