"""Local session state. Models propose scores; deterministic code owns transitions."""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import math
from pathlib import Path
import sqlite3
import subprocess
import shutil
import time
import uuid

from adengine.quality import load_rubric, evaluate_review

STAGES = {"script": ("copy",), "storyboard": ("copy", "storyboard"),
          "render": ("copy", "storyboard", "edit")}
ARTIFACT_KINDS = {"copy": "script", "storyboard": "storyboard", "edit": "render"}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _positive(value, name):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite")
    return value


class RunStore:
    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.db = self.root / "runs.sqlite3"
        with self.transaction() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, data TEXT NOT NULL)")
            conn.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, run_id TEXT NOT NULL, at REAL NOT NULL, kind TEXT NOT NULL, data TEXT NOT NULL)")

    @contextmanager
    def transaction(self):
        conn = sqlite3.connect(self.db, timeout=30)
        try:
            conn.execute("BEGIN IMMEDIATE")
            yield conn
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_run(self, run_id: str) -> dict:
        with self.transaction() as conn:
            return self._get(conn, run_id)

    @staticmethod
    def _get(conn, run_id):
        row = conn.execute("SELECT data FROM runs WHERE id = ?", (run_id,)).fetchone()
        if not row:
            raise ValueError(f"Unknown run: {run_id}")
        return json.loads(row[0])

    @staticmethod
    def _save(conn, run, kind, detail=None):
        conn.execute("INSERT INTO runs VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET data=excluded.data", (run["id"], json.dumps(run)))
        conn.execute("INSERT INTO events(run_id, at, kind, data) VALUES (?, ?, ?, ?)", (run["id"], time.time(), kind, json.dumps(detail or {})))

    def events(self, run_id):
        with self.transaction() as conn:
            return [{"at": row[0], "kind": row[1], "data": json.loads(row[2])} for row in conn.execute("SELECT at, kind, data FROM events WHERE run_id=? ORDER BY id", (run_id,))]


def _snapshot(store, run_id, round_number, packet_path, rubrics=None):
    source = Path(packet_path).resolve()
    packet = json.loads(source.read_text())
    if packet.get("stage") not in STAGES:
        raise ValueError("stage must be script, storyboard, or render")
    if not isinstance(packet.get("creator_id"), str) or not packet["creator_id"].strip():
        raise ValueError("creator_id is required")
    if any(key in packet.get("context", {}) for key in ("artifact", "render")):
        raise ValueError("context cannot use reserved artifact or render roles")
    required = [ARTIFACT_KINDS[key] for key in STAGES[packet["stage"]]]
    if any(key not in packet.get("artifacts", {}) for key in required):
        raise ValueError(f"Required artifacts: {required}")
    folder = store.root / run_id / f"round-{round_number}-{uuid.uuid4().hex[:8]}"
    # All inputs copied before registering the round; failed snapshots never complete a run.
    folder.mkdir(parents=True, exist_ok=False)
    snapshot = {"number": round_number, "stage": packet["stage"], "creator_id": packet["creator_id"], "artifacts": {}, "context": {}, "reviews": {}, "results": {}}
    for group in ("artifacts", "context"):
        for key, raw_path in packet.get(group, {}).items():
            if not isinstance(raw_path, str):
                raise ValueError(f"{group}.{key} must be a local file path")
            src = (source.parent / raw_path).resolve()
            if not src.is_file():
                raise ValueError(f"Missing evidence file: {raw_path}")
            data = src.read_bytes()
            sha = hashlib.sha256(data).hexdigest()
            dst = folder / f"{sha}{src.suffix}"
            dst.write_bytes(data)
            snapshot[group][key] = {"path": str(dst), "source_path": str(src), "packet_path": raw_path, "sha256": sha}
    snapshot["rubrics"] = rubrics or {key: load_rubric(key) for key in STAGES[packet["stage"]]}
    snapshot["rubric_hashes"] = {key: hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest() for key, value in snapshot["rubrics"].items()}
    snapshot["packet_hash"] = hashlib.sha256(json.dumps({k: snapshot[k] for k in ("stage", "creator_id", "artifacts", "context", "rubric_hashes")}, sort_keys=True).encode()).hexdigest()
    (folder / "packet.json").write_text(json.dumps(snapshot, indent=2))
    return snapshot


def start_run(store: RunStore, packet_path, *, max_rounds=3, max_budget_usd=10.0):
    if isinstance(max_rounds, bool) or not isinstance(max_rounds, int) or max_rounds < 1:
        raise ValueError("max_rounds must be a positive integer")
    _positive(max_budget_usd, "max_budget_usd")
    run_id = uuid.uuid4().hex
    snapshot = _snapshot(store, run_id, 1, packet_path)
    run = {"id": run_id, "status": "awaiting_reviews", "max_rounds": max_rounds,
           "max_budget_usd": max_budget_usd, "spent_usd": 0.0, "reserved_usd": 0.0,
           "attempt": None, "rounds": [snapshot], "final_delivery_ready": False}
    with store.transaction() as conn:
        store._save(conn, run, "started")
    return run


