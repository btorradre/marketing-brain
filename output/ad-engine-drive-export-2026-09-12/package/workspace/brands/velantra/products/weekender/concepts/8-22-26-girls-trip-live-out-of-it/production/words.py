import json, pathlib
al=json.loads(pathlib.Path("vo/take2_align.json").read_text())
ch=al["characters"]; st=al["character_start_times_seconds"]; en=al["character_end_times_seconds"]
words=[]; cur=""; s=None
for c,a,b in zip(ch,st,en):
    if c.strip()=="":
        if cur: words.append((cur,s,prev_b)); cur=""; s=None
    else:
        if not cur: s=a
        cur+=c; prev_b=b
if cur: words.append((cur,s,prev_b))
# display-word map: TTS text uses Vell-Ahn-Trah, caption should read Velantra
pathlib.Path("vo/take2_words.json").write_text(json.dumps([{"w":w,"s":round(a,3),"e":round(b,3)} for w,a,b in words]))
print("total", round(words[-1][2],2), "s |", len(words), "words")
for w,a,b in words: print(f"{a:6.2f} {b:6.2f}  {w}")
