import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';
const R=path.dirname(fileURLToPath(import.meta.url)),P=path.resolve(R,'../..'),ROOT=path.resolve(P,'../../../..');
const kitPath=path.resolve(ROOT,'../marketing-apps/adengine/packages/timeline/dist/index.js');
const {createProject,createLog,append,validateProject}=await import(pathToFileURL(kitPath));
const nativeRoot='/Users/brooksorradre2/Movies/CapCut/User Data/Projects/com.lveditor.draft/MOT-VID-013-HOOK-A-Remedy-Cabinet';
const nativePath=path.join(nativeRoot,'draft_info.json');
const native=JSON.parse(fs.readFileSync(nativePath)),shots=JSON.parse(fs.readFileSync(path.join(R,'shot-plan.json'))),schedule=JSON.parse(fs.readFileSync(path.join(R,'native-picture-segments.json')));
const out=path.join(R,'internal-editor');fs.mkdirSync(out,{recursive:true});
const toTicks=us=>Math.round(us*.006),seconds=s=>Math.round(s*6000),resolveNative=s=>path.join(nativeRoot,'Resources',path.basename(s));
const author={kind:'agent',id:'codex-mot013-r3'},at=new Date().toISOString();let seq=0;
const op=(type,body)=>({id:`r3-op-${++seq}`,type,author,at,...body});
const assets=[],ops=[],assetMap=new Map(),sourceNotes=[];
function addAsset(file,kind,id){
 if(assetMap.has(file))return assetMap.get(file);
 if(!fs.existsSync(file))throw Error(`Required source not ready: ${file}`);
 const a={id,kind,name:path.basename(file),url:pathToFileURL(file).href,provenance:{source:file}};
 if(kind==='video'||kind==='audio'){
  const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',file],{encoding:'utf8'}));
  a.duration=seconds(Number(probe.format.duration));const v=probe.streams.find(x=>x.codec_type===kind);
  if(kind==='video'){a.width=v.width;a.height=v.height;const [n,d]=v.r_frame_rate.split('/').map(Number);a.fps=n/d;}
  else a.sampleRate=Number(v.sample_rate);
 }else{a.width=1080;a.height=1920;}
 assets.push(a);assetMap.set(file,id);return id;
}
function transform(s){const c=s.clip??{},t=c.transform??{};return {x:(t.x??0)*540,y:-(t.y??0)*960,scale:c.scale?.x??1,rotation:c.rotation??0,opacity:c.alpha??1,anchor:{x:.5,y:.5}};}
ops.push(op('addTrack',{track:{id:'picture',kind:'video',name:'R3 distinct visuals',muted:true}}));
for(let i=0;i<schedule.length;i++){
 const n=schedule[i],s=n.segment,row=shots.find(x=>x.start<=n.start+.01&&x.end>n.start+.01);
 const id=row.id==='S06'?['S06a','S06b','S06c','S06d'][i-5]:row.id;
 let file,kind='video',inTick=0,speed=1,xf;
 if(row.decision==='generate')file=path.join(R,'motion',id+'.mp4');
 else if(row.decision==='graphic'){file=path.join(R,'keyframes',id+'.png');kind='image';}
 else if(row.decision==='library')file=path.join(P,'output/omni',id+'.mp4');
 else {file=resolveNative(n.source);inTick=toTicks(s.source_timerange.start);speed=s.speed;xf=transform(s);}
 const duration=toTicks(s.target_timerange.duration),assetId=addAsset(file,kind,'picture-'+id);
 const clip={id:'shot-'+id,kind,assetId,name:id+' — '+row.visual,start:toTicks(s.target_timerange.start),duration,in:inTick,out:kind==='image'?duration:inTick+Math.round(duration*speed),speed};
 if(xf)clip.transform=xf;
 ops.push(op('addClip',{trackId:'picture',clip}));
 sourceNotes.push({id,native_segment:s.id,decision:row.decision,source:file,original:n.source,original_source_range:s.source_timerange,original_transform:s.clip,original_material_refs:s.extra_material_refs,graphic_source:row.decision==='graphic'?row.source:null});
}
const audioMap=new Map(native.materials.audios.map(a=>[a.id,a]));const fadeMap=new Map((native.materials.audio_fades??[]).map(a=>[a.id,a]));
const audioTracks=native.tracks.filter(t=>t.type==='audio');
for(let ti=0;ti<audioTracks.length;ti++){
 const tid=ti===0?'narration':'music';ops.push(op('addTrack',{track:{id:tid,kind:'audio',name:ti===0?'Approved 1.1x narration — R2 source edits':'Approved music'}}));
 for(let i=0;i<audioTracks[ti].segments.length;i++){
  const s=audioTracks[ti].segments[i],a=audioMap.get(s.material_id),file=resolveNative(a.path),assetId=addAsset(file,'audio','audio-'+tid);
  const fade=(s.extra_material_refs??[]).map(id=>fadeMap.get(id)).find(Boolean);
  ops.push(op('addClip',{trackId:tid,clip:{id:tid+'-'+i,kind:'audio',assetId,start:toTicks(s.target_timerange.start),duration:toTicks(s.target_timerange.duration),in:toTicks(s.source_timerange.start),out:toTicks(s.source_timerange.start+s.source_timerange.duration),speed:s.speed,audio:{gain:20*Math.log10(s.volume),fadeIn:toTicks(fade?.fade_in_duration??0),fadeOut:toTicks(fade?.fade_out_duration??0)}}}));
 }
}
const textMap=new Map(native.materials.texts.map(t=>[t.id,t]));const textTracks=native.tracks.filter(t=>t.type==='text');
for(let ti=0;ti<textTracks.length;ti++){
 const track=textTracks[ti];
 if(track.segments.length===95){
  // Line-mode canonical captions retain exact R2 text and exposure windows.
  const captions=track.segments.map((s,i)=>{const m=textMap.get(s.material_id),text=JSON.parse(m.content).text,duration=toTicks(s.target_timerange.duration);return {id:'caption-'+i,start:toTicks(s.target_timerange.start),duration,words:[{text,start:0,duration}]};});
  ops.push(op('addCaptionTrack',{track:{id:'captions',name:'95 approved R2 phrases',style:{font:'Inter',size:60,weight:800,color:'#111111',mode:'line',uppercase:false,background:{color:'#ffffff',padding:14,radius:12}},placement:{anchor:'custom',x:.5,y:.66,safeZone:true,scrimAware:false},captions}}));
 }else{
  const tid='callouts-'+ti;ops.push(op('addTrack',{track:{id:tid,kind:'text',name:'Approved callouts / CTA'}}));
  for(let i=0;i<track.segments.length;i++){
   const s=track.segments[i],m=textMap.get(s.material_id),text=JSON.parse(m.content).text;
   const style={content:text,font:'Inter',size:m.font_size*1920/360,weight:800,italic:false,color:m.text_color,align:'center',lineHeight:1.1,letterSpacing:0,uppercase:false};
   if(m.background_alpha>0)style.background={color:m.background_color,padding:16,radius:12};
   ops.push(op('addClip',{trackId:tid,clip:{id:tid+'-'+i,kind:'text',start:toTicks(s.target_timerange.start),duration:toTicks(s.target_timerange.duration),text:style,transform:transform(s)}}));
  }
 }
}
const projectInit={id:'MOT-VID-013-HOOK-A-R3',name:'MOT-VID-013 Hook A — revised visuals / 1.1x',width:1080,height:1920,fps:30,assets,meta:{editingAuthorized:true,sourceProject:nativePath,editingPlan:path.join(R,'editing-plan.md'),status:'Editable internal document; playback/export QA pending',narrationSpeed:1.1,celeryFirstFrame:1387,graphicSource:path.join(R,'graphics/S19-three-things.svg'),textPresentationImport:'Provisional internal font-size translation; compare against approved R2 export before final render.',transitions:'Straight cuts per R3 plan. Native transition metadata preserved separately; not silently emulated.',editorEntry:kitPath}};
let project=createProject(projectInit);const base=structuredClone(project);let log=createLog(base);
ops.push(op('addMarker',{marker:{id:'approval-edit',at:0,kind:'approval',author,body:'User explicitly approved editing the revised concept.'}}));
ops.push(op('addMarker',{marker:{id:'render-pending',at:0,kind:'review',author,body:'Playback/export interface still required. Validate text presentation, caption safe zones, audio joins and all cut boundaries before delivery.'}}));
({project,log}=append(log,project,op('batch',{ops})));
const check=validateProject(project);assert.equal(check.ok,true,JSON.stringify(check));
assert.equal(project.duration,seconds(95.9));
const pic=project.tracks.find(t=>t.id==='picture');assert.equal(pic.clips.length,40);
for(let i=1;i<pic.clips.length;i++)assert.equal(pic.clips[i].start,pic.clips[i-1].start+pic.clips[i-1].duration);
const vo=project.tracks.find(t=>t.id==='narration');assert.equal(vo.clips.length,32);assert(vo.clips.every(c=>c.speed===1.1));
for(let i=0;i<vo.clips.length;i++){const s=audioTracks[0].segments[i],c=vo.clips[i];assert.equal(c.start,toTicks(s.target_timerange.start));assert.equal(c.in,toTicks(s.source_timerange.start));assert.equal(c.out,toTicks(s.source_timerange.start+s.source_timerange.duration));assert.equal(c.duration,toTicks(s.target_timerange.duration));}
assert.equal(project.captions[0].captions.length,95);
assert.equal(pic.clips.find(c=>c.id==='shot-S20').start,1387*200);
assert.equal(pic.clips.find(c=>c.id==='shot-S19').kind,'image');
const write=(name,obj)=>fs.writeFileSync(path.join(out,name),JSON.stringify(obj,null,2));
write('MOT-VID-013-HOOK-A-R3.timeline.json',project);write('event-log.json',{base,log});write('source-mapping.json',sourceNotes);write('validation.json',{...check,pictureClips:40,voiceSegments:32,captionPhrases:95,durationSeconds:95.9,voiceSpeed:1.1,sourceTimeRangesPreserved:true,celeryFirstFrame:1387,rendered:false});
console.log(JSON.stringify({project:path.join(out,'MOT-VID-013-HOOK-A-R3.timeline.json'),valid:check.ok,pictureClips:40,voiceSegments:32,captionPhrases:95,durationSeconds:95.9,rendered:false}));
