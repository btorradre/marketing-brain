from pathlib import Path
import json,subprocess
b=Path(__file__).resolve().parent.parent
beats=json.load(open(b/'edit/beats.json'))
source_url='https://www.facebook.com/61587741773603/posts/122123193285258059/'
lanes=[]
for reference in [True,False]:
 items=[]
 for z in beats:
  f=(b/'edit/reference-analysis/selected-frames' if reference else b/'storyboard/final-composites')/(z['id']+'.jpg');assert f.exists(),f
  visual=('Original held 2×2 designer-bag grid, continuous cream-blouse presenter and white outlined phrase captions.' if reference and z['id']=='H1' else z['visual'])
  why=('Original grid establishes designer style aspiration under the long hook and bridge; this intent is inferred from narration.' if reference and z['id']=='H1' else z['why'])
  items.append({'t':f"{z['id']} · {z['in']/30:.3f}–{z['out']/30:.3f}s",'script':z['line'],'frame':str(f),'visual':visual,'emotion':why,'note':z['cut_cue']+' Direct cuts; preserve original presenter, voice and caption timing.'})
 lanes.append({'label':'EXACT FACEBOOK SOURCE — REFERENCE' if reference else 'FINAL FOUR-COLOR REVISION','source':source_url if reference else 'Native DaVinci Resolve final · 1080×1920 · 30fps · 51.3s','beats':items})
spec={'title':'Weekender — Old money / four-color women','project':'velantra','summary':'The exact selected old-money ad, with one change: its opening grid shows four different women carrying the Weekender. Cognac top-left, Army Green top-right, Dark Chocolate bottom-left, Black bottom-right. Fashion aspiration leads through four distinct outfits and natural settings. Original narration, cream-blouse presenter, caption style, body scenes and 51.3-second edit are preserved.','timelines':lanes,'notes':[{'title':'Grid order and presenter clearance','text':'Cognac / Army Green across the top; Dark Chocolate / Black across the bottom. The silver-haired woman raises Dark Chocolate beside her face so the original lower-left presenter leaves its front visible.','color':'#dff2e1'},{'title':'Locked source timing','text':'Grid holds from frame 0 through 357. Product-body cut is frame 358 (11.933s). End is frame 1539 (51.300s). Keep every original spoken word, voice pace, pause edit, caption phrase and CTA.','color':'#fdf3c9'},{'title':'Selected first assets','text':'The final lane shows the actual rendered hook and each retained body scene, including the original pickup motion first frame. The clean selected hook is below. The reference lane remains separate.','color':'#f7f5ee'}],'moodboard':[{'image':str(b/'storyboard/assets/fourcolorgridselected.png'),'caption':'SELECTED CLEAN HOOK — four distinct women and the exact requested color order. Actual final composite appears in the revision lane.'}]}
p=b/'storyboard/cutroom-spec.json';p.write_text(json.dumps(spec,indent=2));workspace=next(x for x in b.parents if (x/'cutroom/board_builder.py').exists());subprocess.run(['python3',str(workspace/'cutroom/board_builder.py'),str(p),'--slug','weekender-old-money-four-colors-2026-09-13'],check=True)
