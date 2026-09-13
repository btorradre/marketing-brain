# Scheduled Tasks

**Pattern structure**: `Schedule Trigger → [Fetch Data] → [Process] → [Deliver] → [Log/Notify]`

**Key characteristic**: time-based automated execution.

## Core Components

**1. Schedule Trigger** — execute the workflow at specified times. Modes: Interval (every X minutes/hours/days), Cron (specific times, advanced), Days & Hours (simple recurring schedule).

**2. Data source** — common sources: HTTP Request (APIs), database queries, file reads, service-specific nodes.

**3. Processing** — typical operations: filter/transform data, aggregate statistics, generate reports, check conditions.

**4. Delivery** — output channels: email, Slack/Discord/Teams, file storage, database writes.

**5. Logging** — track execution history via database log entries, file append, or a monitoring service.

## Schedule Configuration

**Interval mode** — best for simple recurring tasks:
```javascript
// Every 15 minutes
{
  mode: "interval",
  interval: 15,
  unit: "minutes"
}

// Every 2 hours
{
  mode: "interval",
  interval: 2,
  unit: "hours"
}

// Every day at midnight
{
  mode: "interval",
  interval: 1,
  unit: "days"
}
```

**Days & Hours mode** — best for specific days and times:
```javascript
// Weekdays at 9 AM
{
  mode: "daysAndHours",
  days: ["monday", "tuesday", "wednesday", "thursday", "friday"],
  hour: 9,
  minute: 0
}

// Every Monday at 6 PM
{
  mode: "daysAndHours",
  days: ["monday"],
  hour: 18,
  minute: 0
}
```

**Cron mode (advanced)** — best for complex schedules:
```javascript
// Every weekday at 9 AM
{
  mode: "cron",
  expression: "0 9 * * 1-5"
}

// First day of every month at midnight
{
  mode: "cron",
  expression: "0 0 1 * *"
}

// Every 15 minutes during business hours (9 AM - 5 PM) on weekdays
{
  mode: "cron",
  expression: "*/15 9-17 * * 1-5"
}
```

Cron format: `minute hour day month weekday`, where `*` = any value, `*/15` = every 15 units, `1-5` = a range (Monday–Friday), `1,15` = specific values.

Cron examples:
```
0 */6 * * *      Every 6 hours
0 9,17 * * *     At 9 AM and 5 PM daily
0 0 * * 0        Every Sunday at midnight
*/30 * * * *     Every 30 minutes
0 0 1,15 * *     1st and 15th of each month
```

## Common Use Cases

**1. Daily reports** — `Schedule → Fetch data → Aggregate → Format → Email`

Example (sales report):
```
1. Schedule (daily at 9 AM)

2. Postgres (query yesterday's sales)
   SELECT date, SUM(amount) as total, COUNT(*) as orders
   FROM orders
   WHERE date = CURRENT_DATE - INTERVAL '1 day'
   GROUP BY date

3. Code (calculate metrics)
   - Total revenue
   - Order count
   - Average order value
   - Comparison to previous day

4. Set (format email body)
   Subject: Daily Sales Report - {{$json.date}}
   Body: Formatted HTML with metrics

5. Email (send to team@company.com)

6. Slack (post summary to #sales)
```

**2. Data synchronization** — `Schedule → Fetch from source → Transform → Write to target`

Example (CRM to data warehouse sync):
```
1. Schedule (every hour)

2. Set (store last sync time)
   SELECT MAX(synced_at) FROM sync_log

3. HTTP Request (fetch new CRM contacts since last sync)
   GET /api/contacts?updated_since={{$json.last_sync}}

4. IF (check if new records exist)

5. Set (transform CRM schema to warehouse schema)

6. Postgres (warehouse - INSERT new contacts)

7. Postgres (UPDATE sync_log SET synced_at = NOW())

8. IF (error occurred)
   └─ Slack (alert #data-team)
```

**3. Monitoring & health checks** — `Schedule → Check endpoints → Alert if down`

Example (website uptime monitor):
```
1. Schedule (every 5 minutes)

2. HTTP Request (GET https://example.com/health)
   - timeout: 10 seconds
   - continueOnFail: true

3. IF (status !== 200 OR response_time > 2000ms)

4. Redis (check alert cooldown - don't spam)
   - Key: alert:website_down
   - TTL: 30 minutes

5. IF (no recent alert sent)

6. [Alert Actions]
   ├─ Slack (notify #ops-team)
   ├─ PagerDuty (create incident)
   ├─ Email (alert@company.com)
   └─ Redis (set alert cooldown)

7. Postgres (log uptime check result)
```

**4. Cleanup & maintenance** — `Schedule → Find old data → Archive/Delete → Report`

Example (database cleanup):
```
1. Schedule (weekly on Sunday at 2 AM)

2. Postgres (find old records)
   SELECT * FROM logs
   WHERE created_at < NOW() - INTERVAL '90 days'
   LIMIT 10000

3. IF (records exist)

4. Code (export to JSON for archive)

5. Google Drive (upload archive file)
   - Filename: logs_archive_{{$now.format('YYYY-MM-DD')}}.json

6. Postgres (DELETE archived records)
   DELETE FROM logs
   WHERE id IN ({{$json.archived_ids}})

7. Slack (report: "Archived X records, deleted Y records")
```

