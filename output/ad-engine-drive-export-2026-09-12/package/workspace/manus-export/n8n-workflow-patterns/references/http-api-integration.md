# HTTP/API Integration

**Pattern structure**: `Trigger → HTTP Request → [Transform] → [Action] → [Error Handler]`

**Key characteristic**: external data fetching with error handling.

## Core Components

**1. Trigger** — Schedule (periodic fetching, most common), Webhook (triggered by an external event), or Manual (on-demand execution).

**2. HTTP Request node** — call external REST APIs:
```javascript
{
  method: "GET",                    // GET, POST, PUT, DELETE, PATCH
  url: "https://api.example.com/users",
  authentication: "predefinedCredentialType",
  sendQuery: true,
  queryParameters: {
    "page": "={{$json.page}}",
    "limit": "100"
  },
  sendHeaders: true,
  headerParameters: {
    "Accept": "application/json",
    "X-API-Version": "v1"
  }
}
```

**3. Response processing** — extract and transform API response data. Typical flow: `HTTP Request → Code (parse) → Set (map fields) → Action`.

**4. Action** — common actions: store in database, send to another API, create notifications, update a spreadsheet.

**5. Error handler** — handle API failures gracefully via an Error Trigger workflow: `Error Trigger → Log Error → Notify Admin → Retry Logic (optional)`.

## Common Use Cases

**1. Data fetching & storage** — `Schedule → HTTP Request → Transform → Database`

Example (fetch GitHub issues):
```
1. Schedule (every hour)
2. HTTP Request
   - Method: GET
   - URL: https://api.github.com/repos/owner/repo/issues
   - Auth: Bearer Token
   - Query: state=open
3. Code (filter by labels)
4. Set (map to database schema)
5. Postgres (upsert issues)
```
Response handling:
```javascript
// Code node - filter issues
const issues = $input.all();
return issues
  .filter(item => item.json.labels.some(l => l.name === 'bug'))
  .map(item => ({
    json: {
      id: item.json.id,
      title: item.json.title,
      created_at: item.json.created_at
    }
  }));
```

**2. API to API integration** — `Trigger → Fetch from API A → Transform → Send to API B`

Example (Jira to Slack):
```
1. Schedule (every 15 minutes)
2. HTTP Request (GET Jira tickets updated today)
3. IF (check if tickets exist)
4. Set (format for Slack)
5. HTTP Request (POST to Slack webhook)
```

**3. Data enrichment** — `Trigger → Fetch base data → Call enrichment API → Combine → Store`

Example (enrich contacts with company data):
```
1. Postgres (SELECT new contacts)
2. Code (extract company domains)
3. HTTP Request (call Clearbit API for each domain)
4. Set (combine contact + company data)
5. Postgres (UPDATE contacts with enrichment)
```

**4. Monitoring & alerting** — `Schedule → Check API health → IF unhealthy → Alert`

Example (API health check):
```
1. Schedule (every 5 minutes)
2. HTTP Request (GET /health endpoint)
3. IF (status !== 200 OR response time > 2000ms)
4. Slack (alert #ops-team)
5. PagerDuty (create incident)
```

**5. Batch processing** — `Trigger → Fetch large dataset → Split in Batches → Process → Loop`

Example (process all users):
```
1. Manual Trigger
2. HTTP Request (GET /api/users?limit=1000)
3. Split In Batches (100 items per batch)
4. HTTP Request (POST /api/process for each batch)
5. Wait (2 seconds between batches - rate limiting)
6. Loop (back to step 4 until all processed)
```

## Authentication Methods

**1. None (public APIs)**:
```javascript
{ authentication: "none" }
```

**2. Bearer Token (most common)** — set up as a credential:
```javascript
{
  authentication: "predefinedCredentialType",
  nodeCredentialType: "httpHeaderAuth",
  headerAuth: {
    name: "Authorization",
    value: "Bearer YOUR_TOKEN"
  }
}
```
Access in the workflow:
```javascript
{
  authentication: "predefinedCredentialType",
  nodeCredentialType: "httpHeaderAuth"
}
```

**3. API key (header or query)**

Header auth:
```javascript
{
  sendHeaders: true,
  headerParameters: {
    "X-API-Key": "={{$credentials.apiKey}}"
  }
}
```
Query auth:
```javascript
{
  sendQuery: true,
  queryParameters: {
    "api_key": "={{$credentials.apiKey}}"
  }
}
```

**4. Basic Auth** — set up a "Basic Auth" credential:
```javascript
{
  authentication: "predefinedCredentialType",
  nodeCredentialType: "httpBasicAuth"
}
```

