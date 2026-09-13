#!/usr/bin/env python3
"""Animate GAP-01 (base + brass feet macro) via Google Omni, reusing the b-roll runner."""
import sys, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNNER = Path("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/vivienne/broll/animate_omni.py")
spec = importlib.util.spec_from_file_location("omni", RUNNER)
omni = importlib.util.module_from_spec(spec)
sys.modules["omni"] = omni
spec.loader.exec_module.__self__ if False else None
# exec the module body without running main()
src = RUNNER.read_text().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(src, str(RUNNER), "exec"), omni.__dict__)

MOTION = ("THE CAMERA DOES NOT MOVE AT ALL. It is locked off at table level at exactly the framing "
 "of the still and never pushes in, pulls back, tilts or reframes. NOTHING in the frame moves "
 "except an almost imperceptible handheld breathing of one or two pixels and a very faint shift "
 "of the highlight on the brass feet, as if someone leaned slightly and the room light moved. The "
 "bag does not settle, shift, rock or slide. The two round brass feet stay exactly where they are, "
 "keep exactly the same size, shape and spacing, and never multiply, disappear, sink into the "
 "table or turn into studs, rivets or wheels. The stitched cognac corner cap stays flat against "
 "the leather and never lifts, peels or becomes a separate flap. ")

if __name__ == "__main__":
    out = HERE / "GAP-01.mp4"
    img = HERE.parent / "board-frames" / "GAP-01-brass-feet.png"
    print("submitting GAP-01...", flush=True)
    iid = omni.submit(img, MOTION + omni.LOCK + omni.REAL)
    data = omni.poll(iid)
    out.write_bytes(data)
    print("OK", out, round(len(data)/1e6, 1), "MB")
