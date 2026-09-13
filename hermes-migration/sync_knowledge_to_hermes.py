#!/usr/bin/env python3
"""Sync documented local knowledge, with file-level backups and no deletions."""
import argparse,datetime,hashlib,json,os,pathlib,subprocess
BASE=pathlib.Path(__file__).resolve().parents[1]
SERVER='root@187.124.249.12'
DEST='/opt/vault/marketing-brain/'
EXTS={'.md','.txt','.rtf','.pdf','.doc','.docx','.csv','.tsv','.xlsx','.xls','.json','.jsonl','.yaml','.yml','.py','.sh','.html','.htm','.srt','.vtt','.epub','.odt','.pptx','.ppt'}
SKIP={'.git','node_modules','__pycache__','venv','.venv','auth','logs','cache','oauth credentials'}
BAD=['credential','secret','hyperframes','remotion','cookie','oauth']

def eligible(p):
 return not(p.is_symlink() or not p.is_file() or p.name.startswith('.') or p.suffix.lower() not in EXTS or any(x.lower() in SKIP or any(s in x.lower() for s in BAD) for x in p.relative_to(BASE).parts))

def main():
 a=argparse.ArgumentParser();a.add_argument('--apply',action='store_true');args=a.parse_args()
 files=[]
 for name in ['_engine','brands','resources','swipe-intake']:
  files.extend(p for p in (BASE/name).rglob('*') if eligible(p))
 files.extend(p for p in BASE.glob('*.md') if eligible(p))
 files=sorted(set(files))
 out=BASE/'hermes-migration/knowledge-sync-2026-09-07';out.mkdir(exist_ok=True)
 manifest=[{'path':str(p.relative_to(BASE)),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (out/'files.nul').write_bytes(b'\0'.join(str(p.relative_to(BASE)).encode() for p in files)+b'\0')
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 backup='/root/hermes-migration-backups/knowledge-sync-'+stamp
 cmd=['rsync','-az','--checksum','--from0','--files-from='+str(out/'files.nul'),'--itemize-changes','--stats','-e','ssh -S none -o BatchMode=yes -o ConnectTimeout=15']
 if args.apply:cmd+=['--backup','--backup-dir='+backup]
 else:cmd+=['--dry-run']
 cmd += [str(BASE)+'/',SERVER+':'+DEST]
 print(json.dumps({'files':len(files),'bytes':sum(x['size'] for x in manifest),'mode':'apply' if args.apply else 'dry-run','backup':backup if args.apply else None}),flush=True)
 log=out/('applied.log' if args.apply else 'dry-run.log')
 with log.open('w') as f:subprocess.run(cmd,stdout=f,check=True)
 summary={'files':len(files),'bytes':sum(x['size'] for x in manifest),'applied':args.apply,'server':SERVER,'destination':DEST,'backup':backup if args.apply else None,'scope':'_engine, brands, resources, swipe-intake and root Markdown; documented text/data and PDF/Office references; excludes media binaries, credentials, caches and banned composition tooling; no deletions'}
 (out/('applied.json' if args.apply else 'dry-run.json')).write_text(json.dumps(summary,indent=2)+'\n')
 print(log.read_text(errors='replace')[-1000:])
if __name__=='__main__':main()