**5. OAuth2** — set up an OAuth2 credential with an authorization URL, token URL, client ID, client secret, and scopes:
```javascript
{
  authentication: "predefinedCredentialType",
  nodeCredentialType: "oAuth2Api"
}
```

## Handling API Responses

**Success response (200-299)** — data flows to the next node by default. Access it as `{{$json}}` for the entire response, or drill in with `{{$json.data.id}}` / `{{$json.results[0].name}}`.

### Pagination

Pattern 1: offset-based:
```
1. Set (initialize: page=1, has_more=true)
2. HTTP Request (GET /api/items?page={{$json.page}})
3. Code (check if more pages)
4. IF (has_more === true)
   └→ Set (increment page) → Loop to step 2
```
Code node (check pagination):
```javascript
const items = $input.first().json;
const currentPage = $json.page || 1;

return [{
  json: {
    items: items.results,
    page: currentPage + 1,
    has_more: items.next !== null
  }
}];
```

Pattern 2: cursor-based:
```
1. HTTP Request (GET /api/items)
2. Code (extract next_cursor)
3. IF (next_cursor exists)
   └→ Set (cursor={{$json.next_cursor}}) → Loop to step 1
```

Pattern 3: Link header:
```javascript
// Code node - parse Link header
const linkHeader = $input.first().json.headers['link'];
const hasNext = linkHeader && linkHeader.includes('rel="next"');

return [{
  json: {
    items: $input.first().json.body,
    has_next: hasNext,
    next_url: hasNext ? parseNextUrl(linkHeader) : null
  }
}];
```

**Error responses (400-599)** — configure the HTTP Request node:
```javascript
{
  continueOnFail: true,  // Don't stop workflow on error
  ignoreResponseCode: true  // Get response even on error
}
```
Handle errors:
```
HTTP Request (continueOnFail: true)
  → IF (check error)
    ├─ [Success Path]
    └─ [Error Path] → Log → Retry or Alert
```
IF condition: `{{$json.error}}` is empty, or `{{$json.statusCode}}` < 400.

## Rate Limiting

**Pattern 1: wait between requests**
```
Split In Batches (1 item per batch)
  → HTTP Request
  → Wait (1 second)
  → Loop
```

**Pattern 2: exponential backoff**
```javascript
// Code node
const maxRetries = 3;
let retryCount = $json.retryCount || 0;

if ($json.error && retryCount < maxRetries) {
  const delay = Math.pow(2, retryCount) * 1000; // 1s, 2s, 4s

  return [{
    json: {
      ...$json,
      retryCount: retryCount + 1,
      waitTime: delay
    }
  }];
}
```

**Pattern 3: respect rate-limit headers**
```javascript
// Code node - check rate limit
const headers = $input.first().json.headers;
const remaining = parseInt(headers['x-ratelimit-remaining'] || '999');
const resetTime = parseInt(headers['x-ratelimit-reset'] || '0');

if (remaining < 10) {
  const now = Math.floor(Date.now() / 1000);
  const waitSeconds = resetTime - now;

  return [{
    json: {
      shouldWait: true,
      waitSeconds: Math.max(waitSeconds, 0)
    }
  }];
}

return [{ json: { shouldWait: false } }];
```

## Request Configuration

GET request:
```javascript
{
  method: "GET",
  url: "https://api.example.com/users",
  sendQuery: true,
  queryParameters: {
    "page": "1",
    "limit": "100",
    "filter": "active"
  }
}
```

POST request (JSON body):
```javascript
{
  method: "POST",
  url: "https://api.example.com/users",
  sendBody: true,
  bodyParametersJson: JSON.stringify({
    name: "={{$json.name}}",
    email: "={{$json.email}}",
    role: "user"
  })
}
```

POST request (form data):
```javascript
{
  method: "POST",
  url: "https://api.example.com/upload",
  sendBody: true,
  bodyParametersUi: {
    parameter: [
      { name: "file", value: "={{$json.fileData}}" },
      { name: "filename", value: "={{$json.filename}}" }
    ]
  },
  sendHeaders: true,
  headerParameters: {
    "Content-Type": "multipart/form-data"
  }
}
```

PUT/PATCH request (update):
```javascript
{
  method: "PATCH",
  url: "https://api.example.com/users/={{$json.userId}}",
  sendBody: true,
  bodyParametersJson: JSON.stringify({
    status: "active",
    last_updated: "={{$now}}"
  })
}
```

DELETE request:
```javascript
{
  method: "DELETE",
  url: "https://api.example.com/users/={{$json.userId}}"
}
```

## Error Handling Patterns

**Pattern 1: retry on failure**
```
HTTP Request (continueOnFail: true)
  → IF (error occurred)
    └→ Wait (5 seconds)
    └→ HTTP Request (retry)
```

