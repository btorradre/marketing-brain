#!/usr/bin/env bash
# Train 5 reusable Soul Characters from Pinterest reference images.
#
# Per character:
#   1. Take the original Pinterest JPG as training image #1
#   2. Generate 4 Nano Banana 2 i2i variations (different angles/expressions, same outfit/setting/identity)
#   3. Upload all 5 images to Higgsfield
#   4. Train a Soul 2.0 reference via `higgsfield soul-id create --soul-2 --image id1 ... --image id5`
#   5. Wait for training, save the soul_id to ../souls.json registry
#
# Cost (Nano Banana 2 i2i ~2 cr × 4 vars × 5 chars = 40, plus Soul training ~30 cr × 5 = 150) ≈ 190 credits.
#
# Usage:
#   train_souls.sh             # train all 5
#   train_souls.sh char_3      # train one character by id
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SOULS_JSON="$SKILL_DIR/souls.json"
SOULS_DIR="$SKILL_DIR/avatars/souls"
PINS_DIR="$SKILL_DIR/avatars/pinterest_refs"

mkdir -p "$SOULS_DIR"

# Initialize souls.json if missing
[ -f "$SOULS_JSON" ] || cat > "$SOULS_JSON" <<'EOF'
{
  "_comment": "Trained Soul 2.0 character IDs for use as identity anchors in aiugc-longform / aiugc-infinite. Generated via train_souls.sh from Pinterest references.",
  "characters": {}
}
EOF

# Character definitions — keys must match Pinterest filenames (ref1..ref5)
declare -a CHARS=(
  "ref1|Linda|Pink Coat in Car|mid-50s woman with strawberry-blonde wavy bob, sunglasses pushed up on her head, soft pink fleece coat over black top, sitting in the driver seat of a parked modern car, daylight through windshield, neutral expression with faint smile, seatbelt visible across chest, candid iPhone selfie, no makeup polish, realistic skin texture, warm tones"
  "ref2|Susan|Orange Sweater Big Smile in Car|mid-50s woman with shoulder-length dirty-blonde wavy hair, burnt-orange knit sweater, big warm genuine smile with light pink lipstick, cream leather seat behind her, sitting in a parked car driver seat, soft daylight through sunroof and windshield, candid iPhone selfie, realistic skin pores"
  "ref3|Karen|Brown Bob Black Sweater in Car|late-30s/40s woman with dark brown straight shoulder-length bob with subtle highlights, charcoal/black ribbed knit sweater, slight closed-mouth smile, direct camera gaze, light tan car interior, suburban houses visible out the right window, parked car driver seat, daylight, candid iPhone selfie"
  "ref4|Rachel|Mint Green Sunny Smile in Car|late-30s/40s woman with long honey-blonde wavy hair, mint-green sweatshirt with pale graphic, big genuine open-mouth smile, harsh sunny daylight, cream/tan car seats, sitting in parked car driver seat, golden-hour-style backlight, candid iPhone selfie, realistic skin"
  "ref5|Margaret|Beige Sweater Hotel Room|early-60s woman with shoulder-length blonde-grey wavy hair with highlights, oatmeal beige sweater, big warm smile with blue eyes, beige hotel-style room background with framed beach print on wall and TV in left corner, soft indoor warm light, candid iPhone selfie, realistic skin texture and laugh lines"
)