**5. Data enrichment** — `Schedule → Find incomplete records → Enrich → Update`

Example (enrich contacts with company data):
```
1. Schedule (nightly at 3 AM)

2. Postgres (find contacts without company data)
   SELECT id, email, domain FROM contacts
   WHERE company_name IS NULL
   AND created_at > NOW() - INTERVAL '7 days'
   LIMIT 100

3. Split In Batches (10 contacts per batch)

4. HTTP Request (call Clearbit enrichment API)
   - For each contact domain
   - Rate limit: wait 1 second between batches

5. Set (map API response to database schema)

6. Postgres (UPDATE contacts with company data)

7. Wait (1 second - rate limiting)

8. Loop (back to step 4 until all batches processed)

9. Email (summary: "Enriched X contacts")
```

**6. Backup automation** — `Schedule → Export data → Compress → Store → Verify`

Example (database backup):
```
1. Schedule (daily at 2 AM)

2. Code (execute pg_dump)
   const { exec } = require('child_process');
   exec('pg_dump -h db.example.com mydb > backup.sql')

3. Code (compress backup)
   const zlib = require('zlib');
   // Compress backup.sql to backup.sql.gz

4. AWS S3 (upload compressed backup)
   - Bucket: backups
   - Key: db/backup-{{$now.format('YYYY-MM-DD')}}.sql.gz

5. AWS S3 (list old backups)
   - Keep last 30 days only

6. AWS S3 (delete old backups)

7. IF (error occurred)
   ├─ PagerDuty (critical alert)
   └─ Email (backup failed!)
   ELSE
   └─ Slack (#devops: "✅ Backup completed")
```

**7. Content publishing** — `Schedule → Fetch content → Format → Publish`

Example (automated social media posts):
```
1. Schedule (every 3 hours during business hours)
   - Cron: 0 9,12,15,18 * * 1-5

2. Google Sheets (read content queue)
   - Sheet: "Scheduled Posts"
   - Filter: status=pending AND publish_time <= NOW()

3. IF (posts available)

4. HTTP Request (shorten URLs in post)

5. HTTP Request (POST to Twitter API)

6. HTTP Request (POST to LinkedIn API)

7. Google Sheets (update status=published)

8. Slack (notify #marketing: "Posted: {{$json.title}}")
```

## Timezone Considerations

Set the workflow timezone explicitly:
```javascript
// In workflow settings
{
  timezone: "America/New_York"  // EST/EDT
}
```

Common timezones:
```
America/New_York    - Eastern (US)
America/Chicago     - Central (US)
America/Denver      - Mountain (US)
America/Los_Angeles - Pacific (US)
Europe/London       - GMT/BST
Europe/Paris        - CET/CEST
Asia/Tokyo          - JST
Australia/Sydney    - AEDT
UTC                 - Universal Time
```

Handle daylight saving with timezone-aware scheduling:
```javascript
// ❌ Bad: UTC schedule for "9 AM local"
// Will be off by 1 hour during DST transitions

// ✅ Good: Set workflow timezone
{
  timezone: "America/New_York",
  schedule: {
    mode: "daysAndHours",
    hour: 9  // Always 9 AM Eastern, regardless of DST
  }
}
```

## Error Handling

**Pattern 1: Error Trigger workflow**

Main:
```
Schedule → Fetch → Process → Deliver
```
Error:
```
Error Trigger (for main workflow)
  → Set (extract error details)
  → Slack (#ops-team: "❌ Scheduled job failed")
  → Email (admin alert)
  → Postgres (log error for analysis)
```

**Pattern 2: retry with backoff**
```
Schedule → HTTP Request (continueOnFail: true)
  → IF (error)
    ├─ Wait (5 minutes)
    ├─ HTTP Request (retry 1)
    └─ IF (still error)
      ├─ Wait (15 minutes)
      ├─ HTTP Request (retry 2)
      └─ IF (still error)
        └─ Alert admin
```

**Pattern 3: partial failure handling**
```
Schedule → Split In Batches
  → Process (continueOnFail: true)
  → Code (track successes and failures)
  → Report:
    "✅ Processed: 95/100"
    "❌ Failed: 5/100"
```

## Performance Optimization

1. **Batch processing** for large datasets:
```
Schedule → Query (LIMIT 10000)
  → Split In Batches (100 items)
  → Process batch
  → Loop
```
2. **Parallel processing** when operations are independent:
```
Schedule
  ├─ [Branch 1: Update DB]
  ├─ [Branch 2: Send emails]
  └─ [Branch 3: Generate report]
  → Merge (wait for all) → Final notification
```
3. **Skip if already running** — prevent overlapping executions:
```
Schedule → Redis (check lock)
  → IF (lock exists)
    └─ End (skip this execution)
  → ELSE
    ├─ Redis (set lock, TTL 30 min)
    ├─ [Execute workflow]
    └─ Redis (delete lock)
```
4. **Early exit on no data** — don't waste time if nothing to process:
```
Schedule → Query (check if work exists)
  → IF (no results)
    └─ End workflow (exit early)
  → ELSE
    └─ Process data
```

