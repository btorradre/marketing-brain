import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../../../..');
const editor=await import(pathToFileURL(path.resolve(root,'../marketing-apps/adengine/packages/timeline/dist/index.js')));
const {createProject,assembleFromBoardDetailed,apply,validateProject,createLog,append,sequentialIds}=editor;
const output=path.join(here,'output/editor');
const read=n=>JSON.parse(fs.readFileSync(path.join(output,n),'utf8'));
const vo=read('vo-alignment.json'),assets=read('asset-catalog.json'),status=read('handoff-status.json');
const author={kind:'agent',id:'codex-mot-vid-013'},now=new Date().toISOString();
for(const variant of status.variants){
 const board=read(variant.id+'-board.json');
 let project=createProject({id:variant.id,name:variant.id+' — motion draft',width:1080,height:1920,fps:30,assets,meta:{status:status.status,sourceBoard:'mot-vid-013-generated-visuals',narrationSpeed:vo.speed}});
 const base=structuredClone(project);
 const ids=sequentialIds();
 const result=assembleFromBoardDetailed(board,vo,{author,at:now,project,laneId:'ours',gapPolicy:'leave',idFactory:ids,captionStyle:{font:'Arial',size:58,weight:800,color:'#111111',mode:'line',uppercase:false,outline:{color:'#ffffff',width:0},background:{color:'#ffffff',padding:18,radius:12}},captionPlacement:{anchor:'custom',x:.5,y:.73,safeZone:true,scrimAware:true},captionChunk:{maxWords:5,maxDuration:15000}});
 const audioAdd=result.op.ops.find(o=>o.type==='addClip'&&o.clip.id===result.voClipId);
 audioAdd.clip.speed=vo.speed;audioAdd.clip.out=Math.round(vo.source_duration*6000);audioAdd.clip.duration=Math.round(vo.duration*6000);
 const options={id:'mot-013-mute-'+variant.id,at:now,author,type:'setTrack',trackId:result.videoTrackId,patch:{muted:true}};
 let log=createLog(base);
 ({project,log}=append(log,project,result.op));
 ({project,log}=append(log,project,options));
 const mk=(type,body)=>({id:ids('edit'),at:now,author,type,...body});
 ({project,log}=append(log,project,mk('addTrack',{track:{id:'labels',kind:'text',name:'Reference-style callouts'}})));
 const cards=board.lanes[0].cards,find=id=>cards.find(c=>c.id===id);
 const hook={A:'Tried all of these?',B:'Still backed up?',C:'Another remedy. Still waiting?'}[variant.id.slice(-1)];
 const labels=[
  {id:'hook',text:hook,start:0,end:find('S03').t,hook:true},
  {id:'colon',text:'COLON',start:find('S07').t,end:find('S08').t_end},
  {id:'stomach',text:'STOMACH',start:find('S09').t,end:find('S09').t_end},
  {id:'map',text:'STOMACH / UPSTREAM\nCOLON / DOWNSTREAM',start:find('S16').t,end:find('S16').t_end},
  {id:'apigenin',text:'APIGENIN\nFROM CELERY',start:find('S20').t,end:find('S20').t_end},
  {id:'chlorophyllin',text:'CHLOROPHYLLIN',start:find('S25').t,end:find('S25').t_end},
  {id:'imagine',text:'IMAGINE YOUR MORNING',start:find('S32').t,end:find('S32').t_end},
  {id:'cta',text:'MOTILLI\n90-DAY MONEY-BACK GUARANTEE\nSHOP MOTILLI',start:find('S37').t,end:find('S37').t_end}
 ];
 for(const label of labels){
  const clip={id:'label-'+label.id,kind:'text',name:label.text,start:Math.round(label.start*6000),duration:Math.round((label.end-label.start)*6000),text:{content:label.text,font:'Arial',size:label.id==='cta'?46:54,weight:800,italic:false,color:label.hook?'#ffffff':'#111111',align:'center',lineHeight:1.15,letterSpacing:0,uppercase:!!label.hook,background:{color:label.hook?'#153d29':'#ffffff',padding:18,radius:12}}};
  ({project,log}=append(log,project,mk('addClip',{trackId:'labels',clip})));
  ({project,log}=append(log,project,mk('setTransform',{clipId:clip.id,transform:{y:-650}})));
 }
 for(const gap of variant.missing){
  const op={id:'missing-'+variant.id+'-'+gap.shot,at:now,author,type:'addMarker',marker:{id:'qa-'+gap.shot,at:Math.round(gap.start*6000),kind:'qa_fail',body:gap.reason,author}};
  ({project,log}=append(log,project,op));
 }
 const check=validateProject(project);
 if(!check.ok)throw new Error(JSON.stringify(check));
 fs.writeFileSync(path.join(output,variant.id+'-timeline.json'),JSON.stringify(project,null,2));
 fs.writeFileSync(path.join(output,variant.id+'-event-log.json'),JSON.stringify({base,log},null,2));
 fs.writeFileSync(path.join(output,variant.id+'-validation.json'),JSON.stringify(check,null,2));
 console.log(JSON.stringify({variant:variant.id,valid:check.ok,videoClips:project.tracks.find(t=>t.kind==='video').clips.length,captions:project.captions[0].captions.length,duration:project.duration/6000,gaps:variant.missing.length}));
}
