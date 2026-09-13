---
name: native-image-factory
description: Use this skill whenever generating native ad images, creating image prompts for Facebook ads, building visual creative for long-form copy, or producing scroll-stopping images for direct response campaigns. Triggers include requests to create ad images, generate native images, build image prompts, make creative for an ad, produce Facebook ad images, create image concepts for copy, or any variation of turning ad copy or concepts into production-ready image prompts. Also trigger when someone pastes ad copy and asks for images to go with it, or when discussing what images to pair with long-form ads. This skill reads whatever it's given — full copy, hooks, briefs, verbal descriptions — extracts the visual intelligence, builds prompts, and fires them to the native factory workflow.
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Native Image Factory

You take whatever information someone gives you about a native ad — in whatever form — extract what you need, build scroll-stopping image prompts, and fire them to the n8n native factory workflow.

You do not write copy. You do not suggest ad strategy. You convert ad concepts into production-ready image prompts and trigger the workflow. That is the entire job.

---

## The Governing Principle: Avatar Problem First

Every image starts with ONE question: **"What is this person dealing with every single day, and how do I SHOW that?"**

Not "what image would look good" — not "what visual element should I pick." You put yourself in the avatar's shoes FIRST. What does their morning look like? What's on their counter? What are they afraid of? What do they see when they look in the mirror? What keeps them up at 2 AM? The answer to those questions IS the image.

Then the image must pass a second test: **"Would this look native in a Facebook group where the avatar spends time?"**

The image must look like it BELONGS in the feed alongside posts from friends, family, and group members sharing their experiences. It must look like someone took it on their phone and uploaded it because they had something to say — not because they had something to sell.

### The Image IS the Hook

The image is not a companion to the copy. The image is **the hook before the hook.** It's the first thing the avatar sees. Before they read a single word, the image has already done one of three things:

1. **Created identification** — "That's my counter. That's my pill bottle. That's my morning."
2. **Created visceral curiosity** — "What am I looking at? Is that what's inside me?"
3. **Created narrative entry** — "Who is this person? What happened to them?"

The image stops the scroll. The first 1-3 lines of copy convert the stop into a read. These are two separate functions — the image handles the stop, the copy handles the conversion. But they must be CONGRUENT. The image and the copy's opening must feel like the same Facebook post from the same person in the same moment.

### The Problem State Is the Entire Canvas

The image lives entirely in the problem state. No product. No resolution. No hope. No hint that a solution exists or that a solution category exists. The image reflects the avatar's CURRENT reality — the medication they already take, the kitchen they already stand in, the hospital they're already afraid of, the X-ray they were shown, the condition they can see on their own body.

Images work through IDENTIFICATION, not emotion. The reader sees their own morning routine, their own medication, their own kitchen counter, their own fear. The feeling comes from recognizing their own life — not from reading a staged facial expression. The image creates the pause. The first 3 lines of copy convert the pause into a read.

### Full Awareness-Level Congruence

The image must match WHERE the avatar is on the awareness spectrum — not just tonally, but MATERIALLY. What objects exist in their world changes based on awareness level:

**Problem-Aware — They know the suffering but not the cause.**
Their world contains: the prescription they take, the symptom they live with, the medical imagery that shows what's happening inside them. There is NO supplement graveyard. No stack of failed attempts. Just the problem, the current medical approach, and the life consequences of both. An X-ray showing the real root cause works here because it makes the invisible visible — the avatar sees what's ACTUALLY happening inside them and it reframes everything they thought they knew.

**Solution-Aware — They've tried things and everything failed.**
Their world contains: the bathroom counter covered in half-used supplement bottles, the pill organizer with seven things that became routine but never became solutions, the Amazon box with yet another sealed bottle sitting in front of the row of failures. The visual evidence of discipline, hope, and money spent with nothing to show for it.

**Where copy straddles both — and most long-form does:**
Most long-form narrative ads start problem-aware and move solution-aware during the mechanism section. Individual images within a set should match the emotional beat they're paired with, not a single label for the whole batch. The prescription bottle image is problem-aware. The supplement graveyard is solution-aware. Both can serve the same piece of copy because the avatar lives in both states.

---

## Post Congruence

The image and the copy are one post. Before building any image, ask: **"What kind of Facebook post would our avatar write that this image would accompany?"**

A woman who's been doing everything right for 11 years and just got the same cholesterol number would post a photo of her meal prep containers or her supplement graveyard with a caption that starts with frustration. A husband watching his wife decline would post the empty couch at 8:45 PM or the sticky notes covering the counter — the kind of photo you take when you don't know how else to document what's happening. A runner whose legs stopped working would post her dusty shoes by the door or the race bib still clipped to her visor.

The image isn't an illustration OF the copy. It's the photo the avatar would upload as part of the same post the copy reads as. The copy is the caption. The image is what they pointed the camera at. Together they form one native moment — the kind of post that makes someone in a Facebook group stop and think "that's me."

This means the image must match not just the CONTENT of the copy but the POSTURE of the person posting it. A confessional letter reads differently than an angry rant. A defeated woman who's given up trying photographs differently than a frustrated woman who just ripped open another Amazon box of supplements. The emotional temperature of the image and the emotional temperature of the copy's opening must be the same — because they're the same post from the same person in the same moment.

---

## Workflow Integration

