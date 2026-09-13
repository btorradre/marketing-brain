# Database Operations

**Pattern structure**: `Trigger → [Query/Read] → [Transform] → [Write/Update] → [Verify/Log]`

**Key characteristic**: data persistence and synchronization.

## Core Components

**1. Trigger** — Schedule (periodic sync/maintenance, most common), Webhook (event-driven writes), or Manual (one-time operations).

**2. Database read nodes** — supported databases include Postgres, MySQL, MongoDB, Microsoft SQL, SQLite, Redis, and others via community nodes.

**3. Transform** — map between different database schemas or formats, typically with Set (field mapping), Code (complex transformations), or Merge (combine data from multiple sources).

**4. Database write nodes** — operations: INSERT (create new records), UPDATE (modify existing records), UPSERT (insert or update), DELETE (remove records).

**5. Verification** — confirm operations succeeded via a query to verify records, a count of rows affected, or logged results.

## Common Use Cases

**1. Data synchronization** — `Schedule → Read Source DB → Transform → Write Target DB → Log`

Example (Postgres to MySQL sync):
```
1. Schedule (every 15 minutes)
2. Postgres (SELECT * FROM users WHERE updated_at > {{$json.last_sync}})
3. IF (check if records exist)
4. Set (map Postgres schema to MySQL schema)
5. MySQL (INSERT or UPDATE users)
6. Postgres (UPDATE sync_log SET last_sync = NOW())
7. Slack (notify: "Synced X users")
```
Incremental sync query:
```sql
SELECT *
FROM users
WHERE updated_at > $1
ORDER BY updated_at ASC
LIMIT 1000
```
Parameters:
```javascript
{
  "parameters": [
    "={{$node['Get Last Sync'].json.last_sync}}"
  ]
}
```

**2. ETL (Extract, Transform, Load)** — `Extract from multiple sources → Transform → Load into warehouse`

Example (consolidate data):
```
1. Schedule (daily at 2 AM)
2. [Parallel branches]
   ├─ Postgres (SELECT orders)
   ├─ MySQL (SELECT customers)
   └─ MongoDB (SELECT products)
3. Merge (combine all data)
4. Code (transform to warehouse schema)
5. Postgres (warehouse - INSERT into fact_sales)
6. Email (send summary report)
```

**3. Data validation & cleanup** — `Schedule → Query → Validate → Update/Delete invalid records`

Example (clean orphaned records):
```
1. Schedule (weekly)
2. Postgres (SELECT users WHERE email IS NULL OR email = '')
3. IF (invalid records exist)
4. Postgres (UPDATE users SET status='inactive' WHERE email IS NULL)
5. Postgres (DELETE FROM users WHERE created_at < NOW() - INTERVAL '1 year' AND status='inactive')
6. Slack (alert: "Cleaned X invalid records")
```

**4. Backup & archive** — `Schedule → Query → Export → Store`

Example (archive old records):
```
1. Schedule (monthly)
2. Postgres (SELECT * FROM orders WHERE created_at < NOW() - INTERVAL '2 years')
3. Code (convert to JSON)
4. Write File (save to archive.json)
5. Google Drive (upload archive)
6. Postgres (DELETE FROM orders WHERE created_at < NOW() - INTERVAL '2 years')
```

**5. Real-time data updates** — `Webhook → Parse → Update Database`

Example (update user status):
```
1. Webhook (receive status update)
2. Postgres (UPDATE users SET status = {{$json.body.status}} WHERE id = {{$json.body.user_id}})
3. IF (rows affected > 0)
4. Redis (SET user:{{$json.body.user_id}}:status {{$json.body.status}})
5. Webhook Response ({"success": true})
```

## Database Node Configuration

### Postgres

SELECT query:
```javascript
{
  operation: "executeQuery",
  query: "SELECT id, name, email FROM users WHERE created_at > $1 LIMIT $2",
  parameters: [
    "={{$json.since_date}}",
    "100"
  ]
}
```

