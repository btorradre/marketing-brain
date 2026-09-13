"""watch_reference — the MANDATORY head of every adaptation pipeline.

Frame-by-frame beat extraction (ffmpeg scene-change detection), transcript
(captions or Whisper fallback), and a per-beat Gemini descriptive pass (shot
type, composition, on-screen text, motion, audio cues, ad_role). This is the
raw material the strategist reasoning step (see the strategize-ad-adaptation
skill) works from — no downstream tool should generate anything against a
reference it hasn't been through this first.

Thin wrapper around the proven ad-watcher pipeline.py — reused, not rewritten.
"""

import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import db

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ad_watcher_pipeline = _load(
    "ad_engine_ad_watcher_pipeline_watch",
    Path.home() / ".claude" / "skills" / "ad-watcher" / "pipeline.py",
)


def watch(video_ref: str, brand: str | None = None, concept: str | None = None,
          skip_gemini: bool = False) -> dict:
    """video_ref is either a local path or an asset_id from resolve_reference().
    Returns the job dict; job['output']['manifest'] is the full frame-by-frame
    breakdown (overall format/emotion-arc/promise + one entry per beat with
    shot_type, composition, action, on_screen_text, audio_cues, ad_role, vo)."""
    if video_ref.startswith("asset_"):
        asset = db.get_asset(video_ref)
        if asset is None:
            raise ValueError(f"unknown asset_id {video_ref}")
        video_path = asset["path"]
        brand = brand or asset.get("brand")
        concept = concept or asset.get("concept")
    else:
        video_path = video_ref

    video = Path(video_path).expanduser().resolve()
    job_id = db.create_job("gemini", "watch", brand=brand, concept=concept,
                            input_data={"video_path": str(video)})
    work_dir = DATA_DIR / "watch" / job_id
    work_dir.mkdir(parents=True, exist_ok=True)

    try:
        beats = ad_watcher_pipeline.extract_beats(video, work_dir)
        transcript, transcript_label = ad_watcher_pipeline.get_transcript(video, work_dir)
        gemini = ({} if skip_gemini else
                  ad_watcher_pipeline.gemini_pass(video, beats, transcript_label))
        manifest_path = ad_watcher_pipeline.write_manifest(
            work_dir, video_ref, video, beats, transcript, transcript_label, gemini)
        manifest = json.loads(manifest_path.read_text())

        asset_id = db.create_asset(
            job_id, "manifest", path=str(manifest_path), brand=brand, concept=concept,
            meta={"n_beats": len(beats), "transcript_source": transcript_label},
        )
        db.update_job(job_id, status="success", output_data={
            "manifest_asset_id": asset_id,
            "manifest_path": str(manifest_path),
            "n_beats": len(beats),
            "overall": manifest.get("overall", {}),
            "manifest": manifest,
        })
    except Exception as exc:  # noqa: BLE001 — surfaced via job.error
        db.update_job(job_id, status="fail", error=str(exc))
    return db.get_job(job_id)
