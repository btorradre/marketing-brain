#!/bin/bash
# GPT Image 2 via kie.ai — 6 t2i scenes + 1 i2i product shot for the Carol universal advertorial
set -uo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="/Users/brooksorradre2/Documents/marketing brain/.env"
KEY=$(grep '^KIE_API_KEY=' "$ENV_FILE" | cut -d= -f2- | tr -d '"' | tr -d "'")
JAR="/Users/brooksorradre2/Documents/marketing brain/brands/motilli/product-images/updated/product img 1.webp"
mkdir -p "$DIR/images" "$DIR/gen"

jsonget() { python3 -c "
import json,sys
d=json.load(sys.stdin)
for k in sys.argv[1:]:
    d=d[k] if not k.isdigit() else d[int(k)]
print(d)
" "$@"; }

echo "== upload jar ref =="
UP=$(curl -s -X POST "https://kieai.redpandaai.co/api/file-stream-upload" \
  -H "Authorization: Bearer $KEY" -F "file=@$JAR" -F "uploadPath=images" -F "fileName=motilli-jar.webp")
JAR_URL=$(echo "$UP" | jsonget data downloadUrl)
echo "jar: $JAR_URL"

create() { # $1=model $2=payload-file -> taskId
  curl -s -X POST "https://api.kie.ai/api/v1/jobs/createTask" \
    -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
    -d @"$2" | jsonget data taskId
}

declare -a NAMES TASKS

submit() { # name model prompt [i2i_url]
  local name="$1" model="$2" prompt="$3" ref="${4:-}"
  python3 - "$model" "$prompt" "$ref" > "$DIR/gen/$name.json" <<'PY'
import json,sys
model,prompt,ref=sys.argv[1],sys.argv[2],sys.argv[3]
inp={"prompt":prompt,"aspect_ratio":"3:2","resolution":"2K"}
if ref: inp["input_urls"]=[ref]
print(json.dumps({"model":model,"input":inp}))
PY
  local tid=$(create "$model" "$DIR/gen/$name.json")
  echo "task $name = $tid"
  NAMES+=("$name"); TASKS+=("$tid")
}

T2I="gpt-image-2-text-to-image"
I2I="gpt-image-2-image-to-image"

submit "01_hero" "$T2I" "Editorial magazine photograph, warm documentary realism. A woman in her early 60s with shoulder-length silver-streaked hair sits at a lived-in kitchen table in bright soft morning window light, hands wrapped around a white coffee mug, gentle relaxed smile, looking slightly off-camera, quietly content, like someone whose mornings finally belong to her again. Shallow depth of field, warm natural tones, 50mm lens look. Photorealistic. No text or logos anywhere."

submit "02_party" "$T2I" "Editorial documentary photograph at a family retirement party in a warm living room, evening lamplight. A woman in her early 60s in a loose navy dress stands slightly apart from a small blurred group of chatting guests, holding a glass of sparkling water with both hands, wearing a polite strained smile, one arm crossed over her midsection. Candid, quietly melancholy mood. Photorealistic, natural tones. No text or logos anywhere."

submit "03_drawer" "$T2I" "Overhead editorial photograph of an open bathroom drawer crowded with generic unbranded constipation remedies: a large white powder tub, small orange laxative boxes, a gummy supplement bottle, herbal tea boxes, a magnesium capsule bottle, a prune juice bottle. Worn, half-used packaging, every label plain and completely blank with no readable words. Honest flat daylight, documentary style. Photorealistic. No readable text anywhere."

submit "04_article" "$T2I" "Editorial photograph over the shoulder of a woman in her early 60s sitting at a kitchen table in soft winter morning light, holding a smartphone displaying a long text article with the screen content soft and unreadable, a mug of tea and reading glasses beside her, her free hand paused at her chin in a moment of quiet realization. Photorealistic, shallow depth of field, warm muted tones. No readable text anywhere."

submit "05_product" "$I2I" "Place this exact product jar on a warm wooden kitchen counter next to a white coffee mug and a small white plate holding two dark forest green heart-shaped gummies, soft morning window light from the left, shallow depth of field, clean editorial product photography. Keep the jar shape, white cap, green label design, label text, colors, and proportions exactly as shown in the reference image: a clear square jar with rounded corners, white screw cap, green motilli label. Do not alter the label." "$JAR_URL"

submit "06_porch" "$T2I" "Editorial photograph, joyful candid moment: a woman in her early 60s in a light knit cardigan standing on her sunlit front porch holding a coffee mug, laughing freely with her head tilted slightly back, golden morning light, spring greenery softly blurred behind her. Genuine relief and lightness. Photorealistic, warm tones, 50mm lens look. No text or logos anywhere."

submit "07_doctor" "$T2I" "Editorial photograph inside a bright modern medical exam room: a woman doctor in her 50s wearing a white coat sits on a rolling stool writing a note on a small prescription pad with a pen, looking up with a warm curious expression toward her patient, a woman in her early 60s seen softly from behind at the edge of the frame. Natural window light, photorealistic documentary style. Screen and papers unreadable. No readable text anywhere."

echo "== polling =="
for i in "${!NAMES[@]}"; do
  name="${NAMES[$i]}"; tid="${TASKS[$i]}"
  for attempt in $(seq 1 60); do
    sleep 10
    R=$(curl -s "https://api.kie.ai/api/v1/jobs/recordInfo?taskId=$tid" -H "Authorization: Bearer $KEY")
    STATE=$(echo "$R" | python3 -c "import json,sys; print(json.loads(sys.stdin.read(),strict=False)['data']['state'])" 2>/dev/null || echo parse_err)
    if [ "$STATE" = "success" ]; then
      URL=$(echo "$R" | python3 -c "
import json,sys
d=json.loads(sys.stdin.read(),strict=False)['data']
print(json.loads(d['resultJson'],strict=False)['resultUrls'][0])")
      curl -s -A "Mozilla/5.0" -o "$DIR/gen/$name.png" "$URL"
      sips -s format jpeg -s formatOptions 80 -Z 1600 "$DIR/gen/$name.png" --out "$DIR/images/$name.jpeg" >/dev/null
      echo "DONE $name ($(du -h "$DIR/images/$name.jpeg" | cut -f1))"
      break
    elif [ "$STATE" = "fail" ]; then
      echo "FAIL $name: $R" ; break
    fi
    [ $attempt -eq 60 ] && echo "TIMEOUT $name"
  done
done
echo "== all done =="
ls -la "$DIR/images/"