INSERT:
```javascript
{
  operation: "insert",
  table: "users",
  columns: "id, name, email, created_at",
  values: [
    {
      id: "={{$json.id}}",
      name: "={{$json.name}}",
      email: "={{$json.email}}",
      created_at: "={{$now}}"
    }
  ]
}
```

UPDATE:
```javascript
{
  operation: "update",
  table: "users",
  updateKey: "id",
  columns: "name, email, updated_at",
  values: {
    id: "={{$json.id}}",
    name: "={{$json.name}}",
    email: "={{$json.email}}",
    updated_at: "={{$now}}"
  }
}
```

UPSERT (INSERT ... ON CONFLICT):
```javascript
{
  operation: "executeQuery",
  query: `
    INSERT INTO users (id, name, email)
    VALUES ($1, $2, $3)
    ON CONFLICT (id)
    DO UPDATE SET name = $2, email = $3, updated_at = NOW()
  `,
  parameters: [
    "={{$json.id}}",
    "={{$json.name}}",
    "={{$json.email}}"
  ]
}
```

### MySQL

SELECT with JOIN:
```javascript
{
  operation: "executeQuery",
  query: `
    SELECT u.id, u.name, o.order_id, o.total
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.created_at > ?
  `,
  parameters: [
    "={{$json.since_date}}"
  ]
}
```

Bulk INSERT:
```javascript
{
  operation: "insert",
  table: "orders",
  columns: "user_id, total, status",
  values: $json.orders  // Array of objects
}
```

### MongoDB

Find documents:
```javascript
{
  operation: "find",
  collection: "users",
  query: JSON.stringify({
    created_at: { $gt: new Date($json.since_date) },
    status: "active"
  }),
  limit: 100
}
```

Insert document:
```javascript
{
  operation: "insert",
  collection: "users",
  document: JSON.stringify({
    name: $json.name,
    email: $json.email,
    created_at: new Date()
  })
}
```

Update document:
```javascript
{
  operation: "update",
  collection: "users",
  query: JSON.stringify({ _id: $json.user_id }),
  update: JSON.stringify({
    $set: {
      status: $json.status,
      updated_at: new Date()
    }
  })
}
```

## Batch Processing (Database-Specific)

**Pattern 1: Split In Batches** — use when processing large datasets to avoid memory issues:
```
Postgres (SELECT 10000 records)
  → Split In Batches (100 items per batch)
  → Transform
  → MySQL (write batch)
  → Loop (until all processed)
```

**Pattern 2: Paginated queries** — use when the database has millions of records:
```
Set (initialize: offset=0, limit=1000)
  → Loop Start
  → Postgres (SELECT * FROM large_table LIMIT {{$json.limit}} OFFSET {{$json.offset}})
  → IF (records returned)
    ├─ Process records
    ├─ Set (increment offset by 1000)
    └─ Loop back
  └─ [No records] → End
```
Query:
```sql
SELECT * FROM large_table
ORDER BY id
LIMIT $1 OFFSET $2
```

**Pattern 3: Cursor-based pagination** — better performance for large datasets:
```
Set (initialize: last_id=0)
  → Loop Start
  → Postgres (SELECT * FROM table WHERE id > {{$json.last_id}} ORDER BY id LIMIT 1000)
  → IF (records returned)
    ├─ Process records
    ├─ Code (get max id from batch)
    └─ Loop back
  └─ [No records] → End
```
Query:
```sql
SELECT * FROM table
WHERE id > $1
ORDER BY id ASC
LIMIT 1000
```

## Transaction Handling

**Pattern 1: BEGIN/COMMIT/ROLLBACK** — for databases that support transactions:
```javascript
// Node 1: Begin Transaction
{
  operation: "executeQuery",
  query: "BEGIN"
}

// Node 2-N: Your operations
{
  operation: "executeQuery",
  query: "INSERT INTO ...",
  continueOnFail: true
}

// Node N+1: Commit or Rollback
{
  operation: "executeQuery",
  query: "={{$node['Operation'].json.error ? 'ROLLBACK' : 'COMMIT'}}"
}
```