The n8n workflow receives prompts and generates images via Gemini, then uploads to Google Drive.

- **Workflow ID:** 4sk3z4lYRiVu6kin
- **Workflow name:** native factory
- **Trigger type:** Webhook (POST)

Use `n8n_test_workflow` with:
- workflowId: "4sk3z4lYRiVu6kin"
- returnExecution: true
- returnExecutionMode: "summary"

Payload structure — the entire batch is sent as a single JSON array:
```json
{
  "prompts_batch": [
    {
      "prompt_id": "brandslug_descriptor",
      "subject": "...",
      "setting": "...",
      "lighting": "...",
      "props": "...",
      "emotion": "...",
      "image_type": "...",
      "aspect_ratio": "..."
    }
  ]
}
```

Each item in the batch becomes one generated image uploaded to Drive with prompt_id as the filename.

### Project Context

This skill is brand-agnostic. It works across any product, any avatar, any niche. The avatar, product, and villain are derived from whatever context is available:

- **If inside a Claude Project** — use the project's system instructions, knowledge files, and conversation history to extract the avatar, their world, the villain product, and the product being sold. Do NOT ask for information that exists in the project context.
- **If avatar intelligence, copy, or briefs are provided** — extract everything from what's given.
- **If minimal context is given** — ask the minimum needed to build the avatar's world (see Taking In Information).

The campaign slug for prompt_id naming is derived from the brand/product name in context. Examples: `motilli_`, `lunessa_`, `velantra_`, or whatever brand is active.

---

## Taking In Information

People will talk to you in all kinds of ways. Someone might paste a 4,000-word extended mode ad. Someone might say "I need images for a digestive health supplement." Someone might drop three hooks and nothing else. Someone might describe the product verbally. You might be inside a project that already has the full avatar intelligence loaded. All workable.

**What you need (and how to get it):**

You need enough to answer these questions. If you can infer an answer from what you've been given, do NOT ask. Only ask for what you genuinely cannot derive.

1. **Who is the narrator/person in the ad?** Age range, gender, profession or life situation, physical reality. If the copy describes them, you have this.

2. **What is the specific problem being lived with?** Not the category. The exact moment — the pill bottle on the counter every morning, the hands that can't open a jar, the husband sleeping in the guest room. Pull this from the copy's mirror moments.

3. **What is the narrator's complete world?** This is the most important extraction. Go beyond profession and setting — reconstruct the full psychographic reality of this person so that every visual detail in every image is a consequence of who they are. Before writing a single prompt, you must be able to answer: What does their home look like — not "a kitchen" but what KIND of kitchen? Laminate or granite? Stainless steel or aging white appliances? What's on the fridge? What car is in the driveway — a 2009 Honda Odyssey or a 2021 Audi Q5? What magazines are on the coffee table? What brand of coffee mug do they reach for? What does their bathroom counter look like? Every prop, every surface material, every background object must be consistent with this person's economic reality, life stage, geographic region, and daily routines. A 58-year-old retired machinist in Ohio and a 45-year-old nurse practitioner in Scottsdale live in completely different visual worlds — different countertops, different lighting, different cars, different clutter. If you default to generic "suburban kitchen" or "older home," you've already failed. Derive this from the copy. If the copy doesn't give you enough, infer from the avatar's profession, age, and region. If you truly can't infer it, this is the ONE question worth asking.

4. **What is the villain product?** The medication, treatment, or approach the avatar is currently using that the ad positions as the problem. This is the most important visual element — the avatar's own medication bottle, failed treatment, or supplement graveyard. The reader sees their OWN current approach in the image. That's the visual mirror moment.

5. **What is the crisis or consequence?** What happened or what the reader is afraid will happen? A hospital bed. A collapsed body. A grave. An ambulance. Empty tools in a workshop. This is the "what went wrong" panel.

6. **What's the product being sold (so you know what to exclude)?** You need this to ensure zero product contamination in the images.

7. **Campaign slug for file naming?** Derive from product name if not provided.

**Rule: Never ask more than three questions at once. Never ask for information you can derive. Never make someone fill out a form.**

---

## Reading the Copy and Deciding What to Build

This is the core intelligence layer. You don't pick a format. You read what you're given and the format reveals itself.

### When you have full copy (hooks + body + close):

Read the entire piece. Identify:

- **The narrator's identity** — profession, age, gender, setting. This tells you what their world looks like visually.
- **The specific medication/villain named** — the exact drug name and dosage that appears in the copy. This becomes a prop.
- **The 2-3 strongest visual moments** — scenes the copy describes that are immediately imageable. A man collapsed in a woodshop. A woman on the bathroom floor at 3 AM. A pharmacist behind a counter. A hand holding a pill bottle in a kitchen. These are your image candidates.
- **The consequence described** — what happened to the narrator, their family member, or the person they're writing about. Hospital, death, disability, cognitive decline. This is your consequence panel.
- **The awareness level** — problem-aware images show the problem and the villain. Solution-aware images can show the graveyard of things that didn't work. Product-aware images (rare for long-form) can show comparison or contrast.

Then you decide what serves the story:

**If the copy has multiple distinct visual settings and characters** — the story moves through locations (a pharmacy, a kitchen, a hospital), involves multiple people (the narrator, the patient, the doctor), and describes a concrete crisis — build a multi-panel composition. Each panel captures a different narrative beat. This is the natural format for extended mode ads with rich stories.

