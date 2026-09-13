# Meta Ads Library — Static Ad Collection Summary

## Overview

This collection contains **291 unique static ad images** scraped from the Meta Ads Library, split into two categories: supplement brands and fashion brands. All images are deduplicated by content hash and filtered to exclude profile pictures and thumbnails.

---

## Supplement Ads (172 images)

| Brand | Category |
|-------|----------|
| Primal Viking | Men's health / testosterone |
| Alpha Grind | Men's health / testosterone |
| Nugenix | Testosterone booster |
| Force Factor | Men's health supplements |
| Athletic Greens (AG1) | Greens / multivitamin |
| Organifi | Green juice / wellness |
| Ryse Supplements | Pre-workout / fitness |
| Jocko Fuel | Fitness / discipline supplements |
| Ancestral Supplements | Organ meats / ancestral health |
| Tongkat Ali brands | Testosterone / men's vitality |
| Ashwagandha brands | Adaptogen / stress / testosterone |
| Liver King / Ancestral | Organ supplements |
| Seed | Probiotics / gut health |
| Bloom Nutrition | Greens / women's wellness |
| Onnit (Alpha Brain) | Nootropics / brain health |
| Momentous | Performance nutrition |

**File naming:** `supplement_ad_0001.jpg` through `supplement_ad_0172.jpg` (with some `.png` and `.webp`)

---

## Fashion Ads (119 images)

| Brand | Category |
|-------|----------|
| Nike | Athletic / sportswear |
| Zara | Fast fashion |
| H&M | Fast fashion |
| Shein | Online fast fashion |
| Gymshark | Fitness apparel |
| Lululemon | Athletic / athleisure |
| Ralph Lauren | Premium fashion |
| Calvin Klein | Designer fashion |
| Adidas | Athletic / sportswear |
| Fashion Nova | Online fashion |
| Tommy Hilfiger | Premium fashion |
| Gucci | Luxury fashion |
| Versace | Luxury fashion |
| Puma | Sportswear |
| ASOS | Online fashion |

**File naming:** `fashion_ad_0001.jpg` through `fashion_ad_0119.jpg` (with some `.png` and `.webp`)

---

## Source

All ads were scraped from the **Meta Ad Library** (facebook.com/ads/library) filtered by:
- Country: United States
- Media type: Images only
- Sorted by: Total impressions (descending) where available

## Notes

- Images are at 600x600 or 1080x1080 resolution depending on availability
- All images are deduplicated by MD5 hash
- Images smaller than 5KB were excluded as likely non-ad content
- Collection date: March 2026