**Pattern 2: Atomic operations** — use database features for atomicity:
```sql
-- Upsert example (atomic)
INSERT INTO inventory (product_id, quantity)
VALUES ($1, $2)
ON CONFLICT (product_id)
DO UPDATE SET quantity = inventory.quantity + $2
```

**Pattern 3: Error rollback** — manual rollback on error:
```
Try Operations:
  Postgres (INSERT orders)
  MySQL (INSERT order_items)

Error Trigger:
  Postgres (DELETE FROM orders WHERE id = {{$json.order_id}})
  MySQL (DELETE FROM order_items WHERE order_id = {{$json.order_id}})
```

## Data Transformation

Schema mapping:
```javascript
// Code node - map schemas
const sourceData = $input.all();

return sourceData.map(item => ({
  json: {
    // Source → Target mapping
    user_id: item.json.id,
    full_name: `${item.json.first_name} ${item.json.last_name}`,
    email_address: item.json.email,
    registration_date: new Date(item.json.created_at).toISOString(),
    // Computed fields
    is_premium: item.json.plan_type === 'pro',
    // Default values
    status: item.json.status || 'active'
  }
}));
```

Data type conversions:
```javascript
// Code node - convert data types
return $input.all().map(item => ({
  json: {
    // String to number
    user_id: parseInt(item.json.user_id),
    // String to date
    created_at: new Date(item.json.created_at),
    // Number to boolean
    is_active: item.json.active === 1,
    // JSON string to object
    metadata: JSON.parse(item.json.metadata || '{}'),
    // Null handling
    email: item.json.email || null
  }
}));
```

Aggregation:
```javascript
// Code node - aggregate data
const items = $input.all();

const summary = items.reduce((acc, item) => {
  const date = item.json.created_at.split('T')[0];
  if (!acc[date]) {
    acc[date] = { count: 0, total: 0 };
  }
  acc[date].count++;
  acc[date].total += item.json.amount;
  return acc;
}, {});

return Object.entries(summary).map(([date, data]) => ({
  json: {
    date,
    count: data.count,
    total: data.total,
    average: data.total / data.count
  }
}));
```

## Performance Optimization

1. **Use indexes**:
```sql
-- Add index for sync queries
CREATE INDEX idx_users_updated_at ON users(updated_at);

-- Add index for lookups
CREATE INDEX idx_orders_user_id ON orders(user_id);
```
2. **Limit result sets** — always use LIMIT:
```sql
-- ✅ Good
SELECT * FROM large_table
WHERE created_at > $1
LIMIT 1000

-- ❌ Bad (unbounded)
SELECT * FROM large_table
WHERE created_at > $1
```
3. **Use prepared statements** — parameterized queries are faster:
```javascript
// ✅ Good - prepared statement
{
  query: "SELECT * FROM users WHERE id = $1",
  parameters: ["={{$json.id}}"]
}

// ❌ Bad - string concatenation
{
  query: "SELECT * FROM users WHERE id = '={{$json.id}}'"
}
```
4. **Batch writes** — write multiple records at once rather than looping individual inserts:
```javascript
// ✅ Good - batch insert
{
  operation: "insert",
  table: "orders",
  values: $json.items  // Array of 100 items
}

// ❌ Bad - individual inserts in loop
// 100 separate INSERT statements
```
5. **Connection pooling** — configure in credentials:
```javascript
{
  host: "db.example.com",
  database: "mydb",
  user: "user",
  password: "pass",
  // Connection pool settings
  min: 2,
  max: 10,
  idleTimeoutMillis: 30000
}
```

## Error Handling

**Pattern 1: Check rows affected**
```
Database Operation (UPDATE users...)
  → IF ({{$json.rowsAffected === 0}})
    └─ Alert: "No rows updated - record not found"
```

**Pattern 2: Constraint violations**
```javascript
// Database operation with continueOnFail: true
{
  operation: "insert",
  continueOnFail: true
}

// Next node: Check for errors
IF ({{$json.error !== undefined}})
  → IF ({{$json.error.includes('duplicate key')}})
    └─ Log: "Record already exists - skipping"
  → ELSE
    └─ Alert: "Database error: {{$json.error}}"
```

