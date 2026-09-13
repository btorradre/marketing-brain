#!/usr/bin/env python3
"""POV profile over the universal scene replicator.

THE ENGINE LIVES ELSEWHERE. As of 2026-08-03 all scene detection, per-scene
keyframe generation, animation and assembly is handled by:

    _engine/pipelines/scene_replicator.py

That runner is format-agnostic and takes ANY reference ad. This file is only a
thin POV profile over it: it injects the POV doctrine defaults into job.json
and forwards the subcommand. There is deliberately no duplicated kie.ai
plumbing here — four drifting copies of it across skills was the problem this
consolidation fixed.

POV defaults injected (only when job.json does not already set them):
  footer_preset  "ugc_text" when overlay/baked text is in play, else "ugc"
                 (the raw-iPhone, no-cuts, text-stays-fixed footer)
  max_seconds    8       POV doctrine: the assembled ad stays short
  upload_path    "pov-trend-factory"
  image_aspect_ratio "2:3"  (kie GPT Image 2 has no 9:16; the runner crops)

Usage is identical to the shared runner:
  pov_factory.py fetch   <url-or-path> <out_dir>
  pov_factory.py scan    <out_dir> [--threshold ...] [--max-scene ...]
  pov_factory.py image   <job.json>
  pov_factory.py animate <job.json>
  pov_factory.py finish  <job.json>

Anything not POV-specific belongs in the shared runner, not here.
"""
import json
import os
import subprocess
import sys

VAULT = "/Users/brooksorradre2/Documents/marketing brain"
RUNNER = os.path.join(VAULT, "_engine/pipelines/scene_replicator.py")

POV_MAX_SECONDS = 8   # POV doctrine. Override by setting max_seconds in job.json.


def apply_pov_defaults(job_path):
    """Inject POV defaults into a job file, without clobbering explicit values."""
    try:
        job = json.loads(open(job_path).read())
    except (OSError, ValueError) as e:
        sys.exit(f"could not read {job_path}: {e}")

    changed = []
    if "footer_preset" not in job and "footer" not in job:
        # A baked/overlaid caption needs the "text stays pixel-fixed" line.
        any_text = bool(job.get("overlay_text")) or any(
            s.get("bake_text") for s in job.get("scenes", []))
        job["footer_preset"] = "ugc_text" if any_text else "ugc"
        changed.append(f"footer_preset={job['footer_preset']}")
    if "max_seconds" not in job:
        job["max_seconds"] = POV_MAX_SECONDS
        changed.append(f"max_seconds={POV_MAX_SECONDS}")
    elif job["max_seconds"] and float(job["max_seconds"]) > POV_MAX_SECONDS:
        print(f"NOTE: max_seconds is {job['max_seconds']}s, above the {POV_MAX_SECONDS}s "
              f"POV default — set deliberately in job.json")
    if "upload_path" not in job:
        job["upload_path"] = "pov-trend-factory"
        changed.append("upload_path=pov-trend-factory")
    if "image_aspect_ratio" not in job:
        job["image_aspect_ratio"] = "2:3"
        changed.append("image_aspect_ratio=2:3")

    if changed:
        json.dump(job, open(job_path, "w"), indent=1)
        print(f"POV profile applied: {', '.join(changed)}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if not os.path.exists(RUNNER):
        sys.exit(f"shared runner missing at {RUNNER}")
    cmd = sys.argv[1]
    # image/animate/finish take a job.json — stamp POV defaults on it first.
    # Skip when the arg is a flag (--help) or the file does not exist yet;
    # let the shared runner produce the real error message.
    if (cmd in ("image", "animate", "finish") and len(sys.argv) > 2
            and not sys.argv[2].startswith("-")
            and os.path.isfile(sys.argv[2])):
        apply_pov_defaults(sys.argv[2])
    sys.exit(subprocess.run([sys.executable, RUNNER] + sys.argv[1:]).returncode)


if __name__ == "__main__":
    main()
