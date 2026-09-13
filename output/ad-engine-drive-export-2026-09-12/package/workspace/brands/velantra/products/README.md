# Velantra — Products

Organized **product-first**: one folder per product; inside each, its own creatives and assets grouped by type.

```
products/<product>/
├── product-references/   # canonical product/colorway reference images (for i2i)
├── product-images/       # generated/edited product shots
├── statics/              # static ad creatives
├── ugc/                  # UGC clips
├── ugc-ripped/           # ripped competitor/source UGC (TikTok rips)
└── video/                # generated video ads
```

Products: `boat-tote` · `weekender` · `meridian` · `straw-birkin` · `jelly-tote` · `inspired-birkin` · `bergen` (placeholder).

Non-product assets live in `../_shared/` (theme-build, ugc-creators, references, experiments, omnisend, site-assets).

> Skill registries point at `brands/velantra/products/<product>`. Add a new product by making `products/<name>/` with the same subfolders.
