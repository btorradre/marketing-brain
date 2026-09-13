"""Reference resolution — turns ANY input (GetHookd URL/ID, generic video URL,
or local path) into a local file, registered as an asset. This used to be
something only replicators that remembered to call gethookd_resolver got;
here it's the universal front door every workflow tool can rely on.

Reuses the existing, proven implementations rather than re-deriving them:
  - GetHookd resolution: _engine/tools/tools/gethookd_resolver.py
  - generic URL download (yt-dlp): ad-watcher's pipeline.py
"""

import importlib.util
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import db

ENGINE_DIR = Path(__file__).resolve().parents[3]  # .../marketing brain/_engine
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gethookd_resolver = _load(
    "ad_engine_gethookd_resolver",
    ENGINE_DIR / "tools" / "tools" / "gethookd_resolver.py",
)
ad_watcher_pipeline = _load(
    "ad_engine_ad_watcher_pipeline",
    Path.home() / ".claude" / "skills" / "ad-watcher" / "pipeline.py",
)


def _is_url(s: str) -> bool:
    p = urlparse(s)
    return p.scheme in {"http", "https"} and bool(p.netloc)


def resolve(input_str: str, brand: str | None = None, concept: str | None = None) -> dict:
    """Resolves input_str to a local video file + registers it as an asset.
    Returns the job dict; job['output']['asset_id'] is the resolved video asset."""
    job_id = db.create_job("resolver", "resolve", brand=brand, concept=concept,
                            input_data={"input": input_str})
    try:
        meta = None
        if gethookd_resolver.is_gethookd_url(input_str):
            local_path, meta = gethookd_resolver.resolve_video_input(input_str)
        elif _is_url(input_str):
            work_dir = DATA_DIR / "downloads" / job_id
            work_dir.mkdir(parents=True, exist_ok=True)
            local_path = str(ad_watcher_pipeline.download(input_str, work_dir))
        else:
            p = Path(input_str).expanduser().resolve()
            if not p.exists():
                raise FileNotFoundError(f"video file not found: {p}")
            local_path = str(p)

        asset_id = db.create_asset(
            job_id, "video", path=local_path,
            source_url=input_str if _is_url(input_str) else None,
            brand=brand, concept=concept, meta=meta,
        )
        db.update_job(job_id, status="success",
                       output_data={"asset_id": asset_id, "local_path": local_path,
                                    "metadata": meta})
    except Exception as exc:  # noqa: BLE001 — surfaced via job.error, not raised to the tool caller
        db.update_job(job_id, status="fail", error=str(exc))
    return db.get_job(job_id)