**Pattern 3: Rollback on error**
```
Try Operations:
  → Database Write 1
  → Database Write 2
  → Database Write 3

Error Trigger:
  → Rollback Operations
  → Alert Admin
```

## Security Best Practices

**1. Use parameterized queries (prevent SQL injection)**:
```javascript
// ✅ SAFE - parameterized
{
  query: "SELECT * FROM users WHERE email = $1",
  parameters: ["={{$json.email}}"]
}

// ❌ DANGEROUS - SQL injection risk
{
  query: "SELECT * FROM users WHERE email = '={{$json.email}}'"
}
```

**2. Least privilege access**:
```sql
-- ✅ Good - limited permissions
CREATE USER n8n_workflow WITH PASSWORD 'secure_password';
GRANT SELECT, INSERT, UPDATE ON orders TO n8n_workflow;
GRANT SELECT ON users TO n8n_workflow;

-- ❌ Bad - too much access
GRANT ALL PRIVILEGES TO n8n_workflow;
```

**3. Validate input data**:
```javascript
// Code node - validate before write
const email = $json.email;
const name = $json.name;

// Validation
if (!email || !email.includes('@')) {
  throw new Error('Invalid email address');
}

if (!name || name.length < 2) {
  throw new Error('Invalid name');
}

// Sanitization
return [{
  json: {
    email: email.toLowerCase().trim(),
    name: name.trim()
  }
}];
```

**4. Encrypt sensitive data**:
```javascript
// Code node - encrypt before storage
const crypto = require('crypto');

const algorithm = 'aes-256-cbc';
const key = Buffer.from($credentials.encryptionKey, 'hex');
const iv = crypto.randomBytes(16);

const cipher = crypto.createCipheriv(algorithm, key, iv);
let encrypted = cipher.update($json.sensitive_data, 'utf8', 'hex');
encrypted += cipher.final('hex');

return [{
  json: {
    encrypted_data: encrypted,
    iv: iv.toString('hex')
  }
}];
```

## Common Gotchas

**1. Wrong: unbounded queries** (`SELECT * FROM large_table` — could return millions of rows). **Correct**: use LIMIT with an ORDER BY.

**2. Wrong: string concatenation in queries** (`query: "SELECT * FROM users WHERE id = '{{$json.id}}'"`). **Correct**: parameterized queries (`query: "SELECT * FROM users WHERE id = $1", parameters: ["={{$json.id}}"]`).

**3. Wrong: no transaction for multi-step operations** — an INSERT into `orders` followed by a failing INSERT into `order_items` leaves an orphaned order record. **Correct**: wrap in BEGIN / COMMIT (or ROLLBACK on error).

**4. Wrong: processing all items at once** — `SELECT 1000000 records → Process all` risks an out-of-memory error. **Correct**: batch processing — `SELECT records → Split In Batches (1000) → Process → Loop`.

## Checklist for Database Workflows

**Planning**
- [ ] Identify source and target databases
- [ ] Understand schema differences
- [ ] Plan transformation logic
- [ ] Consider batch size for large datasets
- [ ] Design error handling strategy

**Implementation**
- [ ] Use parameterized queries (never concatenate)
- [ ] Add LIMIT to all SELECT queries
- [ ] Use appropriate operation (INSERT/UPDATE/UPSERT)
- [ ] Configure credentials properly
- [ ] Test with small dataset first

**Performance**
- [ ] Add database indexes for queries
- [ ] Use batch operations
- [ ] Implement pagination for large datasets
- [ ] Configure connection pooling
- [ ] Monitor query execution times

**Security**
- [ ] Use parameterized queries (SQL injection prevention)
- [ ] Least privilege database user
- [ ] Validate and sanitize input
- [ ] Encrypt sensitive data
- [ ] Never log sensitive data

**Reliability**
- [ ] Add transaction handling if needed
- [ ] Check rows affected
- [ ] Handle constraint violations
- [ ] Implement retry logic
- [ ] Add Error Trigger workflow