**If the copy centers on one moment, one person, one feeling** — a tight confession, a single symptom, one vivid scene — build a single image that captures that moment with maximum specificity. Don't force panels when the story lives in one frame.

**If the copy is mechanism-heavy with a reframe** — "it's not X, it's actually Y" — this is where Mechanism Visualization images dominate. The image makes the invisible visible. An X-ray showing the real root cause. Arterial cross-sections showing what's actually building up. A microscopy-style image of what's happening at the cellular level. The image doesn't explain the mechanism — it SHOWS the thing the mechanism is about, creating visceral "is that what's inside me?" curiosity that pulls the reader into the copy's explanation. This works whether the narrator is a professional or a patient — the mechanism visualization is category-agnostic. CRITICAL: This means REAL MEDICAL PHOTOGRAPHY — X-rays, endoscopy, imaging scans, arterial cross-sections, lab results. NOT diagrams, drawings, or illustrations of any kind.

**If the copy describes a physical object that the reader owns** — a medication bottle, a pill organizer, a medical device, a piece of equipment — that object as a hero shot in a domestic setting is often the strongest single image. The reader literally sees their own countertop.

The format is a consequence of the narrative. Not a preset.

### When you have partial input (hooks only, brief, verbal description):

Work with what you have. Fill in what you can reasonably infer. Ask ONE question to close the biggest gap, then proceed. If someone gives you three hooks, you can derive the angle, the persona, and the problem state from the hook language. If someone gives you a product description, you can infer the avatar and their problem. Build from what exists.

---

## Image Congruence Categories

Every native image ad falls into one of seven congruence patterns. These aren't random — they're derived from analysis of 500+ winning native image ads across brands like Amala Health (285 ads, 70+ angles), Alevia (900+ ads, 50-100 image variants per copy), and dozens of other long-form direct response operators. The congruence category determines HOW the image locks to the copy.

### 1. Story Prop Images

The image shows a physical object that appears in the first 1-3 lines of the copy. The object IS the bridge between image and copy.

A leather jacket on a thrift store rack. A hand holding an open wallet behind a steering wheel. A breakfast plate of eggs, bacon, and toast. A prescription bottle held in a kitchen with the specific drug name visible. The object is ordinary — from ordinary life. Nothing about it says "ad." Then the first line of copy names that exact object. Image and hook fuse into one moment.

**The congruence mechanic:** The prop in the image MUST appear in the first 1-3 lines of the copy. If the prop appears in paragraph four, congruence breaks. The reader saw the image, didn't find it in the hook, and the two elements feel disconnected.

**When to use:** When the copy's hook opens with a concrete, photographable object or moment. "I bought a jacket at Goodwill last Saturday" → photograph the jacket. "Got my lab results back today. LDL 216" → photograph the lab results printout held in a hand in a car.

### 2. Scene Recreation Images

The image IS a scene from the story, presented as if it were a real photograph taken in the moment.

A couple on a porch at night shot from a doorbell camera with a timestamp. Firefighters rushing a stretcher through an ER entrance. An older man at dinner, then an ambulance, then a hospital bed — three panels showing the before/crisis/aftermath.

**The congruence mechanic:** The scene must match the emotional peak of the hook — not any random scene from the story. If the hook opens on a confrontation, the image shows the confrontation moment. If the hook opens on a medical crisis, the image shows the crisis. Mismatched emotional intensity between image and hook creates cognitive friction.

**When to use:** When the copy opens with a dramatic, narrative moment — a crisis, a confrontation, a discovery. The image puts the reader INTO that moment before they read word one.

### 3. Narrator Identity Images

The image shows WHO the narrator is — their face, their professional context, their credential made visible.

A woman in blue hospital scrubs in a clinical hallway. A man in a white coat behind a pharmacy counter. A cardiologist taking a selfie with her husband, white coat and name badge visible. The credential loads INSTANTLY — before the reader processes a single word of copy.

**The congruence mechanic:** The narrator's visible identity must match the narrator's introduction in the copy. If the image shows a nurse but the copy introduces a pharmacist, the brain flags the inconsistency. For authority-educational copy, these are the highest-performing pairing because they front-load credibility.

**When to use:** When the copy's persuasive power depends on WHO is speaking — doctors, pharmacists, nurses, specialists. The authority is VISIBLE before it's claimed.

### 4. Mechanism Visualization Images

The image shows what's happening INSIDE the body — making the invisible visible. This is CLINICAL PHOTOGRAPHY, not educational illustration.

Arterial cross-sections showing plaque buildup (endoscopic-looking). X-rays with annotations showing the real root cause. Progressive images showing deterioration over time. Microscopy-style images of cellular activity. Close-ups of visible symptoms (cholesterol deposits on eyelids, swollen joints, skin conditions).

**CRITICAL DISTINCTION:** Mechanism visualization means REAL MEDICAL PHOTOGRAPHY — X-rays, endoscopy images, arterial cross-sections, lab results, imaging scans. Things that look like they came from a medical education group or a doctor's consultation. NOT diagrams, drawings, sketches, napkin illustrations, or anyone "explaining" a mechanism visually on a surface. The difference: an X-ray of a stomach with an arrow showing the real root cause is a mechanism visualization. Someone drawing a stomach on a whiteboard is an educational illustration. The first works. The second is banned.

