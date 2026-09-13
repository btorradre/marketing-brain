#!/bin/zsh
set -a; source "/Users/brooksorradre2/Documents/marketing brain/.env"; set +a
export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
RUN="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/videos/boatkin-vo-7-21-26"
cd "$RUN"
for round in 1 2 3 4 5 6 7 8; do
  missing=$(python3 - <<'PY'
import json, os
m = json.load(open("veo_manifest.json"))
scenes = [s for s in m["scenes"] if not os.path.exists(s["output"])]
if scenes:
    json.dump({"defaults": m["defaults"], "scenes": scenes}, open("veo_manifest_retry.json", "w"))
print(len(scenes))
PY
)
  if [ "$missing" = "0" ]; then echo "ALL CLIPS PRESENT"; break; fi
  echo "round $round: $missing missing, retrying..."
  python3 ~/.claude/skills/video-gen/scripts/generate_video.py --manifest veo_manifest_retry.json 2>&1 | grep -E "Saved|ERROR|saved|->" | tail -20
  [ "$round" != "8" ] && sleep 90
done
echo "final count: $(ls clips | grep -c mp4)/13"
