# Higgsfield Hooks & Settings (UGC-family Presets Only)

Hooks and settings are Marketing Studio's reusable openers and locations. They apply ONLY to `--mode` values: `ugc`, `ugc_how_to`, `ugc_unboxing`, `product_review`, `ugc_virtual_try_on`. For `product_showcase`, `tv_spot`, `wild_card`, `virtual_try_on` — DO NOT pass `--hook_id` or `--setting_id` (server validation rejects).

## How to Use

1. Pick a hook (the opener) and/or a setting (the location).
2. Pass the IDs to `higgsfield generate create marketing_studio_video --hook_id <uuid> --setting_id <uuid>`.
3. Both are optional. Defaults are auto-picked by Marketing Studio if omitted.

To get the live full list:
```bash
higgsfield marketing-studio hooks list --size 100 --json | jq '.items[] | {id, name, type}'
higgsfield marketing-studio settings list --size 100 --json | jq '.items[] | {id, name, type}'
```

The lists below are a snapshot — Higgsfield adds new ones often. **Re-fetch before any production run.**

## Hook Catalog (snapshot)

Hooks are openers that solve the "stop the scroll in the first 1.5s" problem. Two types: `subtle` (natural, narrative) and `stunt` (chaotic, attention-grabbing).

| Name | Type | ID | Use For |
|---|---|---|---|
| Product Hit | stunt | `3d45fb46-254f-4c83-9685-8e3d28945a67` | High-energy ads, sports, snacks, tech |
| Spicy | subtle | `75b6d501-be0e-4416-a7ed-52f04f180574` | Beauty, makeup, fashion (close-up to selfie reveal) |
| Interview | subtle | `26cac2dd-99cb-4818-a678-509b0dab2c32` | Lifestyle/aspirational (Erewhon-style, food, wellness) |
| Random Object Mic | stunt | `d50eb41c-fcfa-4f4d-93aa-473cdc6bc3b2` | Comedy, viral-bait, casual products |
| Product Crash | subtle | `8101cd3e-3cc9-4607-a171-3582daa2f6ee` | Durability proof, drama-pivot reviews |
| Blizzard | stunt | `31976cc7-e597-4be2-9753-4a80153b0cc7` | Outdoor/durability, electronics, drinks |
| Camera Bump | subtle | `2db84ed8-7082-4981-9c9c-9d61b3c28668` | Fashion, accessories, casual reveal |
| Product Dodge | stunt | `5443eff1-d940-4ad3-9413-957bb048a6b0` | Fast-paced reviews, snacks, tech |
| Epic Fail | subtle | `ec9fdf99-314d-480d-a656-10d9861341e7` | Comedy, casual UGC, fitness products |

## Setting Catalog (snapshot)

Settings are the location/environment. Two types: `realistic` (everyday) and `unrealistic` (surreal/cinematic).

| Name | Type | ID | Use For |
|---|---|---|---|
| Bedroom | realistic | `b8368076-35eb-4045-b33b-74b2646d9863` | Wellness, sleep, beauty, supplements (evening routine) |
| Bathroom | realistic | `189fa1ac-1fdc-44f4-bdea-8804a76f0659` | Beauty, skincare, hygiene, supplements (mirror selfie) |
| Kitchen | realistic | `a0eb0be9-f0ff-4aee-9dee-69d9fd20110a` | Food, supplements, gummies, drinks (daily-routine) |
| Gym | realistic | `6bfbe372-e50a-4900-adee-d4cbd0db8a2f` | Fitness, recovery, energy, supplements |
| Office | realistic | `d39dda10-643c-44e2-bfc8-2451dddde7d9` | Productivity, focus supplements, work-from-home |
| In Car | realistic | `fdfa032c-801f-4602-8dfd-1162b0f8c9c9` | Yapper-style ads, errands-day energy |
| Street | realistic | `8c95f9ba-5849-44b1-82d0-9f6b33240758` | Fashion, accessories, urban discovery |
| Nature | realistic | `10f47b85-abd7-4899-b6b6-91ff2969d3bf` | Outdoor gear, wellness, mindfulness, fashion |
| Airplane Wing | unrealistic | `b03705e5-bbed-4d83-8d29-3bc2101cd14f` | Surreal viral-bait, durability claims |
| Roofing | unrealistic | `3cf2164e-ffac-4867-9c43-1d673a5cb28a` | High-energy lifestyle, "unbothered" attitude |
| Volcano Rim | unrealistic | `e99c2ee8-3c4a-4697-9a58-908e73c9ad38` | Extreme durability, viral comedy |
| Tiny Reviewer | unrealistic | `f495493f-0251-4bd7-afc0-90bc6a862e04` | Scale-play, hero product showcase |
| Car Roof | unrealistic | `d6992aea-4521-4606-9e4f-8c766e12622c` | Action/lifestyle, never-flinch energy |
| Train Surf | unrealistic | `71f61bb0-dfd9-459b-a220-0dd468b977d5` | Wind/durability proof, viral stunt |

## Brand → Default Hook + Setting

Starting points to test from. Override based on the specific reference ad.

| Brand | Default Hook | Default Setting | Reasoning |
|---|---|---|---|
| Motilli (GLP-1 / gut) | Spicy or Interview | Kitchen or Bedroom | Wellness daily-routine framing — feels native, not stunt-y |
| Lunessa (heart health, 50+) | Interview | Kitchen or Nature | Authority-trust avatar; quiet, credible settings |
| Velantra Boat Tote | Camera Bump or Spicy | Street or Nature | Fashion accessory native context |
| Velantra Meridian | Spicy | Street or Office | Premium-everyday positioning |
| Velantra Weekender | Spicy | Nature or In Car | Travel context |
| Avelle | (TBD) | (TBD) | Confirm category before defaulting |
| Solorna | (TBD) | (TBD) | Confirm category before defaulting |

Add a row here whenever you onboard a new brand — pattern is: default hook + default setting + one line of reasoning tied to the brand's positioning.

## Stunt Hooks: When to Use

Stunt hooks (`Product Hit`, `Random Object Mic`, `Blizzard`, `Product Dodge`, `Volcano Rim` etc.) are for top-of-funnel scroll-stoppers — they trade trust for attention.

- **Use for:** new audience cold traffic, pattern-interrupt creative tests, "viral angle" experiments
- **Avoid for:** high-trust niches (medical, financial, premium luxury) where the absurdity undermines authority. For Lunessa and Motilli, prefer subtle hooks. For Velantra Meridian (premium leather), avoid stunt hooks entirely.

## Combining With Brand Voice

The hook + setting + adapted-script chain works best when the script LEANS INTO the chosen scene rather than ignoring it. Example:

- Setting = Volcano Rim + Brand = heart-health supplement for 50+ women: bad fit, kills trust.
- Setting = Volcano Rim + Brand = energy drink with an "extreme durability" angle: great fit; reference the volcano in the script.
- Setting = Kitchen + Brand = a gummy supplement: natural fit; have the avatar reach for the gummies between food prep.

When in doubt, the realistic settings (Bedroom, Kitchen, Bathroom, Gym, Office, In Car, Street, Nature) are safer for direct-response performance. Surreal settings reward the right brand fit but burn engagement when forced.