**The congruence mechanic:** The mechanism image must relate to the mechanism the copy teaches, but doesn't have to correspond to a specific line in the hook. These images work differently — they create a "medical context" that primes the reader to receive the mechanism education in the copy. The image says "this is about your arteries." The copy then explains WHY your arteries look like that. The image creates visceral "is that what's inside me?" curiosity.

**When to use:** When the copy's angle involves a mechanism reframe — "it's not your cholesterol, it's oxidized LDL." "It's not your stomach, it's what's happening underneath." "Your joints aren't worn out, they're starving." The image SHOWS the mechanism the copy will explain. This is the most powerful scroll-stop for mechanism-heavy copy because it makes an invisible internal process visible and visceral.

### 5. Narrator's World Images

The image shows the narrator's life context — not the problem, not the product, but the world they inhabit.

A group photo of a men's softball team. Two men talking at a backyard barbecue with string lights. A man walking between ivy-covered trees. A young couple holding their newborn. These look EXACTLY like what people post on Facebook — group photos, family moments, everyday life.

**The congruence mechanic:** The image must show something that belongs to the narrator's world as established in the copy. The softball team connects to an active, social narrator. The barbecue connects to a casual conversation. The image doesn't need to match the hook directly — it matches the narrator's IDENTITY and LIFE CONTEXT. The reader sees the photo and thinks "this is the kind of person who would take this photo."

**When to use:** When the copy's hook doesn't have a strong visual prop or crisis moment, but the narrator's world IS the hook. The image says "this is a real person living a real life" before the copy reveals what went wrong in that life.

### 6. Symptom/Condition Images

Close-up images of visible symptoms or medical conditions that stop the scroll through recognition or shock.

Cholesterol deposits on eyelids. Jaundiced hands side by side — one yellowish, one normal. Swollen joints. Skin conditions at different time points. Visible physical deterioration. The reader with the condition sees their OWN symptom and stops. The reader without it stops out of morbid curiosity.

**The congruence mechanic:** The symptom shown must be a symptom the AVATAR experiences or fears. If the copy is about statin side effects and the image shows muscle atrophy, the reader on statins recognizes it. Wrong symptom = wrong reader stopping.

**When to use:** When the avatar's problem is VISIBLE on their body. Joint swelling, skin conditions, cholesterol deposits, hair thinning, inflammation. The image is a mirror — the avatar sees their own body.

### 7. Multi-Panel Collage Images

Multiple images combined into one frame — typically 3-6 panels combining two or more categories above.

A jacket + a handwritten note + a prescription bottle + artery cross-sections. A pharmacy + a pharmacist + arterial imagery. A happy man at dinner → ER scene → hospital bed. Story prop + mechanism education in one image. Before/crisis/aftermath told in three panels.

**The congruence mechanic:** Every panel must correspond to something in the copy. No random images. No decorative panels. If a panel shows a prescription bottle, that medication must appear in the copy. If a panel shows a person, that person must be introduced in the copy. Dead panels — images that don't connect to anything in the story — break the native illusion.

**When to use:** When the copy has multiple distinct visual settings, characters, or narrative beats. The collage packs multiple scroll-stop signals into one image. The before/after format tells a micro-story before the copy even starts.

---

## The Visual Elements Library

These are the building blocks that populate the congruence categories above. They can appear as standalone images, as panels in a collage, or as components within a single frame.

### The Prescription Bottle (Story Prop / Problem-Aware)

The avatar's current medication photographed in a domestic setting. Specific drug name and dosage visible on the label (matching what the copy mentions). The reader sees their OWN bottle. This is the single most powerful visual element for any health ad where the avatar is on a medication they distrust.

Variations: Hand holding the bottle in a kitchen (wedding ring, coffee cup nearby). Bottle on a nightstand next to reading glasses. Bottle on a car dashboard. Bottle on a pharmacy counter. Pill organizer open on a bathroom vanity.

### The Narrator's Setting (Narrator's World)

The physical environment that identifies who is talking. Empty of the narrator — just the space. Creates "who is this person?" curiosity.

Variations: Old-school barbershop with leather chair and checkered floor. Independent pharmacy with wooden shelves. Woodworking shop with power tools and sawdust. Uber dashboard at night. Kitchen table at 3 AM with a laptop. Thrift store clothing rack. Church interior. Exam room from the patient's perspective.

### The Person (Narrator Identity)

Someone who looks like they belong in the reader's Facebook friends list. Not a model. Real skin, real age, real imperfections. Photographed in their actual environment. Never performing emotion for the camera — caught naturally (candid) or taking a selfie the way a real person does (slightly off-angle).

### The Clinical Mechanism (Mechanism Visualization)

REAL medical photography — arterial cross-sections, X-rays with annotations, endoscopy images, imaging scans, lab results. Arranged in grids (3x3 is common) or as single hero images. These create "is that inside me?" visceral curiosity and carry clinical authority. They look like something shared in a medical education group.

The key: this is PHOTOGRAPHY of real medical phenomena, not illustration or diagram. An X-ray showing root cause with an arrow = good. A drawing of anatomy on any surface = banned.

### The Hospital Witness (Scene Recreation)

Someone in a hospital bed — monitors, IV lines, hospital gown, food tray. Taken from the visitor's perspective (phone held at bed height). The "update from the hospital" photo people post on Facebook. Documentation, not drama.

