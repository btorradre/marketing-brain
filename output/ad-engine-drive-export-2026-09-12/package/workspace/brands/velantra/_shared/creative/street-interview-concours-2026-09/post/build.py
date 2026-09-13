#!/usr/bin/env python3
"""VEL-STREET-CONCOURS-01 post build.
Per segment: burn the question cards (serif, top third) and word-synced phrase captions
(bottom, white with black halo), then export the solo cut. Then concat the three solos into the montage.
Usage: python3 post/build.py            (builds everything present in seedance/)
Inputs: seedance/W{n}.mp4, seedance/W{n}.words.json (OpenAI whisper verbose_json with word timestamps)
"""
import json, os, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEG=os.path.join(D,'seedance'); OUT=os.path.join(D,'final'); TMP=os.path.join(D,'post','tmp')
os.makedirs(OUT,exist_ok=True); os.makedirs(TMP,exist_ok=True)
W,H=1080,1920
SERIF='/System/Library/Fonts/Supplemental/Georgia.ttf'
SANS='/System/Library/Fonts/HelveticaNeue.ttc'
if not os.path.exists(SANS): SANS='/System/Library/Fonts/Supplemental/Arial.ttf'
# card schedule per segment: (start, end, text)
CARDS={
 1:[(0.0,3.5,'What are you wearing today?'),(14.0,16.0,'And the rest?'),(19.0,21.0,'Show us the arm')],
 2:[(0.0,3.5,'What are you wearing today?'),(14.0,16.0,'And the rest?'),(19.0,21.0,'Show us the rings')],
 3:[(0.0,3.5,'What are you wearing today?'),(14.0,16.0,'And the rest?'),(19.0,21.0,'And the watch?')],
}
NAMES={1:'VEL-STREET-CONCOURS-01-W1-WEEKENDER',2:'VEL-STREET-CONCOURS-01-W2-MERIDIAN',3:'VEL-STREET-CONCOURS-01-W3-VIVIENNE'}