**Pattern 2: fallback API**
```
HTTP Request (Primary API, continueOnFail: true)
  → IF (failed)
    └→ HTTP Request (Fallback API)
```

**Pattern 3: Error Trigger workflow**

Main workflow:
```
HTTP Request → Process Data
```
Error workflow:
```
Error Trigger
  → Set (extract error details)
  → Slack (alert team)
  → Database (log error for analysis)
```

**Pattern 4: circuit breaker**
```javascript
// Code node - circuit breaker logic
const failures = $json.recentFailures || 0;
const threshold = 5;

if (failures >= threshold) {
  throw new Error('Circuit breaker open - too many failures');
}

return [{ json: { canProceed: true } }];
```

## Response Transformation

Extract nested data:
```javascript
// Code node
const response = $input.first().json;

return response.data.items.map(item => ({
  json: {
    id: item.id,
    name: item.attributes.name,
    email: item.attributes.contact.email
  }
}));
```

Flatten arrays:
```javascript
// Code node - flatten nested array
const items = $input.all();
const flattened = items.flatMap(item =>
  item.json.results.map(result => ({
    json: {
      parent_id: item.json.id,
      ...result
    }
  }))
);

return flattened;
```

Combine multiple API responses:
```
HTTP Request 1 (users)
  → Set (store users)
  → HTTP Request 2 (orders for each user)
  → Merge (combine users + orders)
```

## Testing & Debugging

1. **Test with a Manual Trigger** in place of Schedule while developing.
2. **Test the API outside n8n first** (Postman/Insomnia/curl) to understand the response structure and verify authentication before wiring it into a workflow.
3. **Log responses for debugging**:
```javascript
// Code node - log for debugging
console.log('API Response:', JSON.stringify($input.first().json, null, 2));
return $input.all();
```
4. **Check execution data** in the n8n UI — view node output, headers, body, and status code.
5. **Use binary data properly for file downloads**:
```javascript
{
  method: "GET",
  url: "https://api.example.com/download/file.pdf",
  responseFormat: "file",  // Important for binary data
  outputPropertyName: "data"
}
```

## Performance Optimization

1. **Parallel requests** via Split In Batches with multiple items per batch:
```
Set (create array of IDs)
  → Split In Batches (10 items per batch)
  → HTTP Request (processes all 10 in parallel)
  → Loop
```
2. **Caching**:
```
IF (check cache exists)
  ├─ [Cache Hit] → Use cached data
  └─ [Cache Miss] → HTTP Request → Store in cache
```
3. **Conditional fetching** — only fetch if data changed:
```
HTTP Request (GET with If-Modified-Since header)
  → IF (status === 304)
    └─ Use existing data
  → IF (status === 200)
    └─ Process new data
```
4. **Batch API calls** if the API supports batch operations:
```javascript
{
  method: "POST",
  url: "https://api.example.com/batch",
  bodyParametersJson: JSON.stringify({
    requests: $json.items.map(item => ({
      method: "GET",
      url: `/users/${item.id}`
    }))
  })
}
```

## Common Gotchas

**1. Wrong: hardcoded URLs** (`url: "https://api.example.com/prod/users"`). **Correct**: use environment variables — `url: "={{$env.API_BASE_URL}}/users"`.

**2. Wrong: credentials in parameters** (`headerParameters: { "Authorization": "Bearer sk-abc123xyz" }` — exposed!). **Correct**: use the credentials system (`authentication: "predefinedCredentialType", nodeCredentialType: "httpHeaderAuth"`).

**3. Wrong: no error handling** (`HTTP Request → Process` fails outright if the API is down). **Correct**: `HTTP Request (continueOnFail: true) → IF (error) → Handle`.

**4. Wrong: blocking on large responses** — processing 10,000 items synchronously. **Correct**: use batching — `Split In Batches (100 items) → Process → Loop`.

## Checklist for API Integration

**Planning**
- [ ] Test API with Postman/curl first
- [ ] Understand response structure
- [ ] Check rate limits
- [ ] Review authentication method
- [ ] Plan error handling

**Implementation**
- [ ] Use credentials (never hardcode)
- [ ] Configure proper HTTP method
- [ ] Set correct headers (Content-Type, Accept)
- [ ] Handle pagination if needed
- [ ] Add query parameters properly

**Error Handling**
- [ ] Set continueOnFail: true if needed
- [ ] Check response status codes
- [ ] Implement retry logic
- [ ] Add Error Trigger workflow
- [ ] Alert on failures

**Performance**
- [ ] Use batching for large datasets
- [ ] Add rate limiting if needed
- [ ] Consider caching
- [ ] Test with production load

**Security**
- [ ] Use HTTPS only
- [ ] Store secrets in credentials
- [ ] Validate API responses
- [ ] Use environment variables