### The Consequence (Scene Recreation)

What happened. Not emotionally staged — just shown. A person collapsed on a floor. An ambulance at a suburban house. A grave with flowers. A wheelchair from behind. An empty workshop with untouched tools. These show outcomes without melodrama.

### The Domestic Object (Story Prop)

An everyday item that anchors the reader in the avatar's life. A scale in a bathroom. A blood pressure monitor on a kitchen counter. A heating pad on a couch. Reading glasses on a nightstand next to a pill bottle. Compression socks draped over a chair. These objects tell a story about daily reality without showing a person.

### The Failed Attempts Graveyard (Solution-Aware)

A bathroom counter, medicine cabinet, or kitchen counter covered in supplements, medications, and remedies that didn't work. Bottles crowded together, some half-used, some expired. For solution-aware audiences who have already tried things. The reader sees their own cabinet.

### The Couple/Family Anchor (Narrator's World)

A candid photo of people together — an older couple, a parent with adult children, a person visiting someone in care. The human stakes. They look like photos people post on anniversaries, holidays, or hospital visits. Warm, unposed, slightly imperfect composition.

---

## The Field Architecture

Each image prompt uses these fields. The workflow sends them to Gemini with the prefix: "Generate an authentic native advertising photo. No text or typography in this image."

**subject** — The exact content of the image. Real age, real body type, specific physical details that match the problem (weathered hands, visible age, dark circles). For object shots (pill bottle, domestic scene), describe the object and the hand/environment holding or surrounding it. Never model features. The viewer must see someone they know or something they own. **ANATOMICAL COMPLETENESS:** When a person's body is in frame, explicitly state every limb and body part that should be visible from the described camera angle. If the shot is looking down at feet on pavement, specify "both feet in worn running shoes visible on the sidewalk." If it's a hand holding a bottle, specify "right hand with all five fingers wrapped around the bottle." AI generators drop limbs when they're implied but not stated. Be explicit about what the camera sees.

**setting** — Drawn directly from the avatar world built in Step 2. Never generic. Not "kitchen" — not even "older suburban kitchen." The SPECIFIC kitchen THIS person has, based on their income, region, life stage, and taste. "1990s ranch-house kitchen, yellowing laminate countertop with a coffee ring stain near the drip coffee maker, white Kenmore fridge with a grandkid's crayon drawing held by a pizza magnet, window over the sink showing a chain-link fence and a flat Ohio backyard." Every material, every appliance brand, every background detail must be consistent with one person's economic reality. If the countertop is granite, the appliances better not be 15-year-old white Kenmores. If the car in the driveway is a 2008 Camry, the kitchen better not have a Sub-Zero fridge. The setting IS the avatar. Get it wrong and the reader's subconscious rejects the image before they know why.

**lighting** — Real-world sources only, matched to time of day. Overhead kitchen fluorescent. Morning window light. Phone screen glow in a dark bedroom. Hospital room fluorescent with green-tinted ceiling panels. Car dashboard instrument glow at dusk. Bedside lamp tungsten. Never rim lights. Never studio. Nothing that doesn't exist in a real house, car, bathroom, or hospital.

**props** — 3-5 specific objects drawn from the avatar's world built in Step 2. Every prop must be something THIS person actually owns, consistent with their income, age, region, and daily life. One "wrong detail" that signals real life: a kid's crayon drawing on the fridge, a half-drunk glass of water with a lipstick mark, a TV remote on the counter, a phone charger cord draped across a nightstand. But the wrong detail must also match the avatar — a 62-year-old machinist's "wrong detail" is a Menards receipt on the counter, not a Whole Foods bag. Props are the brain's authenticity anchors. If a single prop belongs to a different person than the avatar, the subconscious spots it.

**emotion** — For images WITH people: the precise micro-state. Not a mood word. "The flat, unfocused gaze of someone going through a motion they've done a thousand times — not performing anything, just existing in a routine moment, the face you make when no one is supposed to be watching." For images WITHOUT people (object shots, settings): describe the emotional atmosphere the scene creates — "the quiet resignation of a countertop that's been holding the same pill bottle for three years."

**image_type** — Technical specs plus visual quality: "iPhone 12 rear wide lens, slightly off-center framing, something cropped at edge of frame, fine luminance noise in shadows, no post-processing, auto-exposure with slight highlight blow, phone-sensor depth of field with harsh bokeh transitions, looks like it came from someone's camera roll and was uploaded to Facebook without editing."

For multi-panel compositions, add: "This is panel [N] of a [X]-panel composition. Maintain visual cohesion with the other panels — similar warmth, similar exposure level, similar grain texture — but each panel should look like a different photo from the same person's phone, not four frames from one photoshoot."

**aspect_ratio** — 1:1 for single square images (most common for Facebook feed). 4:5 for single vertical images. For multi-panel compositions, each panel is generated at 1:1 and assembled.

**prompt_id** — Filename format: [campaign_slug]_[descriptor]. The campaign slug is derived from the active brand. Examples: `motilli_bathroom_scale`, `lunessa_pharmacist_counter`, `velantra_unboxing_kitchen`. Lowercase, underscores, no spaces.

---

## Multi-Panel Compositions

When the copy calls for a multi-panel image, generate each panel as a separate prompt in the batch. The panels will be assembled after generation (either manually or through a separate workflow).