def halo_text(draw_img, text, font, y, fill=(255,255,255)):
    """draw centred text with a soft black halo; returns nothing (draws on draw_img)"""
    layer=Image.new('RGBA',draw_img.size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    tw=d.textlength(text,font=font); x=(W-tw)/2
    for dx,dy in ((-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,2),(-2,2),(2,-2)):
        d.text((x+dx,y+dy),text,font=font,fill=(0,0,0,215))
    layer=layer.filter(ImageFilter.GaussianBlur(9))
    draw_img.alpha_composite(layer)
    d2=ImageDraw.Draw(draw_img); d2.text((x,y),text,font=font,fill=fill+(255,))

def card_png(text, path):
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    font=ImageFont.truetype(SERIF,74)
    lines=textwrap.wrap(text,22)
    y=int(H*0.07)
    for ln in lines:
        halo_text(im,ln,font,y); y+=92
    im.save(path)

def caption_png(text, path):
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    font=ImageFont.truetype(SANS,52)
    lines=textwrap.wrap(text,26)[:2]
    y=int(H*0.80)-(len(lines)-1)*62
    for ln in lines:
        halo_text(im,ln,font,y); y+=62
    im.save(path)

def phrases_from_words(words, max_words=4, max_gap=0.55):
    """group whisper words into short phrases (max 4 words, split on pauses)"""
    out=[]; cur=[]
    for w in words:
        if cur and (len(cur)>=max_words or w['start']-cur[-1]['end']>max_gap or cur[-1]['word'].rstrip().endswith(('.', '?', '!'))):
            out.append(cur); cur=[]
        cur.append(w)
    if cur: out.append(cur)
    res=[]
    for p in out:
        txt=' '.join(x['word'].strip() for x in p)
        res.append([p[0]['start'], p[-1]['end']+0.15, txt])
    for i in range(len(res)-1):
        if res[i][1] > res[i+1][0]-0.03: res[i][1]=max(res[i][0]+0.2, res[i+1][0]-0.03)
    return [tuple(r) for r in res]

SCRIPTS={
 1:"Honestly, my whole weekend is in this bag right now. This is the Weekender from Velantra. It's a Birkin-inspired shape that they scaled up into a travel bag, and there's no logo on it anywhere. Jacket's Veronica Beard, trousers are Frame, and the hat has no label. The cuff is David Yurman and the watch is a Rolex. It holds three days' worth of clothes and it still fits in the overhead bin, which is all I need.",
 2:"Honestly, everyone's been stopping me about this bag all day. This is the Meridian from Velantra. It's all pebbled leather with silver hardware, there's no logo on it anywhere, and my laptop actually sits flat inside it. The dress is Zimmermann, the hat is Janessa Leone, and the shoes are Aquazzura. The rings are David Yurman, and this little one was my grandmother's. Everyone assumes I paid way more for it than I did, which I kind of love.",
 3:"Okay, I'm going to start with the bag because it's brand new. This is the Vivienne from Velantra. It's that Birkin-inspired shape but it's soft, it's vegetable-tanned leather, and there's no logo on it anywhere. The coat is Max Mara, the trousers are Vince, and the boots are Manolo. It's a Cartier, it was a gift from my husband. It's on pre-order and ships in October, and they've got the whole collection on sale right now, link's below.",
}
import difflib, re
def norm(w): return re.sub(r"[^a-z0-9]","",w.lower())
def align_script(words, script):
    """Return script tokens with timings borrowed from whisper words (difflib alignment; unmatched tokens interpolate)."""
    st=script.split(); sn=[norm(t) for t in st]; wn=[norm(w['word']) for w in words]
    sm=difflib.SequenceMatcher(a=sn,b=wn,autojunk=False)
    times=[None]*len(st)
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=='equal':
            for k in range(i2-i1): times[i1+k]=(words[j1+k]['start'],words[j1+k]['end'])
        elif tag=='replace':
            # spread the whisper span across the script span
            s0=words[j1]['start']; e0=words[j2-1]['end']; n=i2-i1
            for k in range(n):
                a=s0+(e0-s0)*k/n; b=s0+(e0-s0)*(k+1)/n; times[i1+k]=(a,b)
    # fill any None by interpolation between neighbours
    for i,t in enumerate(times):
        if t is None:
            prev=next((times[j] for j in range(i-1,-1,-1) if times[j]),None)
            nxt=next((times[j] for j in range(i+1,len(times)) if times[j]),None)
            a=prev[1] if prev else 0.0; b=nxt[0] if nxt else a+0.4
            times[i]=(a,max(a+0.2,b))
    return [{'word':st[i],'start':times[i][0],'end':times[i][1]} for i in range(len(st))]

def build_segment(n):
    src=os.path.join(SEG,f'W{n}.mp4'); wj=os.path.join(SEG,f'W{n}.words.json')
    if not os.path.exists(src): print('missing',src); return None
    overlays=[]  # (png, start, end)
    for i,(s,e,t) in enumerate(CARDS[n]):
        p=os.path.join(TMP,f'W{n}-card{i}.png'); card_png(t,p); overlays.append((p,s,e))
    if os.path.exists(wj):
        words=align_script(json.load(open(wj)).get('words',[]), SCRIPTS[n])
        for i,(s,e,t) in enumerate(phrases_from_words(words)):
            p=os.path.join(TMP,f'W{n}-cap{i:03d}.png'); caption_png(t,p); overlays.append((p,s,e))
    # ffmpeg filter chain: scale to 1080x1920, overlay each png with enable window
    inputs=['-i',src]; fc=[f'[0:v]scale={W}:{H}:flags=lanczos,setsar=1[v0]']; last='v0'
    for k,(p,s,e) in enumerate(overlays):
        inputs+=['-i',p]
        fc.append(f"[{last}][{k+1}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[v{k+1}]"); last=f'v{k+1}'
    out=os.path.join(OUT,NAMES[n]+'.mp4')
    cmd=['ffmpeg','-y',*inputs,'-filter_complex',';'.join(fc),'-map',f'[{last}]','-map','0:a?','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',out]
    subprocess.run(cmd,check=True,capture_output=True)
    print('built',out); return out

def endcard(src, out, lines=("Every bag in this video","is on sale right now.","Link below.")):
    """3s freeze of the last frame of src with the offer card burned on"""
    png=os.path.join(TMP,'endcard.png')
    im=Image.new('RGBA',(W,H),(0,0,0,0)); f1=ImageFont.truetype(SERIF,78); f2=ImageFont.truetype(SANS,52)
    y=int(H*0.40)
    for ln in lines[:-1]: halo_text(im,ln,f1,y); y+=96
    halo_text(im,lines[-1],f2,y+30); im.save(png)
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src],capture_output=True,text=True).stdout.strip())
    last=os.path.join(TMP,'last.png')
    subprocess.run(['ffmpeg','-y','-ss',str(max(0,dur-0.1)),'-i',src,'-frames:v','1',last],check=True,capture_output=True)
    subprocess.run(['ffmpeg','-y','-loop','1','-i',last,'-i',png,'-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-filter_complex',f'[0:v]scale={W}:{H},setsar=1[b];[b][1:v]overlay=0:0,fade=t=in:st=0:d=0.3[v]','-map','[v]','-map','2:a','-t','3','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','192k','-shortest',out],check=True,capture_output=True)
    return out

def concat(paths, out):
    """re-encode join: normalize every input to 1080x1920, 24fps, 48k stereo, then concat filter"""
    inputs=[]; fc=[]
    for i,p in enumerate(paths):
        inputs+=['-i',p]
        fc.append(f'[{i}:v]scale={W}:{H}:flags=lanczos,setsar=1,fps=24,format=yuv420p[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[a{i}]')
    fc.append(''.join(f'[v{i}][a{i}]' for i in range(len(paths)))+f'concat=n={len(paths)}:v=1:a=1[v][a]')
    cmd=['ffmpeg','-y',*inputs,'-filter_complex',';'.join(fc),'-map','[v]','-map','[a]','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',out]
    subprocess.run(cmd,check=True,capture_output=True)
    print('built',out)

if __name__=='__main__':
    built=[build_segment(n) for n in (1,2,3)]
    built=[b for b in built if b]
    if len(built)==3:
        # montage = three clean segments + ONE offer end card after the last woman
        ec=endcard(built[-1], os.path.join(TMP,'endcard.mp4'))
        concat(built+[ec], os.path.join(OUT,'VEL-STREET-CONCOURS-01-MONTAGE-93s.mp4'))
    if built:
        # each solo also gets the end card so it can run alone
        for b0 in built:
            solo_ec=endcard(b0, os.path.join(TMP,'ec_'+os.path.basename(b0)))
            tmp=b0.replace('.mp4','.tmp.mp4'); concat([b0,solo_ec],tmp); os.replace(tmp,b0)
