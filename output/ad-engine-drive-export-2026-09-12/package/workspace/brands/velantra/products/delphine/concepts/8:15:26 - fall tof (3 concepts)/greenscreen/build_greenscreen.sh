#!/bin/bash
# Delphine fall TOF — green screen UGC composite, v2 (Brooks 8/15).
#
# FORMAT: classic TikTok-greenscreen. The keyed creator is SMALL, pinned BOTTOM-LEFT for the
# ENTIRE runtime. The B-roll plays full-frame behind her the whole way. No full-frame creator
# windows.
#
# BED: product-relevant shots only. B14 (black tote + tiny beige bag) is RETIRED — Brooks:
# not relevant to the concept. B03 is the REGENERATED open-state load-in.
#
# CHROMAKEY: colorkey 0x358D5B @ 0.12/0.02 (measured plate green; RGB filter, not YUV).
# NO despill — measured: every despill mix pulls the cream canvas's G channel down (pinking).
# Audio: her native Seedance track, untouched, never time-stretched.

set -e
cd "$(dirname "$0")"
BROLL=../broll/clips
PLATE=creator-plate.mp4
OUT=DEL-FALL-GREENSCREEN-01.mp4

# 1. Full-frame background bed, 30s, six product shots.
ffmpeg -v error -y \
  -i "$BROLL/LC-B01-closet.mp4" -i "$BROLL/LC-B10-wall.mp4" \
  -i "$BROLL/LC-B04-standsquare.mp4" -i "$BROLL/LC-B03-loadin.mp4" \
  -i "$BROLL/LC-B05-walking.mp4" -i "$BROLL/LC-B09-bench.mp4" \
  -filter_complex "\
    [0:v]trim=0:4,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v0]; \
    [1:v]trim=0:5,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v1]; \
    [2:v]trim=0:6,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v2]; \
    [3:v]trim=0:6,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v3]; \
    [4:v]trim=0:5,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v4]; \
    [5:v]trim=0:4,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v5]; \
    [v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0[bg]" \
  -map "[bg]" -an -c:v libx264 -pix_fmt yuv420p -r 30 bg.mp4

# 2. Key the creator, shrink her to a bottom-left PIP, overlay for the FULL duration.
#    Plate is mid-thigh-up; crop to her upper 72% so the PIP is head-and-torso, then scale.
ffmpeg -v error -y -i bg.mp4 -i "$PLATE" \
  -filter_complex "\
    [1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920, \
         colorkey=0x358D5B:0.12:0.02,crop=1080:1382:0:0,scale=520:665[pip]; \
    [0:v][pip]overlay=8:1920-665-16:format=auto[outv]" \
  -map "[outv]" -map 1:a -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest "$OUT"

rm -f bg.mp4
echo "built $OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