## Monitoring & Logging

**Pattern 1: execution log table**
```sql
CREATE TABLE workflow_executions (
  id SERIAL PRIMARY KEY,
  workflow_name VARCHAR(255),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  status VARCHAR(50),
  records_processed INT,
  error_message TEXT
);
```
Log execution:
```
Schedule
  → Set (record start)
  → [Workflow logic]
  → Postgres (INSERT execution log)
```

**Pattern 2: metrics collection**
```
Schedule → [Execute]
  → Code (calculate metrics)
    - Duration
    - Records processed
    - Success rate
  → HTTP Request (send to monitoring system)
    - Datadog, Prometheus, etc.
```

**Pattern 3: summary notifications** — daily/weekly execution summaries:
```
Schedule (daily at 6 PM) → Query execution logs
  → Code (aggregate today's executions)
  → Email (summary report)
    "Today's Workflow Executions:
     - 24/24 successful
     - 0 failures
     - Avg duration: 2.3 min"
```

## Testing Scheduled Workflows

1. **Use a Manual Trigger for testing** during development, then replace it with the Schedule Trigger once verified.
2. **Test with different simulated times**:
```javascript
// Code node - simulate different times
const testTime = new Date('2024-01-15T09:00:00Z');
return [{ json: { currentTime: testTime } }];
```
3. **Dry-run mode**:
```
Schedule → Set (dryRun: true)
  → IF (dryRun)
    └─ Log what would happen (don't execute)
  → ELSE
    └─ Execute normally
```
4. **Use a shorter interval while testing, then widen it for production**:
```javascript
// Testing: every 1 minute
{ mode: "interval", interval: 1, unit: "minutes" }

// Production: every 1 hour
{ mode: "interval", interval: 1, unit: "hours" }
```

## Common Gotchas

**1. Wrong: ignoring timezone** (`Schedule (9 AM)` — 9 AM in which timezone?). **Correct**: set the workflow timezone explicitly in workflow settings.

**2. Wrong: overlapping executions** — `Schedule (every 5 min) → Long-running task (10 min)` means two executions can run simultaneously. **Correct**: add an execution lock (check a Redis lock before running; skip if locked).

**3. Wrong: no error handling** — `Schedule → API call → Process` can fail silently. **Correct**: pair the main workflow with an Error Trigger workflow that alerts.

**4. Wrong: processing all data at once** — `Schedule → SELECT 1000000 records → Process` risks OOM. **Correct**: `Schedule → SELECT with pagination → Split In Batches → Process`.

**5. Wrong: hardcoded dates** (`query: "SELECT * FROM orders WHERE date = '2024-01-15'"`). **Correct**: dynamic dates (`query: "SELECT * FROM orders WHERE date = CURRENT_DATE - INTERVAL '1 day'"`).

## Checklist for Scheduled Workflows

**Planning**
- [ ] Define schedule frequency (interval, cron, days & hours)
- [ ] Set workflow timezone
- [ ] Estimate execution duration
- [ ] Plan for failures and retries
- [ ] Consider timezone and DST

**Implementation**
- [ ] Configure Schedule Trigger
- [ ] Set workflow timezone in settings
- [ ] Add early exit for no-op cases
- [ ] Implement batch processing for large data
- [ ] Add execution logging

**Error Handling**
- [ ] Create Error Trigger workflow
- [ ] Implement retry logic
- [ ] Add alert notifications
- [ ] Log errors for analysis
- [ ] Handle partial failures gracefully

**Monitoring**
- [ ] Log each execution (start, end, status)
- [ ] Track metrics (duration, records, success rate)
- [ ] Set up daily/weekly summaries
- [ ] Alert on consecutive failures
- [ ] Monitor resource usage

**Testing**
- [ ] Test with Manual Trigger first
- [ ] Verify timezone behavior
- [ ] Test error scenarios
- [ ] Check for overlapping executions
- [ ] Validate output quality

**Deployment**
- [ ] Document workflow purpose
- [ ] Set up monitoring
- [ ] Configure alerts
- [ ] Activate the workflow (⚠️ manual activation is typically required — it can't be triggered by the workflow itself)
- [ ] Test in production with a short interval first
- [ ] Monitor the first few executions

## Advanced Patterns

**Dynamic scheduling** — change behavior based on conditions:
```
Schedule (check every hour) → Code (check if it's time to run)
  → IF (business hours AND weekday)
    └─ Execute workflow
  → ELSE
    └─ Skip
```

**Dependent schedules** — chain workflows:
```
Workflow A (daily 2 AM): Data sync
  → On completion → Trigger Workflow B

Workflow B: Generate report (depends on fresh data)
```

**Conditional execution** — skip based on external factors:
```
Schedule → HTTP Request (check feature flag)
  → IF (feature enabled)
    └─ Execute
  → ELSE
    └─ Skip
```
