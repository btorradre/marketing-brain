# Ten Production-Tested Code Node Patterns

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

## Pattern Selection Guide

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
