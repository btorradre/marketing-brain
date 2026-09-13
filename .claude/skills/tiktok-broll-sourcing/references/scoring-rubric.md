# Visible emotional intensity and rawness

Use this as a repeatable editorial rubric. It is a custom selection standard derived from the user's brief, not a scientifically validated scale or an automatic emotion detector. Rate what can be seen in the particular interval. Do not score claimed pain severity, diagnosis, private feelings or engagement metrics.

## EV intensity: 1–5

| Score | Visible anchor | Selection |
|---|---|---|
| 1 — neutral | Ordinary task or neutral expression; emotion is supplied by copy/audio | Reject |
| 2 — mild | Small frown, casual sigh, resting hand, slight smile | Reject |
| 3 — clear | Obvious grimace, visible frustration or happiness; reaction remains moderate | Reject |
| 4 — strong | Pronounced reaction affects posture or the task, but falls short of an unmistakably extreme moment | Reject; search for a stronger interval or source |
| 5 — extreme | Dominant, unmistakable reaction visibly takes over the person's posture, expression or activity; the stakes read immediately without sound/text | Eligible only if every other gate passes |

For 5/5, cite at least two mutually supporting observable cues: e.g. tightly pinched expression plus abdomen-bracing/folded posture; shaking sobs plus interrupted action; recoil plus face/hand response to an object; a large celebratory reaction plus spontaneous movement toward someone. A face need not be visible if body/action evidence is sufficient. Score consistency of the visible reaction, not loudness, camera shake or how alarming the topic is.

Extreme can be positive or negative. Joy, relief, disgust, shock and frustration can all qualify. Do not force every result into pain or crying. A strongly frozen reaction can be intense even without large movement, but its context and additional visible cues must make the reading defensible.

Record:

- `Entry EV`: score of the chosen starting moment. Selection requires 5.
- `Peak EV`: strongest observed moment, with source timestamp. Selection requires 5.
- `Usable extreme interval`: continuous span where the reaction remains clearly extreme enough to carry the beat, allowing natural motion and brief blinks without averaging away intensity.
- `Evidence`: timestamped description of cues. Never give “5/5” with no observable explanation.
- `Confidence`: high / medium / low, and the ambiguity. Low-confidence or conflicting-cue candidates remain leads, not selected matches.

Use integer anchors. Avoid decimals or a fabricated weighted emotion formula. When choosing between two passing clips, explain the better action readability and concept fit rather than pretending their emotional differences can be measured to a tenth.

## Rawness: 1–5, separate from intensity

| Score | Capture appearance | Selection |
|---|---|---|
| 1 | Clearly cinematic/commercial presentation | Reject |
| 2 | Polished stock/performance, studio staging or conspicuous manufactured imperfection | Reject |
| 3 | Mixed signals; looks partly phone-native but staged/beautified or context unclear | Hold/reject until resolved |
| 4 | Believable ordinary phone footage, practical setting/light, natural gesture and plausible camera position | Eligible |
| 5 | Exceptionally convincing raw moment: spontaneous action, incidental framing and ordinary surroundings, while still readable | Eligible |

A steady propped phone can score 5; camera shake is not compulsory. Poor resolution, noise, sweat, crying and bathroom location do not prove rawness or authenticity. Reject glamour lighting, beauty smoothing, theatrical mugging or obviously artificial “candid” camera behavior when they undermine the intended organic look. Known reenactment and event authenticity are provenance fields, not facts established by this appearance score.

## Action and clean-frame gates

Record action/context match as `exact`, `partial` or `wrong`. Only exact qualifies. Preserve required subject/setting/action while broadening query vocabulary. A different emotional action is not equivalent because it is more intense.

Text status is `verified clean`, `text present` or `unverified`. Only verified clean qualifies as a completed visual selection. Every frame within the selected interval must be checked. Transient subtitles, moving watermarks and a text sticker appearing at the end all count. Examine visible background lettering as well. Do not mistake external player UI for embedded text; inspect the actual file or clean original player output.

Keep visual qualification and reuse readiness distinct:

`Visual pass = exact action + EV 5 + rawness ≥4 + verified text-free + sufficient usable duration + credible review evidence.`

`Production-ready = visual pass + confirmed usable asset access + appropriate reuse authorization.`

## Calibration examples — hypothetical, not sourced clips

| Described candidate | Decision and reason |
|---|---|
| Woman on toilet, relaxed face, hand casually resting on stomach, no text | Reject: right setting, low intensity; touching the abdomen is not enough |
| Woman on toilet, folded forward, abdomen tightly braced, sustained strained expression, natural phone capture, clean interval | Potential EV 5/rawness 4–5; select only after motion, complete text review and duration verification |
| Same strong action with “POV: cramps” across the picture | Reject current asset: text overrides emotional fit; seek a clean original or separate clean interval |
| Woman sobbing intensely on sofa when toilet setting is required | Reject: extreme but wrong action/context |
| Bathroom interview describing severe cramps with a neutral face | Reject: verbal claim supplies severity; the requested action is absent |
| One extreme grimace lasting 0.2 seconds in an otherwise mild clip for a three-second beat | Reject duration fit; do not loop or retime to create apparent intensity |
| Dramatic studio reenactment with slow motion and perfect beauty lighting | Reject rawness even if the expression is extreme |
| Raw spontaneous celebration, large face/body reaction, exact desired-outcome line, verified clean frames | Eligible positive-intensity footage; pain is not required |
| Perfect-looking preview; original video cannot be played | Unverified lead, no final score or clean-frame certification |

Calibrate new tasks against the user's approved examples when provided. Describe any borderline judgment explicitly; change anchors only when the user changes the desired standard.
