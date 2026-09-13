Each family has its own Google Omni film, source photographs, exact prompts, native provider receipts, extracted poster and visual review. `delivery-index.json` lists only accepted films; each family's `delivery.json` is the authority for the final file, hash, shot sequence, display ratio and known limitations. Rejected attempts remain archived for traceability and must not be deployed.

Final selection: Weekender, Meridian, Camille, Colette and Delphine each use an 18-second ten-shot film. Juliette uses the original nine-second five-shot film, whose complete front, suede body, handle crowns, corner cap and handle shaft provide the requested multiple views. Longer Juliette attempts introduced unsupported hardware, texture or folds and were excluded. Its opening wide still has AI-amplified surface grain at full resolution; the accepted film is a source-relative depiction, not exact measured suede microstructure.

The approved route is direct Google Gemini Interactions API, `gemini-omni-1.1-flash`, with a nine-second initial interaction and an optional native nine-second extension. An extension returns one cumulative 18-second MP4. A coherent five-shot initial film can be delivered as its original nine-second output when the extension adds unsupported details; consult the family's final manifest for actual duration. The file is decoded from the provider's inline base64 response without local assembly, trimming, transitions or re-encoding. No persistent provider download URL is returned in this configured delivery mode. No video framework or external editor was used. Use the current documented internal editor if a future task genuinely requires editing.

`generate_film.py` uses the configured transport in `../generate_studio.py`. The accepted studio first frame is a GPT Image 2 edit of the selected product source. Original product evidence and accepted material/corner references accompany it as explicitly bound image references. Each receipt retains the exact input hashes, prompt, interaction lineage, provider usage, output hash, video duration, container duration and frame count. No competitor footage was sent to the generation provider or included in the output.

To make a new attempt, create a new version and review its initial stage before extending it:

```sh
python3 generate_film.py --family FAMILY --stage 1 --attempt NEW_VERSION --prompt-file FAMILY/prompts/NEW_INITIAL.txt
python3 generate_film.py --family FAMILY --stage 2 --attempt NEW_VERSION --prompt-file FAMILY/prompts/NEW_EXTENSION.txt
```

Do not mark receipts approved before viewing the actual output. The script guards against overwriting existing media and requires an accepted initial interaction before an extension. Colette and Juliette have family-specific extension wrappers inside their directories; use their final receipts for the exact submitted prompt rather than assuming the generic shot plan.

The films borrow the reference site's restrained studio rhythm, hard cuts, exterior portraits and tactile close-ups. Shots are restricted to evidenced exterior views. Interiors, unseen rear construction, closure operations and hands were omitted when source evidence could not support them. Repeated text-only repair of a failing macro was avoided: unsafe flap, hardware or root shots were replaced with supported handles, body texture or corners. Product geometry and components are assessed against the selected source lineage; apparent size in these generated studio shots does not physically verify dimensions.

Read-only QA uses `qa/extract_review.py` and `qa/inspect_film.py`. These extract JPEG frames, detect candidate cut times, inspect audio and generate diagnostic desktop/mobile crops. They do not alter the MP4. Extended video streams are 18 seconds and 432 frames at 24 fps; unextended streams are nine seconds and 216 frames. The container can be slightly longer because of AAC padding. Native audio remains in the file, so storefront playback stays muted.

The normal PDP crop is desktop 1434/750 and mobile 390/420 with cover and focal position 50% 65%. Weekender needs mobile 390/360 to retain its outer side wings; this wider crop was reviewed. Delphine's accepted film contains one native transition blemish at frame 128 (5.333333 seconds), lasting 41.667 milliseconds just before a clean cut. Adjacent frames and the remaining construction are consistent; the exact bytes were retained and this limitation is recorded in its manifest.

Run `python3 build_delivery_index.py` after a family is accepted. It verifies the native film and poster hashes and refreshes the shared index. Root handles Shopify staging, native Video objects, posters and draft-theme assignments. This production task does not publish the store or certify product dimensions.
