import os, sys, time, io
from google import genai
from google.genai import types
from PIL import Image
ENV={}
for l in open(os.path.expanduser("~/Documents/marketing brain/.env")):
    l=l.strip()
    if "=" in l and not l.startswith("#"):
        k,v=l.split("=",1); ENV[k]=v.strip().strip('"').strip("'")
client=genai.Client(api_key=ENV["GEMINI_API_KEY"])
P=os.path.expanduser("~/Documents/marketing brain/brands/velantra/products/cashmere-tote")
refs=[Image.open(f"{P}/product-references/colette-canonical-caramel-v3.png"),
      Image.open(f"{P}/product-images/square-1to1-2026-08-16/colette-v4-caramel-side.png")]
prompt=("Use the attached product photos ONLY as the reference for the bag's shape, proportions, materials, colours and hardware. Do NOT copy their lighting, plain background or catalogue look. "
"Create this real photograph instead: a vertical 9:16 iPhone video frame, shot handheld by a woman filming herself in a bedroom mirror, phone covering her face, the bag hanging from her forearm at hip height against a long camel wool coat and jeans. Lived-in bedroom visible around the mirror, unmade bed, morning window light from the side, slightly underexposed, framing a little crooked. "
"PRODUCT TRUTH: oatmeal greige brushed wool felt east-west tote, about twice as wide as tall, two wide vertical felt straps on the front face, a slim warm cognac leather belt about half an inch wide crossing the front through the felt straps with both ends curving outward and downward finished with small round aged gold disc caps, two rolled top handles wrapped in cognac leather on the grip with felt below, short handle drop, fully open top, no flap, no zipper, no logos, no lettering. "
"Real photo evidence: sensor noise, slightly blown window highlights, imperfect focus, phone sharpening, a trace of motion blur. Not a render, not CGI, not a catalogue shot. No on-screen text.")
for model in sys.argv[1:] or ["gemini-3-pro-image-preview","gemini-3.1-flash-image-preview"]:
    t0=time.time()
    try:
        resp=client.models.generate_content(model=model, contents=[*refs, prompt],
            config=types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="9:16")))
        n=0
        for part in resp.candidates[0].content.parts:
            if getattr(part,"inline_data",None) and part.inline_data.data:
                out=os.path.join(os.path.dirname(__file__),"..","probes",f"probe_{model.replace('.','_')}.png")
                open(out,"wb").write(part.inline_data.data); n+=1
                print(model,"OK",out,Image.open(out).size,f"{time.time()-t0:.0f}s")
        if not n: print(model,"no image part", resp)
    except Exception as e:
        print(model,"ERR",str(e)[:400])
