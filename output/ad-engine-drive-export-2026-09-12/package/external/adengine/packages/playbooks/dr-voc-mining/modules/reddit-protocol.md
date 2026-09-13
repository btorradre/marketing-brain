# Reddit / open-conversation protocol

For sources where nobody knows a brand is listening: Reddit threads, forum posts, TikTok and YouTube comment sections on category content, Facebook groups, Amazon reviews of competitor products.

This is the most honest focus group available. People describe their problems without performing for a brand, which is exactly why the language is usable and why prospect-side pain (not customer-side satisfaction) is what this protocol harvests.

## Operating rules

1. **Direct quotes only.** Every insight carries the exact language it came from, with a link. Never paraphrase.
2. **Frequency matters.** Note how many times each theme appears. High-frequency pain is mass-market pain, which is the best candidate for top of funnel.
3. **Rare signals get flagged, not dropped.** A pain mentioned once may be the angle nobody is running. Every outlier gets an entry and an explanation of its hook potential.
4. **Separate problem language from solution language.** Someone describing a problem sounds nothing like someone who has found a fix. Both are useful, at different awareness levels. Tag which is which.
5. **Never editorialise.** Map the language, do not judge it. The person writing "I look pregnant by 3pm and I hate myself for it" gets recorded exactly that way.

## Output sections, in order

### SECTION 1 — PAIN POINT MAP

Every distinct pain expressed. For each:

- The pain in their exact words, with the thread URL
- **Frequency**: dominant / common / occasional / rare, with the count
- **Awareness level**: unaware / problem / solution
- **Golden nugget**: the motive under the pain
- **Creative application**: what kind of hook this pain supports

### SECTION 2 — FAILED SOLUTION LIBRARY

Every mention of something tried that did not work. For each:

- What they tried
- Why it failed, verbatim
- A ready-to-test hook that opens on that failed solution

Same Law 6 gate as the reviews protocol: keep the named brand in the index, strip it from the hook.

### SECTION 3 — EMOTIONAL LANGUAGE EXTRACTION

Every emotionally charged phrase, metaphor, hyperbole, or vivid description. This section produces more usable hook copy than any other. For each:

- The exact phrase
- The emotion it expresses
- How it functions: hook / body line / UGC opener

### SECTION 4 — COMMUNITY DIALECT

Slang, shorthand, insider phrases, and recurring references that appear across multiple posts. These are the words the audience uses with each other rather than with a brand. Using one correctly signals membership faster than any proof element.

Flag any term that would read as a tell if used wrong.

### SECTION 5 — WEAK SIGNALS

Every pain or desire appearing only once or twice that carries high hook potential. For each:

- The quote
- Why it has potential despite low frequency
- 2 to 3 hook variations built from it

Weak signals feed the `fresh` end of the angle bank. They are where a differentiated position comes from, because by definition nobody is running them.

### CLOSE

The single highest-potential hook from the entire dataset, with one paragraph on why.

## Sourcing note

There is no Reddit MCP connected. Get the raw material by having the user paste threads, or by using `WebFetch` on specific thread URLs, or `mcp__playwright__browser_navigate` for subreddit search pages. Record the URL and the retrieval date on every quote. Never reconstruct a Reddit quote from memory of what that community typically says.
