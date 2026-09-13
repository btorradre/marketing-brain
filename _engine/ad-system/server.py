"""Local-only Creative OS UI/API. Shared state also works through the CLI."""
import argparse
import json
import mimetypes
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse, quote
from store import Store, Invalid, Conflict, blank_record, digest, now
from workflow import FORMATS, STAGES, TASKS, qa, compare, queue_task, update_task, task_view, transition
from performance import import_csv, analyze, measurements, save_decision, next_iteration, operations
from inventory import sync_brand, inventory
from obsidian_memory import status as memory_status, context as memory_context, sync as memory_sync, remember as memory_remember

HERE=Path(__file__).resolve().parent

def make_server(store,port=8791):
    token=secrets.token_urlsafe(32)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def allowed_host(self):return self.headers.get('Host','').split(':')[0] in {'localhost','127.0.0.1'}
        def send(self,status,body,ctype='application/json; charset=utf-8'):
            if not isinstance(body,bytes):body=json.dumps(body,ensure_ascii=False,allow_nan=False).encode()
            self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body)
        def do_GET(self):
            if not self.allowed_host():return self.send(403,{'error':'Local host required.'})
            u=urlparse(self.path);q=parse_qs(u.query)
            try:
                if u.path=='/api/health':return self.send(200,dict(service='ad-studio',database=str(store.db.resolve()),memory=memory_status(store)))
                if u.path=='/api/memory':return self.send(200,memory_context(store,q['id'][0]))
                if u.path=='/api/bootstrap':return self.send(200,dict(token=token,memory=memory_status(store),records=store.list(),formats=FORMATS,stages=STAGES,task_kinds=list(TASKS),operations=operations(store),inventory_reports=[json.loads(p.read_text()) for p in (store.db.parent/'inventory').glob('*.json')]))
                if u.path=='/api/record':
                    rid=q['id'][0];r=store.get(rid,int(q['revision'][0]) if q.get('revision') else None);return self.send(200,dict(record=r,history=store.history(rid),reviews=store.related('reviews',rid),exports=store.related('exports',rid),tasks=[task_view(t) for t in store.related('tasks',rid)],decisions=store.related('decisions',rid),qa=qa(store,r,'delivery')))
                if u.path=='/api/inventory':return self.send(200,inventory(store,q.get('brand',[None])[0]))
                if u.path=='/api/results':return self.send(200,dict(imports=store.related('imports'),analysis=analyze(store),measurements=measurements(store),operations=operations(store)))
                if u.path=='/api/compare':return self.send(200,compare([store.get(x) for x in q.get('id',[])]))
                if u.path=='/api/file':return self.serve_file(store.safe_file(q['path'][0]))
                paths={'/':'index.html','/app.js':'app.js','/style.css':'style.css'}
                if u.path in paths:
                    p=HERE/'static'/paths[u.path];return self.send(200,p.read_bytes(),{'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8'}[p.suffix])
                return self.send(404,{'error':'Not found.'})
            except (Invalid,KeyError,ValueError) as e:return self.send(400,{'error':str(e)})
        def serve_file(self,p):
            size=p.stat().st_size;start=0;end=size-1;status=200
            if self.headers.get('Range'):
                try:
                    spec=self.headers['Range'].removeprefix('bytes=');a,b=spec.split('-')
                    if not a:start=max(0,size-int(b))
                    else:start=int(a);end=min(end,int(b)) if b else end
                    if start<0 or start>=size or end<start:raise ValueError()
                    status=206
                except ValueError:return self.send(416,{'error':'Invalid byte range.'})
            ctype=mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
            if p.suffix in {'.md','.txt','.csv'}:ctype='text/plain; charset=utf-8'
            self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Accept-Ranges','bytes');self.send_header('Content-Length',str(end-start+1));self.send_header('X-Content-Type-Options','nosniff')
            if p.suffix=='.html':self.send_header('Content-Disposition',"attachment; filename*=UTF-8''"+quote(p.name))
            if status==206:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
            self.end_headers()
            with p.open('rb') as f:
                f.seek(start);left=end-start+1
                while left>0:
                    chunk=f.read(min(1024*256,left))
                    if not chunk:break
                    self.wfile.write(chunk);left-=len(chunk)
        def do_POST(self):
            origin=self.headers.get('Origin')
            if not self.allowed_host() or self.headers.get('X-Creative-Token')!=token or (origin and urlparse(origin).netloc!=self.headers.get('Host')):return self.send(403,{'error':'Open the local app to make this change.'})
            try:
                length=int(self.headers.get('Content-Length',0))
                if length>12*1024*1024:raise Invalid('Request exceeds 12 MB.')
                a=json.loads(self.rfile.read(length));action=a.get('action')
                if action=='remember':out=memory_remember(store,a['id'],a['text'],a['source'],a.get('kind','observation'))
                elif action=='memory-sync':out=memory_sync(store)
                elif action=='create':out=store.save(blank_record(a.get('brand','motilli'),a['title']),0)
                elif action=='save':
                    old=store.get(a['record']['id'])
                    if old['stage']!=a['record']['stage']:raise Invalid('Use the stage action so readiness checks run.')
                    out=store.save(a['record'],a['expected_revision'],a.get('reason','Edited in Creative OS'),a.get('unlock_reason',''))
                elif action=='stage':out=transition(store,a['id'],a['stage'],a['expected_revision'])
                elif action=='lock':
                    r=store.get(a['id']);r['narration_lock']=dict(hash=digest(r['script']),reason=a.get('reason','User locked the selected narration'),at=now());out=store.save(r,a['expected_revision'],'Narration locked')
                elif action=='qa':
                    r=store.get(a['id']);out=qa(store,r,a.get('scope','delivery'));out['review_id']=store.add_review(r['id'],'automated',out,r['revision'])
                elif action=='human-review':out={'review_id':store.add_review(a['id'],'human',a['review'],a['revision'])}
                elif action=='queue':out=queue_task(store,a['id'],a['kind'],a.get('depends_on'))
                elif action=='task':out=update_task(store,a['task_id'],a['operation'],a.get('owner',''),a.get('handle'),a.get('receipt'))
                elif action=='export':out=store.register_export(a['id'],a['path'],int(a['revision']),a.get('hook_id',''),a.get('notes',''))
                elif action=='bind':store.bind(a['platform'],a['account_id'],a['ad_id'],a['export_id']);out={'bound':True}
                elif action=='import':out=import_csv(store,a['csv'],a['settings'])
                elif action=='decision':out=save_decision(store,a['id'],a['decision'])
                elif action=='iterate':out=next_iteration(store,a['decision_id'],a['title'])
                elif action=='sync':out=sync_brand(store,a.get('brand','motilli'))
                else:raise Invalid('Unknown action.')
                self.send(200,out)
            except Conflict as e:self.send(409,{'error':str(e)})
            except (Invalid,ValueError,KeyError,TypeError) as e:self.send(400,{'error':str(e)})
            except Exception as e:
                import traceback;traceback.print_exc();self.send(500,{'error':'Operation failed; changes were not confirmed. See the local server log.'})
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8791);p.add_argument('--db');a=p.parse_args();store=Store(a.db);store.refresh_memory();server=make_server(store,a.port);print(f'Creative OS: http://127.0.0.1:{server.server_port}',flush=True);server.serve_forever()
