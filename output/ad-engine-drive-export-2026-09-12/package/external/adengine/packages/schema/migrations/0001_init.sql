-- adengine 0001_init: tenant data model for Supabase/Postgres.
--
-- Source: PRODUCTIZATION-PLAN.md section 5 + adengine/core/store.py docstring.
-- Every tenant table carries workspace_id (uuid, not null), created_at, updated_at,
-- and a `data jsonb` bag for fields the Store API writes that have no column.
-- Row ids are text (the Store mints "<prefix>_<hex>" ids via adengine.core.ids);
-- workspace ids and auth user ids are uuid.
--
-- RLS: every tenant table is protected by the same four policies, applied by
-- adengine_apply_tenant_policies(). The helper workspace_member()/workspace_role()
-- are SECURITY DEFINER so a policy can read `member` without recursing into
-- member's own RLS.
--
-- Roles (member.role): owner | editor | viewer | agent
--   select: any member          insert/update: owner, editor, agent          delete: owner

create extension if not exists pgcrypto;

-- ------------------------------------------------------------------ helpers
create or replace function adengine_touch_updated_at() returns trigger
language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end $$;

-- ------------------------------------------------------------------ workspace + membership
create table if not exists workspace (
  id          uuid primary key default gen_random_uuid(),
  slug        text not null unique,
  name        text not null,
  plan        text not null default 'free',
  settings    jsonb not null default '{}'::jsonb,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

create table if not exists member (
  id            text primary key default ('mem_' || encode(gen_random_bytes(8), 'hex')),
  workspace_id  uuid not null references workspace(id) on delete cascade,
  user_id       uuid not null,                     -- auth.users.id (Supabase) or the agent's service identity
  email         text,
  role          text not null check (role in ('owner', 'editor', 'viewer', 'agent')),
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  unique (workspace_id, user_id)
);
create index if not exists member_user_idx on member (user_id);

-- The current auth identity. Supabase exposes auth.uid(); elsewhere set
-- `set local request.jwt.claim.sub = '<uuid>'` before queries.
create or replace function adengine_current_uid() returns uuid
language sql stable as $$
  select coalesce(
    nullif(current_setting('request.jwt.claim.sub', true), '')::uuid,
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub')::uuid
  )
$$;

create or replace function workspace_member(ws uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from member m where m.workspace_id = ws and m.user_id = adengine_current_uid())
$$;

create or replace function workspace_role(ws uuid) returns text
language sql stable security definer set search_path = public as $$
  select m.role from member m where m.workspace_id = ws and m.user_id = adengine_current_uid() limit 1
$$;

-- Applies the standard tenant policies + updated_at trigger to one table.
create or replace function adengine_apply_tenant_policies(tbl regclass) returns void
language plpgsql as $$
declare t text := tbl::text;
begin
  execute format('alter table %s enable row level security', tbl);
  execute format('alter table %s force row level security', tbl);
  execute format('drop policy if exists %I on %s', t || '_select', tbl);
  execute format('drop policy if exists %I on %s', t || '_insert', tbl);
  execute format('drop policy if exists %I on %s', t || '_update', tbl);
  execute format('drop policy if exists %I on %s', t || '_delete', tbl);
  execute format('create policy %I on %s for select using (workspace_member(workspace_id))', t || '_select', tbl);
  execute format('create policy %I on %s for insert with check (workspace_role(workspace_id) in (''owner'',''editor'',''agent''))', t || '_insert', tbl);
  execute format('create policy %I on %s for update using (workspace_role(workspace_id) in (''owner'',''editor'',''agent'')) with check (workspace_role(workspace_id) in (''owner'',''editor'',''agent''))', t || '_update', tbl);
  execute format('create policy %I on %s for delete using (workspace_role(workspace_id) = ''owner'')', t || '_delete', tbl);
  execute format('drop trigger if exists %I on %s', t || '_touch', tbl);
  execute format('create trigger %I before update on %s for each row execute function adengine_touch_updated_at()', t || '_touch', tbl);
end $$;

-- workspace and member have their own policies (bootstrap + owner-only membership edits).
alter table workspace enable row level security;
alter table workspace force row level security;
drop policy if exists workspace_select on workspace;
drop policy if exists workspace_insert on workspace;
drop policy if exists workspace_update on workspace;
drop policy if exists workspace_delete on workspace;
create policy workspace_select on workspace for select using (workspace_member(id));
create policy workspace_insert on workspace for insert with check (adengine_current_uid() is not null);
create policy workspace_update on workspace for update using (workspace_role(id) = 'owner');
create policy workspace_delete on workspace for delete using (workspace_role(id) = 'owner');
drop trigger if exists workspace_touch on workspace;
create trigger workspace_touch before update on workspace for each row execute function adengine_touch_updated_at();

alter table member enable row level security;
alter table member force row level security;
drop policy if exists member_select on member;
drop policy if exists member_insert on member;
drop policy if exists member_update on member;
drop policy if exists member_delete on member;
create policy member_select on member for select using (workspace_member(workspace_id));
-- first member of a fresh workspace bootstraps as owner; after that only an owner adds members
create policy member_insert on member for insert with check (
  workspace_role(workspace_id) = 'owner'
  or (user_id = adengine_current_uid() and role = 'owner'
      and not exists (select 1 from member m where m.workspace_id = member.workspace_id))
);
create policy member_update on member for update using (workspace_role(workspace_id) = 'owner');
create policy member_delete on member for delete using (workspace_role(workspace_id) = 'owner');
drop trigger if exists member_touch on member;
create trigger member_touch before update on member for each row execute function adengine_touch_updated_at();

-- ------------------------------------------------------------------ credentials (BYO keys)
create table if not exists credential (
  id             text primary key,
  workspace_id   uuid not null references workspace(id) on delete cascade,
  provider       text not null,                  -- kie | elevenlabs | heygen | gemini | meta | triplewhale ...
  ciphertext     text not null,                  -- encrypted at the app layer, never plaintext
  last_verified  timestamptz,
  balance_cache  jsonb,
  data           jsonb not null default '{}'::jsonb,
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now(),
  unique (workspace_id, provider)
);

-- ------------------------------------------------------------------ brand + product
create table if not exists brand (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  slug          text not null,
  name          text not null,
  brief         jsonb not null default '{}'::jsonb,   -- the 00-brief as fields (avatar, awareness, sophistication, offer)
  house_laws    jsonb not null default '[]'::jsonb,   -- list of law rules, same shape as packages/laws/global.json entries
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  unique (workspace_id, slug)
);

create table if not exists product (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  brand_id      text not null references brand(id) on delete cascade,
  slug          text not null,
  name          text not null,
  truth         jsonb not null default '{}'::jsonb,   -- product_truth record (adengine/product_truth/schema.json)
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  unique (workspace_id, brand_id, slug)
);
create index if not exists product_ws_brand_idx on product (workspace_id, brand_id);

-- ------------------------------------------------------------------ research + copy artifacts
create table if not exists artifact (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  brand_id      text references brand(id) on delete cascade,
  kind          text not null,        -- voc-index | angle-bank | angle | hook | brief | adaptation-plan | mechanism-doc | winner | survey
  name          text not null,
  body          text not null default '',
  frontmatter   jsonb not null default '{}'::jsonb,
  version       integer not null default 1,
  generated_by  text,
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create index if not exists artifact_ws_brand_idx on artifact (workspace_id, brand_id);
create index if not exists artifact_ws_kind_idx on artifact (workspace_id, kind);

create table if not exists reference (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  brand_id      text references brand(id) on delete set null,
  source        text not null,                    -- url or asset id the reference was ingested from
  asset_id      text,                             -- resolved media asset
  manifest      jsonb not null default '{}'::jsonb, -- watch manifest: beats, frames, transcript
  status        text not null default 'ingested', -- ingested | watching | watched | failed
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create index if not exists reference_ws_brand_idx on reference (workspace_id, brand_id);
create index if not exists reference_ws_status_idx on reference (workspace_id, status);

-- ------------------------------------------------------------------ storyboard
-- board.lanes / board.cards / board.edges keep the Store's document form (what push_board
-- writes today); lane and card rows are the normalized form for the editor and approvals.
create table if not exists board (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  brand_id      text references brand(id) on delete cascade,
  slug          text not null,
  title         text not null,
  lanes         jsonb not null default '[]'::jsonb,
  cards         jsonb not null default '[]'::jsonb,
  edges         jsonb not null default '[]'::jsonb,
  version       integer not null default 1,
  status        text not null default 'draft',    -- draft | in_review | approved
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  unique (workspace_id, slug)
);
create index if not exists board_ws_brand_idx on board (workspace_id, brand_id);

create table if not exists lane (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  board_id      text not null references board(id) on delete cascade,
  name          text not null,
  position      integer not null default 0,
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create index if not exists lane_ws_board_idx on lane (workspace_id, board_id);

create table if not exists card (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  board_id      text not null references board(id) on delete cascade,
  lane_id       text references lane(id) on delete set null,
  type          text not null,                    -- text | frame | keyframe | note | timecode ...
  position      jsonb not null default '{}'::jsonb, -- {x, y}
  size          jsonb not null default '{}'::jsonb, -- {w, h}
  content       jsonb not null default '{}'::jsonb,
  asset_id      text,
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create index if not exists card_ws_board_idx on card (workspace_id, board_id);

create table if not exists card_approval (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  board_id      text not null references board(id) on delete cascade,
  card_id       text not null,                    -- card row id or a card id inside board.cards
  member_id     text not null,
  state         text not null check (state in ('approved', 'rejected', 'reroll')),
  note          text,
  at            timestamptz not null default now(),
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create index if not exists card_approval_ws_board_idx on card_approval (workspace_id, board_id);
create index if not exists card_approval_ws_card_idx on card_approval (workspace_id, card_id);

create table if not exists board_version (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  board_id      text not null references board(id) on delete cascade,
  version       integer not null,
  snapshot      jsonb not null,
  created_by    text,
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  unique (board_id, version)
);

create table if not exists comment (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  board_id      text references board(id) on delete cascade,
  card_id       text,
  member_id     text not null,
  body          text not null,
  resolved      boolean not null default false,
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create index if not exists comment_ws_board_idx on comment (workspace_id, board_id);

-- ------------------------------------------------------------------ jobs, assets, cost
create table if not exists job (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  kind          text not null,                    -- ingest | watch | generate | vo | avatar | render ...
  provider      text,
  status        text not null default 'queued',   -- queued | running | done | failed | cancelled
  input         jsonb not null default '{}'::jsonb,
  output        jsonb not null default '{}'::jsonb,
  cost          numeric(12,4) not null default 0,
  parent_id     text references job(id) on delete set null,
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create index if not exists job_ws_status_idx on job (workspace_id, status);
create index if not exists job_ws_kind_idx on job (workspace_id, kind);
create index if not exists job_ws_parent_idx on job (workspace_id, parent_id);

create table if not exists asset (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  kind          text not null,                    -- image | video | audio | file
  mime          text,
  storage_key   text not null,
  url           text,
  meta          jsonb not null default '{}'::jsonb, -- duration, dims, provenance
  job_id        text references job(id) on delete set null,
  duration_ms   integer,
  width         integer,
  height        integer,
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create index if not exists asset_ws_kind_idx on asset (workspace_id, kind);
create index if not exists asset_ws_job_idx on asset (workspace_id, job_id);

create table if not exists cost (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  job_id        text references job(id) on delete set null,
  provider      text not null,
  units         numeric(14,4) not null default 0,
  unit_name     text,
  usd           numeric(12,4) not null default 0,
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create index if not exists cost_ws_job_idx on cost (workspace_id, job_id);
create index if not exists cost_ws_created_idx on cost (workspace_id, created_at);

-- ------------------------------------------------------------------ concepts, editor, ads
create table if not exists concept (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  brand_id      text references brand(id) on delete cascade,
  product_id    text references product(id) on delete set null,
  asset_code    text not null,                    -- naming-convention id, e.g. VEL-WEEKENDER-INVEST-01
  fields        jsonb not null default '{}'::jsonb,
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  unique (workspace_id, asset_code)
);
create index if not exists concept_ws_brand_idx on concept (workspace_id, brand_id);

create table if not exists timeline (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  brand_id      text references brand(id) on delete cascade,
  doc           jsonb not null default '{}'::jsonb, -- packages/timeline document spec
  version       integer not null default 1,
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create index if not exists timeline_ws_brand_idx on timeline (workspace_id, brand_id);

create table if not exists render (
  id                text primary key,
  workspace_id      uuid not null references workspace(id) on delete cascade,
  timeline_id       text not null references timeline(id) on delete cascade,
  timeline_version  integer not null,
  preset            text not null,
  status            text not null default 'queued',
  output_asset_id   text references asset(id) on delete set null,
  job_id            text references job(id) on delete set null,
  cost              numeric(12,4) not null default 0,
  data              jsonb not null default '{}'::jsonb,
  created_at        timestamptz not null default now(),
  updated_at        timestamptz not null default now()
);
create index if not exists render_ws_timeline_idx on render (workspace_id, timeline_id);
create index if not exists render_ws_status_idx on render (workspace_id, status);

create table if not exists style (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  brand_id      text references brand(id) on delete cascade,
  doc           jsonb not null default '{}'::jsonb, -- brand editing style: absorbs corrections
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  unique (workspace_id, brand_id)
);

create table if not exists ad (
  id              text primary key,
  workspace_id    uuid not null references workspace(id) on delete cascade,
  brand_id        text references brand(id) on delete cascade,
  concept_id      text references concept(id) on delete set null,
  naming_id       text not null,                  -- tracker id per naming convention
  concept_family  text,
  axis            text,
  status          text not null default 'draft',  -- draft | live | paused | retired
  data            jsonb not null default '{}'::jsonb,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now(),
  unique (workspace_id, naming_id)
);
create index if not exists ad_ws_brand_idx on ad (workspace_id, brand_id);
create index if not exists ad_ws_status_idx on ad (workspace_id, status);

create table if not exists ad_metric (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  ad_id         text not null references ad(id) on delete cascade,
  source        text not null check (source in ('meta', 'triplewhale', 'manual')),
  period_start  date,
  period_end    date,
  spend         numeric(12,2),
  roas          numeric(10,4),
  cpa           numeric(10,2),
  hook_rate     numeric(6,4),
  hold_rate     numeric(6,4),
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create index if not exists ad_metric_ws_ad_idx on ad_metric (workspace_id, ad_id);

-- ------------------------------------------------------------------ packaged IP
create table if not exists playbook_entitlement (
  id            text primary key,
  workspace_id  uuid not null references workspace(id) on delete cascade,
  playbook_id   text not null,                    -- packages/playbooks/registry.json id
  tier          text not null default 'core',
  granted_at    timestamptz not null default now(),
  expires_at    timestamptz,
  data          jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  unique (workspace_id, playbook_id)
);

-- ------------------------------------------------------------------ RLS on every tenant table
select adengine_apply_tenant_policies(t::regclass) from unnest(array[
  'credential', 'brand', 'product', 'artifact', 'reference',
  'board', 'lane', 'card', 'card_approval', 'board_version', 'comment',
  'job', 'asset', 'cost', 'concept', 'timeline', 'render', 'style',
  'ad', 'ad_metric', 'playbook_entitlement'
]) as t;
