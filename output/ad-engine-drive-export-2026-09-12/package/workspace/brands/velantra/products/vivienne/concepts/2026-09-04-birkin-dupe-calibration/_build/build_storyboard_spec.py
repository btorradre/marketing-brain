#!/usr/bin/env python3
"""Write the current Vivienne app storyboard and review packet."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_FRAMES = Path(
    "/Users/brooksorradre2/Documents/marketing brain/_engine/mcp/ad-engine/data/watch/"
    "job_cc6efc9d4bef/frames"
)


def frame(name: str) -> str:
    return str(ROOT / "visuals" / "storyboard" / name)


reference = [
    {
        "t": "0:00–0:05",
        "script": "[Analysis] Luxury-style recognition creates the first-stop hook.",
        "frame": str(REFERENCE_FRAMES / "beat_001.jpg"),
        "visual": "A stable product collage fills the vertical canvas; the creator remains visible at lower right under a bold top headline.",
        "emotion": "Recognition → curiosity.",
    },
    {
        "t": "0:05–0:10",
        "script": "[Analysis] Personal desire pivots into the alternative reveal.",
        "frame": str(REFERENCE_FRAMES / "beat_003.jpg"),
        "visual": "The same composition holds while gestures, headline words and captions advance the argument.",
        "emotion": "Desire → anticipation.",
    },
    {
        "t": "0:10–0:17.5",
        "script": "[Analysis] Concrete product information supports the value judgment, followed by personal endorsement.",
        "frame": str(REFERENCE_FRAMES / "beat_006.jpg"),
        "visual": "Creator-led delivery remains primary; the product collage stays legible behind her.",
        "emotion": "Specificity → confidence.",
    },
    {
        "t": "0:17.5–0:19.3",
        "script": "[Analysis] A direct response instruction closes the ad.",
        "frame": str(REFERENCE_FRAMES / "beat_008.jpg"),
        "visual": "Same stable composition with a final CTA text change.",
        "emotion": "Confidence → action.",
    },
]

ours = [
    {
        "id": "V01",
        "t": "0:00–0:01.5",
        "start_s": 0.0,
        "end_s": 1.5,
        "script": "Love that Birkin-inspired shape?",
        "frame": frame("01-hook.jpg"),
        "visual": "Persistent collage: generated home-interior Vivienne hero, an exact crop of the approved master at lower left, and Anna keyed against the lower-right frame edge. Top headline BIRKIN-INSPIRED. Start captions immediately on the first spoken word.",
        "emotion": "Recognition and an inviting shared taste cue.",
        "note": "Hard open. No intro sting, price, sale badge or competitor product image.",
    },
    {
        "id": "V02",
        "t": "0:01.5–0:05.25",
        "start_s": 1.5,
        "end_s": 5.25,
        "script": "I've wanted a bag like this for the longest time,",
        "frame": frame("02-desire.jpg"),
        "visual": "Hold the same plate and Anna placement. Change only the top headline to WANTED THIS SHAPE; use word-synced speech captions in short groups.",
        "emotion": "Personal longing and familiarity.",
        "note": "The stillness mirrors the reference; Anna's face and gestures provide motion.",
    },
    {
        "id": "V03",
        "t": "0:05.25–0:11.62",
        "start_s": 5.25,
        "end_s": 11.62,
        "script": "but I got tired of the long waitlist and paying designer prices for quality that didn't match.",
        "frame": frame("03-frustration.jpg"),
        "visual": "Keep the same collage. Top headline becomes TIRED OF THE WAITLIST. Let Anna deliver the frustration directly; captions use exact spoken phrases including QUALITY THAT DIDN'T MATCH without showing an amount.",
        "emotion": "Earned frustration; skeptical, not angry.",
        "note": "No current offer amount. “Designer prices” is spoken qualitative language, not an on-screen price comparison.",
    },
    {
        "id": "V04",
        "t": "0:11.62–0:15.00",
        "start_s": 11.62,
        "end_s": 15.0,
        "script": "Then Velantra gave me early access to the Vivienne.",
        "frame": frame("04-reveal.jpg"),
        "visual": "Same collage and presenter position. Change the headline to THE VIVIENNE; add a smaller VELANTRA identifier in the live edit.",
        "emotion": "Relief and discovery.",
        "note": "The product is named once and clearly. Early access is an authenticated creator experience.",
    },
    {
        "id": "V05",
        "t": "0:15.00–0:21.75",
        "start_s": 15.0,
        "end_s": 21.75,
        "script": "It's got braided trim, a gold-tone closure, and that relaxed, slouchy shape, with no logo across the front.",
        "frame": frame("05-details.jpg"),
        "visual": "Hold the persistent collage and use its source-locked lower-left master crop to show the braided edge, oval center fitting, side bars and inward-falling belt tails. Anna stays at the lower-right edge, clear of every fitting. Headline: BRAIDED TRIM · GOLD-TONE CLOSURE; exact speech captions include no logo across the front.",
        "emotion": "Specific visual proof and quiet-luxury satisfaction.",
        "note": "Do not animate the closure, invent hidden construction, or cover the hardware with Anna or captions.",
    },
    {
        "id": "V06",
        "t": "0:21.75–0:28.12",
        "start_s": 21.75,
        "end_s": 28.12,
        "script": "I've been using it as my daily driver for the past few weeks, and I'm absolutely obsessed.",
        "frame": frame("06-proof.jpg"),
        "visual": "Swap only the lower-left proof tile to the generated café-chair daily-use plate; keep the hero and Anna fixed. The full hero Vivienne remains unobstructed above. Headline: MY DAILY DRIVER. Let the natural vocal emphasis land on absolutely obsessed.",
        "emotion": "Trust, warmth and current enthusiasm.",
        "note": "The usage statement is authenticated. The visual implies normal everyday context without a capacity, material, or durability claim.",
    },
    {
        "id": "V07",
        "t": "0:28.12–0:31.88",
        "start_s": 28.12,
        "end_s": 31.88,
        "script": "It's available for pre-order and expected to ship in October.",
        "frame": frame("07-preorder.jpg"),
        "visual": "Return the lower-left tile to the detail plate while the hero and Anna remain fixed. Top headline PRE-ORDER; disclosure SHIPPING EXPECTED OCTOBER. Anna remains unobstructed.",
        "emotion": "Clear expectations and practical confidence.",
        "note": "Recheck fulfillment immediately before publication. No price or urgency claim.",
    },
    {
        "id": "V08",
        "t": "0:31.88–0:33.75",
        "start_s": 31.88,
        "end_s": 33.75,
        "script": "I've left the link below.",
        "frame": frame("08-cta.jpg"),
        "visual": "Hold the full collage and Anna. Change the top headline to LINK BELOW while PRE-ORDER · SHIPPING EXPECTED OCTOBER remains visible. Use the exact speech caption I've left the link below. End on the product for at least six frames after the final word if the natural read leaves room.",
        "emotion": "Low-pressure, direct action.",
        "note": "Use the platform link CTA. Do not add comment automation, discount, countdown, or price.",
    },
]

storyboard = {
    "schema_version": "1.0",
    "title": "Vivienne — Birkin-inspired personal find — AI UGC greenscreen",
    "summary": (
        "A 33.75-second provisional adaptation of Instagram DckbXyGt785. Mirror the reference's stable vertical "
        "product background, bottom-right presenter, bold headline and rapid speech captions. Anna is the requested "
        "HeyGen presenter; Woman Over 40 is the Eleven v3 Creative voice. The story moves from recognizable shape "
        "to personal frustration, reveal, visible design proof, authenticated daily use, fulfillment and link CTA."
    ),
    "project": "VEL-VIV-BIRKINDUPE-QC-01",
    "timelines": [
        {
            "label": "REFERENCE STRUCTURE — PRIVATE ANALYSIS",
            "source": "Instagram DckbXyGt785 · 19.3s · watched job_cc6efc9d4bef",
            "role": "reference",
            "beats": reference,
        },
        {
            "label": "OUR VERSION — AI UGC GREENSCREEN",
            "source": "Vivienne · Anna · Woman Over 40 VO · 33.75s provisional",
            "role": "ours",
            "beats": ours,
        },
    ],
    "notes": [
        {
            "title": "PRESENTER + VO",
            "text": (
                "HeyGen account avatar Anna: group 71d05871ff2e4f17ac63d43dfefa0ec7; selected existing look "
                "abb163c6fe0d4880863c30a2323394ca. ElevenLabs Woman Over 40: NBIPq5xdnIg9kaBH5Ape; "
                "eleven_v3 Creative, stability 0.0, similarity 0.85, speaker boost on. One continuous natural take; "
                "no atempo or artificial speed change. Confirm Avatar V eligibility before rendering."
            ),
        },
        {
            "title": "EDITING CONTRACT",
            "text": (
                "1080×1920, 30fps. Use the internal video editor after approval. Keep Anna cut by the lower-right frame "
                "edge, sized on her head, without covering product hardware or captions. The hero, detail tile and Anna "
                "form one persistent reference-matched collage; swap only the lower-left tile at V06 and V07. All other "
                "progression comes from text and Anna's performance. Captions use actual aligned words, "
                "2–5 words per cue, one or two lines, high contrast, inside platform safe zones."
            ),
        },
        {
            "title": "PRODUCT FIDELITY",
            "text": (
                "Chocolate Vivienne master selected 2026-09-03 is the identity source. Preserve wide soft slouch, "
                "braided edge, two upright handles, left key bell, cognac trim, oval center fitting, two side bars, "
                "inward-falling slotted belt ends, corner caps and no logo. The master is an owner-selected generated "
                "design target, not a physically measured sample."
            ),
        },
        {
            "title": "FULFILLMENT + CLAIMS",
            "text": (
                "No current offer amount or price badge. The creator's waitlist frustration, price/quality comparison, "
                "early access, several weeks of daily use and enthusiasm were confirmed as authentic. Recheck pre-order "
                "and expected October shipping immediately before publication."
            ),
        },
        {
            "title": "APPROVAL GATE",
            "text": (
                "These are review keyframes. Do not generate the ElevenLabs take, HeyGen animation, Google Omni motion "
                "or final edit until a human approves every OUR VERSION image card in the ad-engine board. Final editing "
                "QC requires the exported video and cannot pass from storyboard evidence."
            ),
        },
    ],
    "moodboard": [
        {"image": str(ROOT / "visuals" / "presenter" / "anna-keyed.png"), "caption": "Requested HeyGen presenter: Anna."},
        {"image": str(ROOT / "visuals" / "generated" / "vivienne-home-hero.png"), "caption": "Generated hero plate: warm creator-home setting."},
        {"image": str(ROOT / "visuals" / "generated" / "vivienne-detail.png"), "caption": "Generated detail plate: braided trim and gold-tone hardware."},
        {"image": str(ROOT / "visuals" / "generated" / "vivienne-daily-driver.png"), "caption": "Generated everyday-use plate."},
    ],
    "production": {
        "status": "storyboard_keyframes_ready_for_human_approval",
        "destination": "adengine-app",
        "width": 1080,
        "height": 1920,
        "fps": 30,
        "target_duration_s": 33.75,
        "timing_basis": "90 words at 160 wpm; replace with ElevenLabs alignment after approval",
        "presenter": {
            "provider": "heygen",
            "name": "Anna",
            "group_id": "71d05871ff2e4f17ac63d43dfefa0ec7",
            "look_id": "abb163c6fe0d4880863c30a2323394ca",
            "composition": "bottom-right keyed talking head",
        },
        "voice": {
            "provider": "elevenlabs",
            "name": "Woman Over 40",
            "voice_id": "NBIPq5xdnIg9kaBH5Ape",
            "model": "eleven_v3",
            "preset": "Creative",
            "stability": 0.0,
            "similarity": 0.85,
            "speaker_boost": True,
            "one_continuous_take": True,
            "speed_change_allowed": False,
        },
        "image_generation": {
            "provider_workflow": "GPT Image 2 for hero and daily-driver plates; direct approved-master crop for detail",
            "aspect_ratio": "9:16",
            "source_master": (
                "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/vivienne/"
                "product-images/master/VIVIENNE-MASTER-chocolate-front.png"
            ),
            "plates": [
                "visuals/generated/vivienne-home-hero.png",
                "visuals/generated/vivienne-detail.png",
                "visuals/generated/vivienne-daily-driver.png",
            ],
        },
        "video_generation_after_approval": "Google Omni only when a beat needs generated motion; stable plates do not require generated video.",
        "editor_after_approval": "internal video editor current documented entry point; no Cutroom, ChatCut, HyperFrames or Remotion",
        "final_qc": (
            "Inspect the full export with audio, exact cut boundaries, caption sync, first/last frames, Anna's key around "
            "hair and hands, product identity, disclosure readability, and unintended price or logo appearances."
        ),
    },
}

packet = {
    "creator_id": "root-creative-author",
    "stage": "storyboard",
    "artifacts": {"script": "script-v4.md", "storyboard": "storyboard-v5.json"},
    "context": {
        "product_truth": "evidence/product-truth-evidence.json",
        "customer_voice": "evidence/customer-voice-evidence.json",
        "avatar_brief": "avatar-brief.json",
        "reference": "reference-analysis.md",
        "reference_watch": "reference/watch.json",
        "product_master": storyboard["production"]["image_generation"]["source_master"],
        "presenter_reference": "visuals/presenter/anna-keyed.png",
        "generated_hero": storyboard["production"]["image_generation"]["plates"][0],
        "generated_detail": storyboard["production"]["image_generation"]["plates"][1],
        "generated_daily_driver": storyboard["production"]["image_generation"]["plates"][2],
        "storyboard_contact_sheet": "visuals/storyboard/contact-sheet.jpg",
        **{f"storyboard_frame_{i:02d}": f"visuals/storyboard/{name}" for i, name in enumerate([
            "01-hook.jpg", "02-desire.jpg", "03-frustration.jpg", "04-reveal.jpg",
            "05-details.jpg", "06-proof.jpg", "07-preorder.jpg", "08-cta.jpg",
        ], start=1)},
    },
}

(ROOT / "storyboard-v5.json").write_text(json.dumps(storyboard, indent=2) + "\n")
(ROOT / "packet-storyboard-v5.json").write_text(json.dumps(packet, indent=2) + "\n")
