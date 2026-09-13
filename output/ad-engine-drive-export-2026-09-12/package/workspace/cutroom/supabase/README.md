# Supabase

Cutroom uses two separate Supabase surfaces:

| Surface | What it holds | How it is reached |
|---|---|---|
| **Storage** (bucket `cutroom`, private) | Board JSON + board images. The live source of truth. | `supabase_store.py` locally, `web/api/*.js` on Vercel. Both use `SUPABASE_SECRET_KEY`. |
| **Postgres** (tables in `migrations/`) | Relational mirror of projects/boards, plus a `cutroom_comments` table for future per-card comments. | Deployed by CI. Not yet populated. |

The Postgres layer has **never been applied** — it was blocked on dashboard
access. The workflow below is what finally applies it.

## How migrations deploy

`.github/workflows/supabase-migrations.yml` runs on every push to `main` that
touches `supabase/migrations/`, and can be run by hand from the Actions tab
(`workflow_dispatch`). It installs the Supabase CLI, links to the project, prints
the pending migration list, then runs `supabase db push`.

Every migration must stay idempotent (`create table if not exists`, `create or
replace`, `drop ... if exists`) so a re-run is always safe.

## One-time setup

Three repository secrets are required. Settings → Secrets and variables →
Actions → New repository secret:

| Secret | Where to get it |
|---|---|
| `SUPABASE_PROJECT_REF` | The subdomain of `SUPABASE_URL` — the `xxxx` in `https://xxxx.supabase.co`. |
| `SUPABASE_ACCESS_TOKEN` | supabase.com/dashboard/account/tokens → *Generate new token*. Account-level, not project-level. |
| `SUPABASE_DB_PASSWORD` | Project Settings → Database → *Database password*. Reset it there if it was never recorded. |

The workflow fails fast with a named error if any of the three is missing, so a
half-configured repo tells you which one it is instead of failing deep inside
the CLI.

## Adding a migration

```
supabase/migrations/<YYYYMMDDHHmmss>_<description>.sql
```

Timestamp prefix, sorted lexically, applied in order. Never edit a migration
that has already been deployed — add a new one.

## Backfill, once

After the first green deploy, copy the existing Storage-only data into the new
tables:

```bash
python3 supabase_store.py migrate
```

## Note on RLS

All three tables have row-level security enabled with **no policies**, so the
publishable/anon key can read nothing. Only the secret key (which bypasses RLS)
can touch them. Keep it that way unless real per-user auth is added.
