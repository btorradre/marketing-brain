#!/bin/zsh
# Extract 0.5s-interval frames from every clip for the mandatory video audit
RUN="/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/videos/boatkin-vo-7-21-26"
for f in "$RUN"/clips/K*.mp4; do
  k=$(basename "$f" .mp4)
  mkdir -p "$RUN/qa/$k"
  ffmpeg -y -v error -i "$f" -vf "fps=2,scale=512:-1" "$RUN/qa/$k/f_%02d.jpg"
  echo "$k: $(ls "$RUN/qa/$k" | wc -l | tr -d ' ') frames"
done
