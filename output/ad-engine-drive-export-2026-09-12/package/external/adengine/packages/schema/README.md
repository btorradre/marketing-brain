# packages/schema

SQL migrations for the hosted store (Supabase/Postgres) plus seed data.

```
migrations/0001_init.sql        tenant data model, RLS on every tenant table
seed/product_truth/*.json       product-truth records extracted from the vault skills
                                (scripts/extract_product_truth.py); loaded into product.truth
```

## Data model

One tenant boundary: `workspace_id` on every row. `workspace` and `member` are the
root; every other table is a tenant table with `workspace_id uuid not null`,
`created_at`, `updated_at`, and a `data jsonb` bag for fields the Store API writes
that have no dedicated column. Row ids are `text` because the engine mints them
(`brand_18f...`, `job_18f...`) via `adengine.core.ids.new_id`.

Tables: `workspace`, `member`, `credential`, `brand`, `product`, `artifact`,
`reference`, `board`, `lane`, `card`, `card_approval`, `board_version`, `comment`,
`job`, `asset`, `cost`, `concept`, `timeline`, `render`, `style`, `ad`, `ad_metric`,
`playbook_entitlement`.

Store collection to table mapping (see `adengine/core/pg_store.py`): every
collection name is the table name, except `approval` which maps to `card_approval`.

## RLS

`adengine_apply_tenant_policies(tbl)` enables and forces RLS and creates four
policies per table:

| policy | rule |
|---|---|
| select | `workspace_member(workspace_id)` |
| insert | role in owner, editor, agent |
| update | role in owner, editor, agent |
| delete | role = owner |

`workspace_member(ws uuid)` and `workspace_role(ws uuid)` are `security definer`
helpers that read `member` for the current auth identity. The identity comes from
`auth.uid()` on Supabase (read via the `request.jwt.claim.sub` / `request.jwt.claims`
settings, so the same SQL runs on plain Postgres when the app sets those before a
query). The engine's own service role bypasses RLS and scopes every query itself
from the auth context (`adengine.core.auth`).

## Applying with the Supabase CLI

```
supabase login
supabase link --project-ref <ref>
# the CLI reads supabase/migrations/, so point it at ours:
mkdir -p supabase/migrations && ln -sf ../../packages/schema/migrations/0001_init.sql supabase/migrations/0001_init.sql
supabase db push
```

Local: `supabase start && supabase db reset` runs every migration against the local
stack. Plain Postgres: `psql "$DATABASE_URL" -f packages/schema/migrations/0001_init.sql`.

The migration is idempotent (`create table if not exists`, `drop policy if exists`),
so re-running it is safe.

## Phase 1

Phase 0 ships `LocalStore` (JSON on disk). Phase 1 sets `ADENGINE_STORE=postgres`
and `DATABASE_URL`, and `adengine.core.store.get_store()` returns
`PostgresStore`, which maps the generic Store API (`put`, `get`, `find`, `delete`)
onto these tables: known columns become columns, everything else lands in `data`.
Blobs move to object storage (`OBJECT_STORE_URL`), keyed by `asset.storage_key`.
