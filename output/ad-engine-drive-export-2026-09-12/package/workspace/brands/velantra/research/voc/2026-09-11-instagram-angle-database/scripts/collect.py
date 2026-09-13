import requests,json,re,sys,time,shutil
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[4]
TOKEN=next(x.split('=',1)[1].strip().strip('\"\'') for x in (REPO/'.env').read_text().splitlines() if x.startswith('APIFY_API_TOKEN='))
HEAD={'Authorization':'Bearer '+TOKEN}
def api(path,method='GET',payload=None,params=None):
 r=requests.request(method,'https://api.apify.com/v2/'+path,headers=HEAD,json=payload,params=params,timeout=60)
 if not r.ok:raise RuntimeError(str(r.status_code)+' '+r.text[:350])
 return r.json()
def start(name,actor,inp,cap):
 p=ROOT/'raw'/f'{name}-run.json'
 if p.exists():return json.loads(p.read_text())
 (ROOT/'raw'/f'{name}-input.json').write_text(json.dumps(inp,indent=2))
 d=api('acts/'+actor+'/runs','POST',inp,{'timeout':1800,'maxTotalChargeUsd':cap})['data']
 p.write_text(json.dumps(d,indent=2));print(name,d['id'],d['status'],flush=True);return d

def poll():
 for p in sorted((ROOT/'raw').glob('*-run.json')):
  name=p.name[:-9];d=json.loads(p.read_text())
  if d['status'] not in ['SUCCEEDED','FAILED','ABORTED','TIMED-OUT']:
   d=api('actor-runs/'+d['id'])['data'];p.write_text(json.dumps(d,indent=2))
  out=ROOT/'raw'/f'{name}-items.json'
  if d['status'] in ['SUCCEEDED','FAILED','ABORTED','TIMED-OUT'] and not out.exists():
   rows=api('datasets/'+d['defaultDatasetId']+'/items',params={'clean':'true','format':'json'});out.write_text(json.dumps(rows,ensure_ascii=False,indent=2))
  n=len(json.loads(out.read_text())) if out.exists() else '?'
  print(name,d['status'],n,'USD',d.get('usageTotalUsd'),flush=True)

def seed():
 src=Path('/Users/brooksorradre2/.codex/attachments/55166195-0f60-41ab-8d94-e75e7eecbf83/pasted-text.txt');shutil.copy(src,ROOT/'seed-notes-original.txt')
 txt=src.read_text();matches=list(re.finditer(r'https?://[^\s]+',txt));entries={}
 for i,m in enumerate(matches):
  u=m.group().split('?')[0].rstrip('/')+'/';notes=txt[m.end():matches[i+1].start() if i+1<len(matches) else len(txt)].strip()
  key=re.sub('https://instagram.com','https://www.instagram.com',u)
  if key in entries:entries[key]['notes']+='\n'+notes;entries[key]['occurrences']+=1
  else:entries[key]={'seed_id':f'S{len(entries)+1:03}','url':key,'notes':notes,'occurrences':1,'platform':'instagram' if 'instagram.com' in u else 'tiktok' if 'tiktok.com' in u else 'other'}
 seeds=list(entries.values());(ROOT/'seeds.json').write_text(json.dumps(seeds,ensure_ascii=False,indent=2));print('Seeds',len(seeds),'IG',sum(x['platform']=='instagram' for x in seeds))
 ig=[x['url'] for x in seeds if x['platform']=='instagram'];tt=[x['url'] for x in seeds if x['platform']=='tiktok']
 start('01-ig-seeds','apify~instagram-scraper',{'directUrls':ig,'resultsType':'posts','resultsLimit':1,'addParentData':True},3)
 start('02-ig-seed-comments','apify~instagram-comment-scraper',{'directUrls':ig,'resultsLimit':100,'includeNestedComments':False},40)
 start('03-tiktok-seed','clockworks~tiktok-scraper',{'postURLs':tt,'resultsPerPage':1,'downloadSubtitlesOptions':'DOWNLOAD_SUBTITLES'},1)
 start('04-tiktok-seed-comments','clockworks~tiktok-comments-scraper',{'postURLs':tt,'commentsPerPost':200,'maxRepliesPerComment':0},1)
if __name__=='__main__':
 if sys.argv[1]=='seed':seed()
 elif sys.argv[1]=='poll':poll()
