#!/bin/bash
# Generate one editorial image per article section heading via higgsfield gpt_image_2.
set -u
cd "$(dirname "$0")"
mkdir -p images logs

STYLE="Candid editorial lifestyle photograph, warm natural light, muted cream and sage palette, shallow depth of field, authentic unposed documentary feel. No text, no logos, no medication labels, no readable brand names."

gen() {
  local name="$1"; local prompt="$2"; local log="logs/${name}.log"
  echo "[$(date +%H:%M:%S)] START $name" | tee -a "$log"
  higgsfield generate create gpt_image_2 \
    --prompt "$prompt $STYLE" \
    --aspect_ratio "16:9" --quality high --resolution 2k \
    --wait --wait-timeout 8m > "$log" 2>&1
  local url; url=$(grep -oE 'https?://[^[:space:]]+' "$log" | head -1)
  if [ -z "$url" ]; then echo "[$(date +%H:%M:%S)] FAIL $name (no url)" | tee -a "$log"; return 1; fi
  curl -sSL "$url" -o "images/${name}_raw.png"
  echo "[$(date +%H:%M:%S)] DONE $name $(stat -f%z images/${name}_raw.png) bytes" | tee -a "$log"
}

gen sec_doctor "A warm gastroenterologist in a white coat sitting across a desk from a woman in her early 50s, explaining gently and gesturing toward a simple anatomical model of the human digestive system on the desk, calm modern clinic office." &
gen sec_cabinet "An open home bathroom cabinet crowded with generic plain laxative boxes, fiber tubs and supplement bottles, a woman's hand reaching in, soft morning bathroom light, a sense of clutter and frustration." &
gen sec_ingredients "A clean overhead flat lay on a pale ceramic surface: fresh celery stalks, vivid green leaves, and a small bowl of pale soluble fiber powder, fresh and botanical, bright daylight." &
gen sec_juicing "A messy kitchen counter with a juicer and bunches of celery, green pulp and juice splatter, a tired woman in her early 50s mid clean-up looking weary, bright morning light, a sense of hassle." &
gen sec_relief "A woman in her early 50s looking calm and quietly relieved in a bright kitchen in the morning, holding a glass of water, gentle ease and comfort on her face." &
gen sec_turnaround "A happy relaxed woman in her late 50s laughing genuinely while having coffee with a friend at a sunny cafe table, warm golden hour light, fully at ease." &
gen sec_cost "A kitchen table covered with many plain unlabeled supplement bottles and fiber tubs beside a small stack of pharmacy receipts and a calculator, a woman's hands resting near them, soft light, a sense of wasted money." &
gen sec_choose "A serene confident woman in her 50s standing by a sunlit kitchen window, calm decisive expression, one hand resting comfortably over her stomach, warm reassuring light." &
gen sec_mornings "A peaceful bright morning at home, a content unhurried woman in her 50s enjoying a calm relaxed morning with a cup of coffee in soft sunlight near a window." &

wait
echo "[$(date +%H:%M:%S)] ALL SECTION IMAGES FINISHED"
ls -la images/*_raw.png
