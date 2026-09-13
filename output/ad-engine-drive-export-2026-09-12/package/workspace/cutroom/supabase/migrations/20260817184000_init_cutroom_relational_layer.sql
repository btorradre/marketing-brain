-- Cutroom relational layer.
--
-- Applied automatically by .github/workflows/supabase-migrations.yml on every
-- push to main that touches supabase/migrations/. Idempotent, so re-running is
-- safe. After the first successful deploy, backfill the existing Storage-only
-- data once with:  python3 cutroom/supabase_store.py migrate
create table if not exists cutroom_projects (
  id text primary key,
  name text not null,
  created_at timestamptz not null default now()
);

create table if not exists cutroom_boards (
  id text primary key,
  title text not null,
  project text not null default 'general',
  cards jsonb not null default '[]'::jsonb,
  edges jsonb not null default '[]'::jsonb,
  updated_at timestamptz not null default now()
);
create index if not exists cutroom_boards_project_idx on cutroom_boards (project);

-- ready for future features (comments on cards, per-user auth via Supabase Auth)
create table if not exists cutroom_comments (
  id uuid primary key default gen_random_uuid(),
  board_id text not null references cutroom_boards(id) on delete cascade,
  card_id text,
  author text not null default '',
  body text not null,
  created_at timestamptz not null default now()
);
create index if not exists cutroom_comments_board_idx on cutroom_comments (board_id);

-- keep updated_at fresh on every write
create or replace function cutroom_touch() returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end $$;
drop trigger if exists cutroom_boards_touch on cutroom_boards;
create trigger cutroom_boards_touch before update on cutroom_boards
  for each row execute function cutroom_touch();

-- lock everything down: RLS on, no public policies.
-- The secret (service) key bypasses RLS, so only our servers can touch these.
alter table cutroom_projects enable row level security;
alter table cutroom_boards enable row level security;
alter table cutroom_comments enable row level security;
