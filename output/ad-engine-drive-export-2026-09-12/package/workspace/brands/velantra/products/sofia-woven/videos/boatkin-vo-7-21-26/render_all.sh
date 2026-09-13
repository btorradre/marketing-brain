#!/bin/zsh
# Render every generated ad project to final/ with canonical DR naming
export npm_config_cache="/private/tmp/claude-503/-Users-brooksorradre2-Documents-marketing-brain/e14fe115-2475-4770-95d9-80ed28f79702/scratchpad/npm-cache"
RUN="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/videos/boatkin-vo-7-21-26"
typeset -A SLUG
SLUG=(S1 foundit S2 ferry S3 disposable S4 stylist S5 fortune)
for d in "$RUN"/hyperframes/ads/S*-v*; do
  ad=$(basename "$d")            # e.g. S1-v30
  s=${ad%%-*}; v=${ad##*-}
  out="$RUN/final/straw-tote-boatkin-${s:l}-${SLUG[$s]}-${v}.mp4"
  if [ -f "$out" ]; then echo "$ad: exists, skip"; continue; fi
  echo "=== rendering $ad -> $(basename $out)"
  (cd "$d" && npx hyperframes render --output "$out" --quality standard 2>&1 | tail -2)
done
echo "RENDER BATCH COMPLETE: $(ls "$RUN/final" | grep -c '\.mp4$')/15"
