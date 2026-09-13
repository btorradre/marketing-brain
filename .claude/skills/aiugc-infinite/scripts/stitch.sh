#!/usr/bin/env bash
# Stitch Cut 1 + Cut 2 with a hard cut.
# Cut 1 has native VO from Marketing Studio. Cut 2 from Seedance ships silent —
# we synthesize a silent stereo audio track for Cut 2 so concat doesn't desync.
# Usage: stitch.sh <cut1.mp4> <cut2.mp4> <final.mp4>
set -euo pipefail

C1="${1:?cut1.mp4}"
C2="${2:?cut2.mp4}"
OUT="${3:?final.mp4}"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# Detect whether Cut 2 has audio. If not, mux a silent track at 48k stereo so
# concat with Cut 1 (which has audio) doesn't drop sync.
HAS_AUDIO_C2="$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_type \
  -of csv=p=0 "$C2" 2>/dev/null || true)"

C2_PREP="$C2"
if [ -z "$HAS_AUDIO_C2" ]; then
  C2_PREP="$WORK/cut2_silent.mp4"
  ffmpeg -y -hide_banner -loglevel error \
    -i "$C2" \
    -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
    -c:v copy -c:a aac -shortest \
    "$C2_PREP"
fi

# Normalize both to the same codec/params, then concat. Re-encode is cheap and avoids
# any container-level mismatch surprises.
ffmpeg -y -hide_banner -loglevel error \
  -i "$C1" -i "$C2_PREP" \
  -filter_complex "[0:v:0]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v0]; \
                   [1:v:0]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v1]; \
                   [0:a:0]aresample=48000,aformat=channel_layouts=stereo[a0]; \
                   [1:a:0]aresample=48000,aformat=channel_layouts=stereo[a1]; \
                   [v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  "$OUT"

echo "[stitch] Wrote $OUT" >&2