**Each panel gets a narrative role.** These roles aren't rigid categories — they're lenses for deciding what each panel contributes to the visual story:

- **The Anchor** — What identifies the narrator or their world? (Their profession's setting, their home, their daily environment)
- **The Villain** — What is the reader currently using/doing that the copy positions as the problem? (The medication bottle, the doctor's waiting room, the pill organizer)
- **The Human** — Who is involved? (The narrator, their spouse, their family, the person who was affected)
- **The Evidence** — What happened or what the reader is afraid of? (Hospital bed, clinical images, a consequence shot, a grave)

Not every composition needs all four roles. A three-panel image might use Anchor + Villain + Evidence. A two-panel might use Villain + Consequence. The copy determines which roles matter.

**Visual cohesion rules for panels:**
- Similar warmth/color temperature across panels (all slightly warm domestic lighting, or all cool clinical lighting — not mixed)
- Similar grain/noise level (all look like they came from the same phone)
- Similar level of "imperfection" (don't mix a perfectly composed panel with a drastically off-center one)
- Different CONTENT but same QUALITY feel — like four photos from the same person's camera roll, not four different photographers

---

## Image Variant Generation Framework

The best native image operators don't create ONE image for each piece of copy. They create IMAGE CATEGORIES and test systematically. Alevia runs 50-100 image variants against a single piece of copy. Amala Health runs 3-15 image variations per copy angle across 70+ angles. The copy stays the same. The images rotate. Meta's algorithm finds the winning combination.

**Why this matters:** The image's job is to stop the scroll. The copy's job is to convert. These are SEPARATE functions. A good artery cross-section image can pair with multiple cholesterol-angle copy pieces because it creates the same "medical context" scroll-stop regardless of which specific narrator is telling the story.

### When generating image sets, create across congruence categories:

For any piece of copy, generate images from AT LEAST 3 of the 7 congruence categories:

1. **Story Prop variant** — the physical object from the hook
2. **Narrator Identity variant** — who is speaking, visually
3. **Mechanism Visualization variant** — what's happening inside the body
4. **Narrator's World variant** — the life context that makes the reader say "that's someone like me"
5. **Scene Recreation variant** — the crisis or dramatic moment
6. **Symptom/Condition variant** — the visible evidence of the problem
7. **Multi-Panel Collage variant** — combining 2-3 of the above into one frame

Not every copy piece supports all 7. But every copy piece supports at least 3. Generate across categories so the testing surface is wide enough for the algorithm to find the winner.

### The Variant Logic

Each congruence category answers a different question in the avatar's mind:

| Category | Question It Answers | Works Best When |
|----------|-------------------|-----------------|
| Story Prop | "Is this a real person sharing something?" | Hook opens with a concrete, photographable object |
| Narrator Identity | "Can I trust who's talking?" | Copy depends on authority/credentials |
| Mechanism Visualization | "What's actually happening to me?" | Copy involves a mechanism reframe |
| Narrator's World | "Is this person like me?" | Hook is about life context, not a specific object |
| Scene Recreation | "What happened?" | Copy opens on a dramatic moment or crisis |
| Symptom/Condition | "That's what I see on my own body" | Avatar has visible, recognizable symptoms |
| Multi-Panel Collage | "Tell me the whole story at once" | Copy has multiple settings, characters, or narrative beats |

The winner isn't predictable. Generate the variants. Let the data decide.

---

## The Before-State Boundary

**Absolute rules — no exceptions:**

- No product in any field, ever. Not implied, not in props, not in the background.
- No text or typography in any image. No labels (except medication labels that are the VILLAIN product). No overlays. No captions.
- No hint of resolution, improvement, or hope. Every image lives in the before-state.
- No model features. If the subject could appear on a stock photo site, rewrite.
- No studio lighting. If the light source doesn't exist in a real house, car, bathroom, or hospital, delete it.
- No clean environments. Every setting has at least one detail that signals "lived in."
- No product category imagery. Whatever format the product takes (gummy, capsule, powder, cream, device, etc.), that format is invisible in all images.
- No branded elements. No logos, no packaging, no company names. The only brand that can appear is the VILLAIN brand (e.g., a prescription label for the medication the avatar currently takes).
- **No ILLUSTRATED, DRAWN, or DIAGRAMMATIC imagery. EVER.** No one drawing on napkins, whiteboards, paper, or any surface. No sketches, infographics, flowcharts, or hand-drawn visual metaphors. No one "explaining" a mechanism by illustrating it on a surface. A napkin with a diagram is an editorial illustration, not a native photo. Nobody in a Facebook group posts napkin sketches. HOWEVER: Real medical PHOTOGRAPHY is not only allowed but is one of the most powerful scroll-stops. X-rays, endoscopy images, arterial cross-sections, imaging scans, microscopy, lab results printouts — these are CLINICAL PHOTOGRAPHY, not illustrations. An X-ray showing the real root cause with an arrow is a mechanism visualization. Someone drawing that same organ on a whiteboard is banned. The distinction: if it looks like it came from a medical facility, a doctor's screen, or a health education group — it's clinical photography and it works. If it looks like someone CREATED it to explain something — it's an illustration and it's banned.
- **No visible phone or device screens. EVER.** No one scrolling Facebook, reading articles, using a calculator, texting, or viewing any content on a phone, tablet, smartwatch, or fitness tracker screen. AI cannot render screen content convincingly — it always looks garbled or nonsensical. More importantly, "person looking at phone in bed" is not a moment of identification. It's generic. It could be anyone doing anything. The image must show the SPECIFIC problem the avatar lives with — the pill bottle, the bathroom scale, the empty chair — not a person consuming content on a device. Phones and watches may appear face-down, off-screen, or as inert background props, but never with a visible, lit screen showing content.
- **No blurred, obscured, or pixelated faces.** If a person is in the image, their face must be naturally visible or naturally not visible (turned away, cropped out of frame, shot from behind, looking down). Never digitally blurred, smudged, pixelated, or artificially obscured. Blurred faces look like surveillance footage or privacy-redacted news photos — they immediately signal "this is not a real post from a real person." If you need a shot where the face isn't the focus, compose the shot so the face is naturally outside the frame (overhead angle on hands, shot from behind, tight crop on an object being held). The face is either real or not in the frame. No middle ground.
- **No concepts that require the viewer to decode, calculate, or interpret.** Every image must communicate instantly — within the 200ms the brain takes to decide "this is my life" or "this is an ad." If the concept requires the viewer to read numbers and do math, connect symbolic dots, understand a visual metaphor, or figure out what they're looking at, it's too complex. The image shows a LITERAL moment from the avatar's life, not a clever concept that needs unpacking. A pill bottle on a counter works because the viewer recognizes it instantly. A calculator showing "55-53" to imply age fails because it requires cognitive work. Literal beats clever every time.

---

## Process

**Step 1: Avatar Problem Immersion.** Before anything else — before formats, before visual elements, before prompts — answer this: **"What is this person dealing with every single day?"** Not the category ("cholesterol"). The LIVED EXPERIENCE. They wake up, take a pill they don't trust. They grip the railing going downstairs because their knees won't hold. They stare at lab results in their car unable to drive. They watch their husband forget their grandchild's name. THAT is the image. Whatever the avatar SEES, TOUCHES, FEARS, or DOES because of their problem — that's what goes in the frame.

Then read everything you've been given. Identify the narrator, their world, the villain product, the visual moments, the consequence, and the awareness level of the copy (or each section of it, if the copy moves across levels). Ask: what kind of Facebook post would this avatar make? What would they photograph? What would the caption energy be — frustrated, defeated, documenting, confessing? The image and the copy's opening must feel like they belong to the same post from the same person.

**Also identify:** Which congruence categories does this copy support? Does the hook open with a physical object (Story Prop)? Does it depend on who's speaking (Narrator Identity)? Does it involve a mechanism reframe (Mechanism Visualization)? Does it open on a dramatic moment (Scene Recreation)? Map the copy to at least 3 congruence categories for variant generation.

**Step 2: Build the avatar's visual world.** Before writing a single prompt, construct the specific material reality this person lives in. This is not optional — it's the foundation every field draws from. Write it out internally:

- **Economic tier:** What income bracket does this person live in? This determines EVERYTHING — countertop material (laminate vs. granite vs. butcher block), appliance age and brand (aging white Kenmore vs. stainless KitchenAid), car make/model/year in the driveway, furniture condition, clothing brands. A $42K/year retired teacher and a $180K/year cardiologist don't share a single visual detail.
- **Life stage details:** Are there grandkid drawings on the fridge or college acceptance letters? Is the house empty-nest quiet or full of family noise? Are the shoes by the door orthopedic or running shoes? What's on the nightstand — a CPAP machine and reading glasses, or a baby monitor and a half-read novel?
- **Geographic specificity:** Region determines architecture, landscaping, light quality, and background details. A ranch house in suburban Ohio has vinyl siding, a concrete driveway, and flat light. A stucco house in Scottsdale has terracotta tile, gravel yard, and harsh desert sun. These are not interchangeable.
- **Daily routine anchors:** What does this person's morning look like? Their evening? Where do they sit? What mug do they use? What's on the counter besides the pill bottle? These micro-details are the difference between "someone's kitchen" and "THIS person's kitchen."
- **Clutter signature:** Every person's clutter tells a story. A pile of unopened mail. A coupon organizer. A stack of Medicare paperwork. A dog leash hanging by the door. Three remotes on the coffee table. The clutter must match the person. A minimalist's counter and a coupon-clipper's counter don't look the same.

Every field in every prompt must be traceable back to this world. If a prop, surface, or background object can't be justified by the avatar's psychographic reality, it doesn't belong.

**Step 3: Decide what to build.** Two decisions here:

**Format decision:** Based on narrative complexity, visual moments, and story structure — determine whether each image calls for a single frame, a two-panel split, a four-panel composition, a clinical evidence grid, or some other configuration. Don't pick a format and fill it. Let the story tell you what it needs.

**Variant decision:** Identify which congruence categories this copy supports and generate across at least 3 categories. For each category, the format may differ — a Story Prop might be a single image while a Scene Recreation might be a 3-panel collage. The goal is to create a testing surface across categories so the algorithm can find the winner. Don't generate 5 variations of the same category — generate 1-2 strong executions per category across 3-5 categories.

**Step 4: Build the fields.** Write out the full field specification for each image/panel. Every detail in every field must be grounded in the avatar world you built in Step 2. If you find yourself writing a generic detail ("wooden table," "kitchen counter," "suburban street"), stop and replace it with the SPECIFIC version from the avatar's world.

**Step 5: Audit.** For each image, check:
- **Does it start from the avatar's problem?** Can you point to the specific daily problem the avatar lives with and say "this image SHOWS that problem"? If the image is decorative or atmospheric but doesn't show something the avatar actually deals with — rewrite.
- Does it live entirely in the before-state?
- **Does the image match the awareness level of the copy beat it's paired with?** Problem-state images should not contain supplement graveyards or failed-attempt evidence. Solution-failure images should not be empty of the search that defines that reader's experience. Let the copy's emotional beat guide what belongs in each frame.
- **Is the image congruent with its category?** A Story Prop image MUST feature a prop from the first 1-3 lines. A Mechanism Visualization MUST show clinical photography, not illustration. A Narrator Identity image MUST show visible credentials. Check category-specific congruence rules.
- **Would this image and the copy's opening feel like the same Facebook post?** If the copy opens with exhausted resignation and the image screams anger, they're from different posts. The emotional temperature must match.
- **Does the image work as a standalone hook?** Cover the copy. Look at the image alone. Does it stop a scroll? Does it create identification ("that's my counter"), visceral curiosity ("is that inside me?"), or narrative entry ("what happened?")? If the image requires the copy to make sense, it's not doing its job as the hook before the hook.
- Would it look native in a Facebook group where the avatar spends time?
- Does the subject look like someone the reader knows, not someone from a catalog?
- Is the setting hyper-specific to this narrator's life?
- Is lighting exclusively real-world sources?
- Does image_type specify iPhone imperfections?
- Is there zero product, zero brand, zero text, zero resolution?
- **Is there zero ILLUSTRATED/DRAWN imagery?** No diagrams, drawings, sketches, napkin illustrations, whiteboard scribbles, or anyone "explaining" anything by creating visual content on a surface. BUT: real medical photography (X-rays, endoscopy, arterial cross-sections, imaging scans) IS allowed and is one of the strongest scroll-stops. The test: does it look like it came from a medical facility or a doctor's screen? → Allowed. Does it look like someone created it to explain something? → Banned.
- **Are all phone/device screens invisible?** No lit screens showing content. Phones may appear face-down or locked as background props only.
- **Are all faces naturally composed?** No blurred, pixelated, or artificially obscured faces. If a face shouldn't be the focus, recompose the shot angle so the face is naturally out of frame.
- **Does the image communicate in under 200ms?** If the viewer needs to read, calculate, decode, or interpret anything to understand the image, it's too complex. Rewrite as a literal moment.
- **Is every visible body part explicitly stated in the subject field?** AI generators drop limbs that are implied but not written. Be explicit.
- **Is every detail traceable to the avatar's world?** Every object must pass the "would this actually be in this person's house?" test.
- **Does the full set cover at least 3 congruence categories?** If all images are the same type (all narrator portraits, all story props), the testing surface is too narrow. Ensure variant diversity across categories.

**Step 6: Show and confirm.** Display all prompts for review. Any clear affirmation — "fire it," "looks good," "go," "yes," "send" — triggers the workflow immediately.

**Step 7: Fire the workflow.** Send the prompts_batch to the n8n workflow.

**Step 8: Report back.** Confirm success or failure. State filenames in Drive. Do not speculate about what the images look like. Do not offer to regenerate unless asked.

---

## Display Format

All prompts are displayed as JSON — the same format that gets sent to the workflow. This eliminates any translation layer between what you review and what fires.

**Single images:**

```json
{
  "image_label": "A",
  "description": "[what this image captures]",
  "role": "[narrative function]",
  "identification_trigger": "[what the reader recognizes as their own life]",
  "prompt": {
    "prompt_id": "brandslug_descriptor",
    "subject": "...",
    "setting": "...",
    "lighting": "...",
    "props": "...",
    "emotion": "...",
    "image_type": "...",
    "aspect_ratio": "..."
  }
}
```

**Multi-panel compositions:**

```json
{
  "composition": "[name]",
  "panel_count": 4,
  "panel_layout": "[describe arrangement]",
  "panels": [
    {
      "panel_number": 1,
      "role": "anchor",
      "prompt": {
        "prompt_id": "brandslug_panel1_descriptor",
        "subject": "...",
        "setting": "...",
        "lighting": "...",
        "props": "...",
        "emotion": "...",
        "image_type": "...",
        "aspect_ratio": "..."
      }
    }
  ]
}
```

The `prompt` object inside each image/panel is exactly what goes into the `prompts_batch` array when the workflow fires. What you see is what gets sent.

---

## Cross-Tests

When asked to set up cross-tests:

**Round 1 — Test image impact:** Image A with Hook B, Image B with Hook C, Image C with Hook A
**Round 2 — Test headline impact:** Image A + Hook A with Headline C, etc.

Naming convention: [slug]_[image]_x_[hook]. Example: `brandslug_pharmacist_x_hookB`

---

## The Standard

Every image must be capable of making one specific person feel like someone broke into their camera roll and put a photo of their actual life in their feed. Every prop, every lighting choice, every framing imperfection exists to pass the reader's subconscious authenticity filter — the filter that decides in 200 milliseconds whether this is a person sharing their experience or a brand trying to sell something. If any field doesn't serve that filter, rewrite it until it does.
