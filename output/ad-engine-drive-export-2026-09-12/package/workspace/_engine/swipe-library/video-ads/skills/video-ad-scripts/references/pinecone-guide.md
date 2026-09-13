# Pinecone Vector Database Guide

The video ad scripts skill has a companion Pinecone vector database containing 79 indexed ads across 3 brands (Balmbare, myNuora, Resilia). Use this to find reference ads, pull matching concepts, and ensure angle diversity.

## Setup

```python
from pinecone import Pinecone
from google import genai

# Initialize clients
pc = Pinecone(api_key='[REDACTED_SECRET]')
genai_client = genai.Client(api_key='[REDACTED_SECRET]')

# Connect to index
index = pc.Index('video-ad-scripts')
```

## Generating Query Embeddings

```python
def get_embedding(text):
    """Generate embedding using Google's gemini-embedding-001 model."""
    result = genai_client.models.embed_content(
        model='gemini-embedding-001',
        contents=text
    )
    return result.embeddings[0].values
```

## Query Patterns

### Find ads similar to a concept
```python
query_text = "hair loss from GLP-1 medications like Ozempic"
query_embedding = get_embedding(query_text)

results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True
)

for match in results['matches']:
    print(f"Score: {match['score']:.3f}")
    print(f"Brand: {match['metadata'].get('brand', 'N/A')}")
    print(f"Hook: {match['metadata'].get('hook', 'N/A')[:100]}")
    print(f"Angle: {match['metadata'].get('angle', 'N/A')}")
    print()
```

### Filter by brand
```python
results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True,
    filter={"brand": {"$eq": "balmbare"}}
)
```

### Filter by format type
```python
results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True,
    filter={"format": {"$eq": "expert_educator"}}
)
```

## Metadata Fields

Each vector includes:
- `brand`: balmbare, mynuora, or resilia
- `hook`: First 2-3 lines of the ad
- `angle`: Pain point targeted (e.g., "GLP-1 hair loss", "vaginal odor shame", "menopausal bloating")
- `format`: expert_educator, personal_discovery, or third_party_story
- `full_text`: Complete ad body text (truncated to 10K chars)
- `source_id`: Library ID if available
- `cta_style`: soft/hard + actual CTA text
- `status`: active/inactive

## When to Use

1. **Before writing a new script**: Query with the product/angle to find 2-3 matching reference ads. Read their full_text to internalize cadence
2. **Anti-mimicry check**: Query to see what angles/hooks have already been used for this product category
3. **Finding inspiration**: Query with the avatar's pain point description to surface unexpected angles from other brands
4. **Brief generation**: Query to find reference ads with similar formats for the editor to study

## Index Stats

- Total vectors: 79
- Dimension: 3072 (Google gemini-embedding-001)
- Metric: cosine similarity
- Brands: Balmbare (19), myNuora (29), Resilia (21) + additional scraped variants