def validate_snapshot(snapshot):
    for group in ("artifacts", "context"):
        for evidence in snapshot[group].values():
            path = Path(evidence["path"])
            if not path.is_file() or digest(path) != evidence["sha256"]:
                raise ValueError("Pinned evidence is missing or changed; submit a new revision")
    for key, rubric in snapshot["rubrics"].items():
        if hashlib.sha256(json.dumps(rubric, sort_keys=True).encode()).hexdigest() != snapshot["rubric_hashes"][key]:
            raise ValueError("Pinned rubric was changed")


def _aggregate(run):
    current = run["rounds"][-1]
    if any(key not in current["results"] for key in STAGES[current["stage"]]):
        run["status"] = "awaiting_reviews"
        return
    states = [value["status"] for value in current["results"].values()]
    if all(state == "pass" for state in states):
        run["status"] = "passed"
        run["final_delivery_ready"] = current["stage"] == "render"
    elif len(run["rounds"]) >= run["max_rounds"]:
        run["status"] = "round_limit"
    elif "needs_evidence" in states:
        run["status"] = "needs_evidence"
    else:
        run["status"] = "needs_revision"


def ingest_review(store: RunStore, run_id: str, review: dict, *, reviewer_id: str, round_number=None, attempt_id=None):
    if not isinstance(review, dict) or not isinstance(review.get("criteria"), dict):
        raise ValueError("Review must be an object with a criteria object")
    if any(not isinstance(item, dict) or not isinstance(item.get("evidence", []), list) for item in review["criteria"].values()):
        raise ValueError("Review criteria must contain evidence arrays")
    if any(not isinstance(evidence, dict) for item in review["criteria"].values() for evidence in item.get("evidence", [])):
        raise ValueError("Evidence citations must be objects")
    with store.transaction() as conn:
        run = store._get(conn, run_id)
        current = run["rounds"][-1]
        if run["attempt"] and attempt_id != run["attempt"]["id"]:
            raise ValueError("A reviewer session is active; cannot ingest concurrently")
        if run["status"] not in ("awaiting_reviews", "reviewing"):
            raise ValueError(f"Run is {run['status']}; create a revision before more reviews")
        if round_number is not None and round_number != current["number"]:
            raise ValueError("Review belongs to a stale round")
        validate_snapshot(current)
        if not reviewer_id or review.get("reviewer_id") != reviewer_id or reviewer_id == current["creator_id"]:
            raise ValueError("Review identity must match an independent trusted reviewer")
        if any(prior["reviewer_id"] == reviewer_id for prior in current["reviews"].values()):
            raise ValueError("Each rubric requires a separate independent reviewer")
        if review.get("packet_hash") != current["packet_hash"]:
            raise ValueError("Review packet hash does not match the current evidence context")
        key = review.get("rubric_id")
        if key not in STAGES[current["stage"]]:
            raise ValueError("Unexpected reviewer rubric")
        if key in current["reviews"]:
            raise ValueError("Review already persisted; use a new revision to replace it")
        artifact_kind = ARTIFACT_KINDS[key]
        expected_hash = current["artifacts"][artifact_kind]["sha256"]
        if review.get("artifact_hash") != expected_hash:
            raise ValueError("Review artifact hash does not match the current round")
        all_evidence = list(current["artifacts"].values()) + list(current["context"].values())
        known_paths = {item[field] for item in all_evidence for field in ("path", "source_path", "packet_path")}
        roles = {"artifact": [current["artifacts"][artifact_kind]]}
        for role, item in current["context"].items():
            roles.setdefault(role, []).append(item)
        if "render" in current["artifacts"]:
            roles.setdefault("render", []).append(current["artifacts"]["render"])
        for criterion in review.get("criteria", {}).values():
            for evidence in criterion.get("evidence", []):
                if evidence.get("path") not in known_paths:
                    raise ValueError(f"Review cites evidence outside the pinned packet: {evidence.get('path')}")
                candidates = roles.get(evidence.get("kind"), [])
                if not any(evidence["path"] in (item["path"], item["source_path"], item["packet_path"]) for item in candidates):
                    raise ValueError(f"Evidence kind does not match pinned source role: {evidence.get('kind')}")
        result = evaluate_review(current["rubrics"][key], review, artifact_hash=expected_hash,
                                 artifact_kind=artifact_kind, creator_id=current["creator_id"])
        if key == "edit":
            media_error = _render_error(current["artifacts"]["render"]["path"])
            if media_error:
                result["status"] = "needs_evidence"
                result["missing_evidence"].append(media_error)
        current["reviews"][key] = review
        current["results"][key] = result
        _aggregate(run)
        store._save(conn, run, "review_persisted", {"rubric_id": key, "status": result["status"]})
    return run



