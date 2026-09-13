#!/usr/bin/env python3
"""Assemble VEL-COLETTE-UGC-REVIEW-03.

A1 and A3 are the shipped Seedance segments, reused byte-for-byte (native audio).
The middle is rebuilt: new eleven_v3 Creative VO + a 5-clip b-roll bed cut to the
VO's real word timestamps, with the "Loro Piana" beat now a full-bag pan and the
three separate packing cuts collapsed into one continuous packing shot.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(HERE, "build")
os.makedirs(BUILD, exist_ok=True)

MID_MP3 = os.path.join(HERE, "vo/cand-A-mid.mp3")
WORDS = json.load(open(os.path.join(HERE, "vo/cand-A-mid-words.json")))
TAIL = 0.28  # matches slice_mid.PAD_TAIL


def at(word, which="s", nth=0):
    hits = [w for w in WORDS if w["w"] == word]
    return hits[nth][which]


# (source clip, in-point in source, out-time in the mid timeline)
def beats():
    end_pan = at("it's", "s", 0)          # lowercase "it's" -> "it's that soft belted shape"
    end_gusset = at("that", "s", 1)       # "that stands up on its own"
    end_setdown = at("Brushed", "s")
    end_felt = at("twenty", "s")
    end_pack = WORDS[-1]["e"] + TAIL
    return [
        ("b01", os.path.join(HERE, "clips/COL-091-pan-full-bag.mp4"), 0.60, end_pan),
        ("b02", os.path.join(ROOT, "broll/VEL-COL-085-macro-side-gusset.mp4"), 0.50, end_gusset),
        ("b03", os.path.join(ROOT, "broll/VEL-COL-088-setdown-park-bench.mp4"), 0.40, end_setdown),
        # the 1.4s KB-075 in broll/ was pre-trimmed for the v2 cut; this beat needs 2.07s
        ("b04", os.path.join(ROOT, "broll/KB-075-felt-fibre-4s.mp4"), 0.30, end_felt),
        ("b05", os.path.join(HERE, "clips/COL-092b-pack-continuous-three-kv1.mp4"), 0.00, end_pack),
    ]


def sh(*a):
    subprocess.run(a, check=True)


def main():
    bs = beats()
    prev = 0.0
    listing = []
    for name, src, ss, out_t in bs:
        dur = round(out_t - prev, 3)
        prev = out_t
        dst = os.path.join(BUILD, f"{name}.mp4")
        sh("ffmpeg", "-y", "-v", "error", "-ss", f"{ss:.3f}", "-i", src, "-t", f"{dur:.3f}",
           "-an", "-vf", "scale=720:1280:force_original_aspect_ratio=increase,"
                          "crop=720:1280,fps=24,setsar=1",
           "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", dst)
        listing.append(f"file '{name}.mp4'")
        print(f"{name}  {os.path.basename(src)[:38]:38s} {dur:5.2f}s -> {out_t:5.2f}")

    total = prev
    open(os.path.join(BUILD, "broll.txt"), "w").write("\n".join(listing) + "\n")
    sh("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
       "-i", os.path.join(BUILD, "broll.txt"), "-c", "copy", os.path.join(BUILD, "midvid.mp4"))

    # room tone bed lifted from A1's pre-speech head, looped under the VO at -30dB
    tone = os.path.join(BUILD, "tone.wav")
    sh("ffmpeg", "-y", "-v", "error", "-i", os.path.join(ROOT, "segments/A1v2-take2.mp4"),
       "-vn", "-ss", "0.00", "-t", "0.50", "-ac", "2", "-ar", "44100", tone)
    bed = os.path.join(BUILD, "tonebed.wav")
    sh("ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", tone, "-t", f"{total:.3f}",
       "-af", "volume=-24dB", "-ac", "2", "-ar", "44100", bed)
    # ElevenLabs returns a dry close-mic take; A1/A3 carry the Seedance room. Without a matching
    # early-reflection tail the splice is audible as an acoustic change, not a voice change.
    midaudio = os.path.join(BUILD, "midaudio.wav")
    sh("ffmpeg", "-y", "-v", "error", "-i", MID_MP3, "-i", bed,
       "-filter_complex", "[0:a]aformat=sample_rates=44100:channel_layouts=stereo,"
                          "aecho=0.9:0.75:14|27|41:0.10|0.06|0.035[v];"
                          "[v][1:a]amix=inputs=2:duration=first:dropout_transition=0,"
                          "dynaudnorm=f=200:g=5[a]",
       "-map", "[a]", "-ac", "2", "-ar", "44100", midaudio)

    # frame quantisation leaves the concat a few frames shy of the VO; hold the last frame and
    # let -shortest land the segment exactly on the audio rather than truncating the VO
    mid = os.path.join(BUILD, "02-mid.mp4")
    sh("ffmpeg", "-y", "-v", "error", "-i", os.path.join(BUILD, "midvid.mp4"), "-i", midaudio,
       "-vf", "tpad=stop_mode=clone:stop_duration=1", "-map", "0:v", "-map", "1:a",
       "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-shortest", mid)
    vd = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                               "-show_entries", "stream=duration", "-of", "csv=p=0", mid],
                              capture_output=True, text=True).stdout.strip())
    assert abs(vd - total) < 0.15, f"mid video {vd:.3f}s vs VO {total:.3f}s"

    # A1 / A3 normalised to the same container spec, audio untouched
    for name, src, ss, dur in [
        ("01-a1", os.path.join(ROOT, "segments/A1v2-take2.mp4"), 0.0, 7.667),
        ("03-a3", os.path.join(ROOT, "segments/A3v2-take2.mp4"), 0.0, 5.958),
    ]:
        sh("ffmpeg", "-y", "-v", "error", "-ss", f"{ss}", "-i", src, "-t", f"{dur}",
           "-vf", "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps=24,setsar=1",
           "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
           os.path.join(BUILD, f"{name}.mp4"))

    open(os.path.join(BUILD, "final.txt"), "w").write(
        "file '01-a1.mp4'\nfile '02-mid.mp4'\nfile '03-a3.mp4'\n")
    raw = os.path.join(BUILD, "raw.mp4")
    sh("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
       "-i", os.path.join(BUILD, "final.txt"), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", raw)

    out = os.path.join(ROOT, "VEL-COLETTE-UGC-REVIEW-03.mp4")
    # loudnorm resamples internally and will otherwise leave the deliverable at 96kHz
    sh("ffmpeg", "-y", "-v", "error", "-i", raw,
       "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000", "-c:v", "copy",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out)
    print("\nDELIVERED", out)
    subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                    "format=duration:stream=codec_name,width,height,r_frame_rate",
                    "-of", "default=nw=1", out])


if __name__ == "__main__":
    main()
