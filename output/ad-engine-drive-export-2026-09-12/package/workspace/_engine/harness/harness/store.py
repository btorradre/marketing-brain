"""Run store. SQLite now; the interface is what ports to Postgres in H3."""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Iterable

from .models import Run

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
  id TEXT PRIMARY KEY,
  workflow TEXT NOT NULL,
  brand TEXT,
  product TEXT,
  status TEXT NOT NULL,
  parent_run TEXT,
  created_by TEXT,
  created_at REAL NOT NULL,
  started_at REAL,
  ended_at REAL,
  cost_usd REAL,
  num_turns INTEGER,
  stop_met INTEGER DEFAULT 0,
  record TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS runs_status ON runs(status, created_at);
CREATE INDEX IF NOT EXISTS runs_brand ON runs(brand, product, created_at);

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id TEXT NOT NULL,
  ts REAL NOT NULL,
  kind TEXT NOT NULL,
  payload TEXT
);
CREATE INDEX IF NOT EXISTS events_run ON events(run_id, id);

CREATE TABLE IF NOT EXISTS evals (
  run_id TEXT NOT NULL,
  check_name TEXT NOT NULL,
  kind TEXT NOT NULL,
  score REAL,
  passed INTEGER,
  detail TEXT,
  ts REAL NOT NULL,
  PRIMARY KEY (run_id, check_name)
);
"""


class RunStore:
    def __init__(self, path: Path):
        self.path = path
        self.conn = sqlite3.connect(str(path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    # -- runs ---------------------------------------------------------
    def save(self, run: Run) -> None:
        self.conn.execute(
            """INSERT INTO runs (id, workflow, brand, product, status, parent_run, created_by,
                   created_at, started_at, ended_at, cost_usd, num_turns, stop_met, record)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET status=excluded.status,
                   started_at=excluded.started_at, ended_at=excluded.ended_at,
                   cost_usd=excluded.cost_usd, num_turns=excluded.num_turns,
                   stop_met=excluded.stop_met, record=excluded.record""",
            (run.id, run.workflow, run.brand, run.product, run.status, run.parent_run,
             run.created_by, run.created_at, run.started_at, run.ended_at, run.cost_usd,
             run.num_turns, int(run.stop_met), run.to_json()))
        self.conn.commit()

    def get(self, run_id: str) -> Run | None:
        row = self.conn.execute("SELECT record FROM runs WHERE id=?", (run_id,)).fetchone()
        return Run.from_dict(json.loads(row["record"])) if row else None

    def list(self, status: str | None = None, brand: str | None = None,
             limit: int = 50) -> list[Run]:
        q, args = "SELECT record FROM runs", []
        conds = []
        if status:
            conds.append("status=?"); args.append(status)
        if brand:
            conds.append("brand=?"); args.append(brand)
        if conds:
            q += " WHERE " + " AND ".join(conds)
        q += " ORDER BY created_at DESC LIMIT ?"; args.append(limit)
        return [Run.from_dict(json.loads(r["record"])) for r in self.conn.execute(q, args)]

    def next_queued(self) -> Run | None:
        row = self.conn.execute(
            "SELECT record FROM runs WHERE status='queued' ORDER BY created_at LIMIT 1").fetchone()
        return Run.from_dict(json.loads(row["record"])) if row else None

    def recent_done(self, brand: str | None, product: str | None, limit: int) -> list[Run]:
        q, args = "SELECT record FROM runs WHERE status IN ('done','blocked_on_human')", []
        if brand:
            q += " AND brand=?"; args.append(brand)
        if product:
            q += " AND product=?"; args.append(product)
        q += " ORDER BY ended_at DESC LIMIT ?"; args.append(limit)
        return [Run.from_dict(json.loads(r["record"])) for r in self.conn.execute(q, args)]

    # -- events -------------------------------------------------------
    def event(self, run_id: str, kind: str, payload: dict | None = None) -> None:
        self.conn.execute("INSERT INTO events (run_id, ts, kind, payload) VALUES (?,?,?,?)",
                          (run_id, time.time(), kind, json.dumps(payload or {}, default=str)))
        self.conn.commit()

    def events(self, run_id: str) -> Iterable[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM events WHERE run_id=? ORDER BY id", (run_id,))

    # -- evals --------------------------------------------------------
    def eval(self, run_id: str, check_name: str, kind: str, score: float | None,
             passed: bool | None, detail: str = "") -> None:
        self.conn.execute(
            """INSERT OR REPLACE INTO evals (run_id, check_name, kind, score, passed, detail, ts)
               VALUES (?,?,?,?,?,?,?)""",
            (run_id, check_name, kind, score, None if passed is None else int(passed),
             detail, time.time()))
        self.conn.commit()

    def evals(self, run_id: str) -> list[dict]:
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM evals WHERE run_id=? ORDER BY check_name", (run_id,))]
