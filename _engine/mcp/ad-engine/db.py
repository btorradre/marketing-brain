"""Jobs / assets / cost registry for the ad-engine MCP server.

Single SQLite file, no ORM. Every engine wrapper (kie, heygen, elevenlabs, ...)
creates a job row before firing a request and updates it on completion, so
"what's running / what did concept X cost" is answerable from one place
instead of N separate progress.json files.
"""

import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "registry.sqlite3"

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id              TEXT PRIMARY KEY,
    engine          TEXT NOT NULL,          -- kie | heygen | elevenlabs | gdrive | ffmpeg | gemini | resolver
    kind            TEXT NOT NULL,          -- generate | watch | resolve | upload | analyze | ...
    model           TEXT,                   -- e.g. bytedance/seedance-2-5
    status          TEXT NOT NULL DEFAULT 'pending',  -- pending | running | success | fail
    external_task_id TEXT,                  -- provider-side job/task id, for polling
    brand           TEXT,
    concept         TEXT,
    input_json      TEXT,
    output_json     TEXT,
    error           TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS assets (
    id          TEXT PRIMARY KEY,
    job_id      TEXT REFERENCES jobs(id),
    kind        TEXT NOT NULL,      -- video | image | audio | transcript | manifest | plan
    path        TEXT,               -- local filesystem path
    source_url  TEXT,               -- provider URL the asset was pulled from, if any
    brand       TEXT,
    concept     TEXT,
    meta_json   TEXT,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS costs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id        TEXT REFERENCES jobs(id),
    engine        TEXT NOT NULL,
    credits       REAL,
    usd_estimate  REAL,
    note          TEXT,
    created_at    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_brand ON jobs(brand);
CREATE INDEX IF NOT EXISTS idx_assets_job ON assets(job_id);
CREATE INDEX IF NOT EXISTS idx_assets_brand ON assets(brand);
CREATE INDEX IF NOT EXISTS idx_costs_job ON costs(job_id);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


@contextmanager
def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)


def _row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    for key in ("input_json", "output_json", "meta_json"):
        if key in d and d[key]:
            try:
                d[key.replace("_json", "")] = json.loads(d[key])
            except (json.JSONDecodeError, TypeError):
                d[key.replace("_json", "")] = None
            del d[key]
    return d


def create_job(engine: str, kind: str, model: str | None = None,
                brand: str | None = None, concept: str | None = None,
                input_data: dict | None = None) -> str:
    job_id = _new_id("job")
    now = _now()
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO jobs (id, engine, kind, model, status, brand, concept,
                                  input_json, created_at, updated_at)
               VALUES (?, ?, ?, ?, 'pending', ?, ?, ?, ?, ?)""",
            (job_id, engine, kind, model, brand, concept,
             json.dumps(input_data) if input_data is not None else None, now, now),
        )
    return job_id


def update_job(job_id: str, status: str | None = None,
               external_task_id: str | None = None,
               output_data: dict | None = None, error: str | None = None) -> None:
    fields, values = [], []
    if status is not None:
        fields.append("status = ?"); values.append(status)
    if external_task_id is not None:
        fields.append("external_task_id = ?"); values.append(external_task_id)
    if output_data is not None:
        fields.append("output_json = ?"); values.append(json.dumps(output_data))
    if error is not None:
        fields.append("error = ?"); values.append(error)
    if not fields:
        return
    fields.append("updated_at = ?"); values.append(_now())
    values.append(job_id)
    with get_conn() as conn:
        conn.execute(f"UPDATE jobs SET {', '.join(fields)} WHERE id = ?", values)


def get_job(job_id: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        return _row_to_dict(row) if row else None


def list_jobs(status: str | None = None, brand: str | None = None,
              engine: str | None = None, limit: int = 50) -> list[dict]:
    clauses, values = [], []
    if status: clauses.append("status = ?"); values.append(status)
    if brand: clauses.append("brand = ?"); values.append(brand)
    if engine: clauses.append("engine = ?"); values.append(engine)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT * FROM jobs {where} ORDER BY created_at DESC LIMIT ?",
            (*values, limit),
        ).fetchall()
        return [_row_to_dict(r) for r in rows]


def create_asset(job_id: str | None, kind: str, path: str | None = None,
                  source_url: str | None = None, brand: str | None = None,
                  concept: str | None = None, meta: dict | None = None) -> str:
    asset_id = _new_id("asset")
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO assets (id, job_id, kind, path, source_url, brand, concept,
                                    meta_json, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (asset_id, job_id, kind, path, source_url, brand, concept,
             json.dumps(meta) if meta is not None else None, _now()),
        )
    return asset_id


def get_asset(asset_id: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM assets WHERE id = ?", (asset_id,)).fetchone()
        return _row_to_dict(row) if row else None


def list_assets(job_id: str | None = None, brand: str | None = None,
                 kind: str | None = None, concept: str | None = None,
                 limit: int = 50) -> list[dict]:
    clauses, values = [], []
    if job_id: clauses.append("job_id = ?"); values.append(job_id)
    if brand: clauses.append("brand = ?"); values.append(brand)
    if kind: clauses.append("kind = ?"); values.append(kind)
    if concept: clauses.append("concept = ?"); values.append(concept)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT * FROM assets {where} ORDER BY created_at DESC LIMIT ?",
            (*values, limit),
        ).fetchall()
        return [_row_to_dict(r) for r in rows]


def record_cost(job_id: str | None, engine: str, credits: float | None = None,
                 usd_estimate: float | None = None, note: str | None = None) -> None:
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO costs (job_id, engine, credits, usd_estimate, note, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (job_id, engine, credits, usd_estimate, note, _now()),
        )


def cost_summary(brand: str | None = None, concept: str | None = None) -> dict:
    """Rolls up spend, joined through jobs so it can be filtered by brand/concept."""
    clauses, values = [], []
    if brand: clauses.append("j.brand = ?"); values.append(brand)
    if concept: clauses.append("j.concept = ?"); values.append(concept)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with get_conn() as conn:
        rows = conn.execute(
            f"""SELECT c.engine, SUM(c.credits) as total_credits,
                       SUM(c.usd_estimate) as total_usd, COUNT(*) as n
                FROM costs c JOIN jobs j ON c.job_id = j.id
                {where}
                GROUP BY c.engine""",
            values,
        ).fetchall()
        return {r["engine"]: dict(r) for r in rows}