def _render_error(path):
    """A render role alone cannot turn a script/empty file into final video evidence."""
    probe = shutil.which("ffprobe")
    if not probe:
        return "ffprobe unavailable: rendered video stream is unverified"
    try:
        result = subprocess.run([probe, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_type,width,height:format=duration", "-of", "json", path], capture_output=True, text=True, timeout=15)
        data = json.loads(result.stdout)
        streams = data.get("streams", [])
        if result.returncode or not streams or not streams[0].get("width") or not streams[0].get("height") or float(data.get("format", {}).get("duration", 0)) <= 0:
            return "Rendered artifact is not a decodable video with positive duration"
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return "Rendered video probe failed; media evidence is unverified"
    return None

def revise_run(store: RunStore, run_id: str, packet_path, *, attempt_id=None, cost_usd=None, revision_summary=None, expected_packet_hash=None):
    with store.transaction() as conn:
        run = store._get(conn, run_id)
        active = run["attempt"]
        owns_revision = active and active["id"] == attempt_id and active["purpose"] == "revision"
        if active and not owns_revision:
            raise ValueError("Reviewer session is active")
        if attempt_id and not owns_revision:
            raise ValueError("Revision attempt does not own this run")
        if not owns_revision and run["status"] not in ("needs_revision", "needs_evidence", "passed", "failed"):
            raise ValueError(f"Cannot revise run in state {run['status']}")
        if len(run["rounds"]) >= run["max_rounds"]:
            raise ValueError("Maximum review rounds reached; human escalation required")
        previous = run["rounds"][-1]
        if expected_packet_hash is not None and expected_packet_hash != previous["packet_hash"]:
            raise ValueError("Revision parent packet changed")
        snapshot = _snapshot(store, run_id, len(run["rounds"]) + 1, packet_path, previous["rubrics"])
        if snapshot["stage"] != previous["stage"]:
            raise ValueError("A stage change requires a new run")
        old_hashes = {k: v["sha256"] for group in ("artifacts", "context") for k, v in previous[group].items()}
        new_hashes = {k: v["sha256"] for group in ("artifacts", "context") for k, v in snapshot[group].items()}
        if old_hashes == new_hashes:
            raise ValueError("Revision must change an artifact or evidence")
        if owns_revision:
            if cost_usd is not None and (isinstance(cost_usd, bool) or not isinstance(cost_usd, (float, int)) or not math.isfinite(cost_usd) or cost_usd < 0):
                raise ValueError("Invalid provider cost")
            charged = active["budget_usd"] if cost_usd is None else cost_usd
            run["spent_usd"] += charged
            run["reserved_usd"] -= active["budget_usd"]
            run["attempt"] = None
        run["rounds"].append(snapshot)
        run.pop("loop_stop_reason", None)
        run["status"], run["final_delivery_ready"] = "awaiting_reviews", False
        store._save(conn, run, "revision_started", {"round": snapshot["number"], "summary": revision_summary,
            "parent_packet_hash": previous["packet_hash"], "charged_usd": charged if owns_revision else 0})
    return run


def reserve_attempt(store, run_id, budget_usd, *, purpose="review"):
    if purpose not in ("review", "revision"):
        raise ValueError("Unknown session purpose")
    _positive(budget_usd, "budget_usd")
    with store.transaction() as conn:
        run = store._get(conn, run_id)
        expected = ("awaiting_reviews",) if purpose == "review" else ("needs_revision",)
        if run["attempt"] or run["status"] not in expected:
            raise ValueError("Run cannot be claimed for review")
        if run["spent_usd"] + run["reserved_usd"] + budget_usd > run["max_budget_usd"] + 1e-9:
            raise ValueError("Total review budget exhausted")
        attempt = {"id": uuid.uuid4().hex, "budget_usd": budget_usd, "started_at": time.time(), "session_ids": [], "purpose": purpose}
        run["attempt"] = attempt
        run["reserved_usd"] += budget_usd
        run["status"] = "reviewing"
        store._save(conn, run, "attempt_reserved", attempt)
    return run


def finish_attempt(store, run_id, attempt_id, *, cost_usd=None, error=None):
    with store.transaction() as conn:
        run = store._get(conn, run_id)
        attempt = run["attempt"]
        if not attempt or attempt["id"] != attempt_id:
            raise ValueError("Attempt does not own this run")
        if cost_usd is not None and (isinstance(cost_usd, bool) or not math.isfinite(cost_usd) or cost_usd < 0):
            raise ValueError("Invalid provider cost")
        # Unknown cost consumes the entire reservation, including interruptions.
        charged = attempt["budget_usd"] if cost_usd is None else cost_usd
        run["spent_usd"] += charged
        run["reserved_usd"] -= attempt["budget_usd"]
        run["attempt"] = None
        _aggregate(run)
        if error:
            run["status"], run["final_delivery_ready"] = "failed", False
        store._save(conn, run, "attempt_finished", {"charged_usd": charged, "cost_known": cost_usd is not None, "error": error})
    return run