ONLY=""
[ $# -gt 0 ] && ONLY="$1"

for line in "${CHARS[@]}"; do
  IFS='|' read -r SLUG NAME BLURB DESC <<<"$line"

  if [ -n "$ONLY" ] && [ "$ONLY" != "$SLUG" ]; then continue; fi

  CHAR_DIR="$SOULS_DIR/$SLUG"
  mkdir -p "$CHAR_DIR"

  PIN_PATH="$PINS_DIR/${SLUG}.jpg"
  [ -f "$PIN_PATH" ] || { echo "[souls] ERROR: missing $PIN_PATH" >&2; exit 2; }

  echo
  echo "==============================================="
  echo " Training Soul: $SLUG ($NAME — $BLURB)"
  echo "==============================================="

  # Skip if already trained
  EXISTING="$(jq -r ".characters.\"$SLUG\".soul_id // empty" "$SOULS_JSON")"
  if [ -n "$EXISTING" ]; then
    echo "[souls] $SLUG already trained: $EXISTING — skipping. Delete the entry to retrain."
    continue
  fi

  # 1. Upload the original Pinterest image as training image #1
  echo "[souls] Uploading Pinterest reference..."
  ORIG_UID="$(higgsfield upload create "$PIN_PATH" --json | jq -r '.id // .[0].id')"
  [ -n "$ORIG_UID" ] || { echo "[souls] upload of $PIN_PATH failed" >&2; exit 3; }
  echo "  upload_id: $ORIG_UID"
  echo "$ORIG_UID" > "$CHAR_DIR/upload_orig.txt"

  # 2. Generate 4 Nano Banana 2 i2i variations (different angles, expressions, same outfit & setting)
  declare -a VARIATION_PROMPTS=(
    "Same exact woman: ${DESC}. NEW VARIATION: three-quarter angle from camera-left, slightly looking off to her right, mouth slightly open mid-word as if mid-sentence. Maintain identical face, hair, clothing, setting, lighting. Candid iPhone selfie continuation, realistic skin pores, no AI sheen, no styling change, 9:16 vertical."
    "Same exact woman: ${DESC}. NEW VARIATION: looking down at her steering wheel or hands briefly, eyes lowered, slight smile. Maintain identical face, hair, clothing, setting, lighting. Candid iPhone selfie continuation, realistic skin pores, no AI sheen, 9:16 vertical."
    "Same exact woman: ${DESC}. NEW VARIATION: head tilted ten degrees to her left, eyes back at camera, raised eyebrow, slight smirk. Maintain identical face, hair, clothing, setting, lighting. Candid iPhone selfie continuation, realistic skin pores, no AI sheen, 9:16 vertical."
    "Same exact woman: ${DESC}. NEW VARIATION: tighter close-up framing, eyes wide and direct at camera, neutral mouth. Maintain identical face, hair, clothing, setting, lighting. Candid iPhone selfie continuation, realistic skin pores, no AI sheen, 9:16 vertical."
  )

  declare -a UPLOAD_IDS
  UPLOAD_IDS=("$ORIG_UID")

  for i in "${!VARIATION_PROMPTS[@]}"; do
    VAR_NUM=$((i + 1))
    VAR_PROMPT="${VARIATION_PROMPTS[$i]}"
    VAR_OUT="$CHAR_DIR/variation_${VAR_NUM}.png"
    VAR_JOB="$CHAR_DIR/variation_${VAR_NUM}_job.json"

    echo "[souls] Variation $VAR_NUM/4 (Nano Banana 2 i2i)..."
    higgsfield generate create nano_banana_2 \
      --prompt "$VAR_PROMPT" \
      --image "$ORIG_UID" \
      --aspect_ratio 9:16 \
      --resolution 2k \
      --wait --wait-timeout 10m \
      --json > "$VAR_JOB"

    URL="$(jq -r 'if type=="array" then (.[0].result_url // .[0].results[0].result_url) else (.result_url // .results[0].result_url) end // empty' "$VAR_JOB")"
    if [ -z "$URL" ]; then
      echo "[souls] variation $VAR_NUM FAILED (no result_url)" >&2
      cat "$VAR_JOB" >&2
      exit 4
    fi
    curl -sSL --fail -o "$VAR_OUT" "$URL"

    # Upload variation
    VAR_UID="$(higgsfield upload create "$VAR_OUT" --json | jq -r '.id // .[0].id')"
    [ -n "$VAR_UID" ] || { echo "[souls] variation $VAR_NUM upload failed" >&2; exit 5; }
    UPLOAD_IDS+=("$VAR_UID")
    echo "  variation_${VAR_NUM} → $VAR_OUT (upload_id $VAR_UID)"
  done

  # 3. Train Soul 2.0
  echo "[souls] Creating Soul 2.0 reference '$NAME' from ${#UPLOAD_IDS[@]} images..."
  IMG_FLAGS=()
  for uid in "${UPLOAD_IDS[@]}"; do IMG_FLAGS+=(--image "$uid"); done

  CREATE_JOB="$CHAR_DIR/soul_create.json"
  higgsfield soul-id create \
    --name "${NAME} (${SLUG})" \
    --soul-2 \
    "${IMG_FLAGS[@]}" \
    --json > "$CREATE_JOB"

  SOUL_ID="$(jq -r '.id // .reference_id // .[0].id // empty' "$CREATE_JOB")"
  [ -n "$SOUL_ID" ] || { echo "[souls] soul-id create returned no id" >&2; cat "$CREATE_JOB" >&2; exit 6; }
  echo "  soul_id (training): $SOUL_ID"

  # 4. Wait for training
  echo "[souls] Waiting for training..."
  higgsfield soul-id wait "$SOUL_ID" --json > "$CHAR_DIR/soul_wait.json" || true

  STATUS="$(jq -r '.status // empty' "$CHAR_DIR/soul_wait.json")"
  echo "  training status: ${STATUS:-unknown}"

  # 5. Save to souls.json
  TMP="$(mktemp)"
  jq --arg slug "$SLUG" --arg name "$NAME" --arg blurb "$BLURB" \
     --arg soul "$SOUL_ID" --arg orig "$PIN_PATH" \
     --arg dir "$CHAR_DIR" --arg desc "$DESC" \
     '.characters[$slug] = {name:$name, blurb:$blurb, description:$desc, pinterest_ref:$orig, training_dir:$dir, soul_id:$soul, created_at:(now | todate)}' \
     "$SOULS_JSON" > "$TMP" && mv "$TMP" "$SOULS_JSON"

  echo "[souls] $SLUG trained → soul_id=$SOUL_ID (saved to souls.json)"
done

echo
echo "==============================================="
echo " All requested Souls processed."
echo " Registry: $SOULS_JSON"
echo "==============================================="
jq '.characters | to_entries | map({slug:.key, name:.value.name, soul_id:.value.soul_id})' "$SOULS_JSON"
