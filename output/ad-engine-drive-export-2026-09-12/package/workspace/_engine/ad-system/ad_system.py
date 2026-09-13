#!/usr/bin/env python3
"""Agent-friendly commands. JSON input comes from files, not escaped shell strings."""
import argparse
import json
from pathlib import Path
from store import Store, blank_record, Invalid
from workflow import qa, queue_task, update_task, compare, transition
from performance import import_csv, analyze, save_decision, next_iteration, operations
from inventory import sync_brand
from obsidian_memory import sync as memory_sync, context, search as memory_search, remember, MarkdownStore

p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db');s=p.add_subparsers(dest='cmd',required=True)
s.add_parser('memory-sync')
x=s.add_parser('context');x.add_argument('id')
x=s.add_parser('memory-search');x.add_argument('query');x.add_argument('--brand')
x=s.add_parser('remember');x.add_argument('id');x.add_argument('file');x.add_argument('--source',required=True);x.add_argument('--kind',default='observation')
x=s.add_parser('stage');x.add_argument('id');x.add_argument('stage');x.add_argument('--revision',type=int,required=True)
x=s.add_parser('sync');x.add_argument('--brand',default='motilli')
x=s.add_parser('list');x.add_argument('--brand')
x=s.add_parser('show');x.add_argument('id');x.add_argument('--revision',type=int)
x=s.add_parser('new');x.add_argument('--brand',default='motilli');x.add_argument('--title',required=True)
x=s.add_parser('save');x.add_argument('file');x.add_argument('--reason',default='Agent saved creative');x.add_argument('--unlock-reason',default='')
x=s.add_parser('qa');x.add_argument('id');x.add_argument('--scope',default='delivery')
x=s.add_parser('queue');x.add_argument('id');x.add_argument('kind');x.add_argument('--after',action='append',default=[])
x=s.add_parser('task');x.add_argument('file',help='JSON containing task_id, action, owner, optional handle/receipt')
x=s.add_parser('export');x.add_argument('id');x.add_argument('path');x.add_argument('--revision',type=int,required=True);x.add_argument('--hook',default='')
x=s.add_parser('bind');x.add_argument('--platform',default='meta');x.add_argument('--account',required=True);x.add_argument('--ad',required=True);x.add_argument('--export',required=True)
x=s.add_parser('import');x.add_argument('csv');x.add_argument('--settings',required=True)
s.add_parser('results');s.add_parser('operations')
x=s.add_parser('decision');x.add_argument('id');x.add_argument('file')
x=s.add_parser('iterate');x.add_argument('decision');x.add_argument('--title',required=True)
x=s.add_parser('compare');x.add_argument('ids',nargs='+')
x=s.add_parser('review');x.add_argument('id');x.add_argument('file');x.add_argument('--revision',required=True,type=int)
a=p.parse_args();db_path=Path(a.db) if a.db else Path(__file__).resolve().parent/'data/system.sqlite3'
st=MarkdownStore(db_path) if a.cmd in {'context','memory-search','remember','memory-sync'} and not db_path.exists() else Store(a.db)
def read(path):return json.loads(Path(path).read_text())
try:
    if a.cmd=='memory-sync':out=memory_sync(st)
    elif a.cmd=='context':out=context(st,a.id)
    elif a.cmd=='memory-search':out=memory_search(st,a.query,a.brand)
    elif a.cmd=='remember':out=remember(st,a.id,Path(a.file).read_text(),a.source,a.kind)
    elif a.cmd=='sync':out=sync_brand(st,a.brand)
    elif a.cmd=='stage':out=transition(st,a.id,a.stage,a.revision)
    elif a.cmd=='list':out=[dict(id=r['id'],title=r['title'],brand=r['brand'],revision=r['revision'],stage=r['stage']) for r in st.list(a.brand)]
    elif a.cmd=='show':out=st.get(a.id,a.revision)
    elif a.cmd=='new':out=st.save(blank_record(a.brand,a.title),0)
    elif a.cmd=='save':r=read(a.file);out=st.save(r,r['revision'],a.reason,a.unlock_reason)
    elif a.cmd=='qa':r=st.get(a.id);out=qa(st,r,a.scope);out['review_id']=st.add_review(r['id'],'automated',out,r['revision'])
    elif a.cmd=='queue':out=queue_task(st,a.id,a.kind,a.after)
    elif a.cmd=='task':j=read(a.file);out=update_task(st,j['task_id'],j['action'],j.get('owner',''),j.get('handle'),j.get('receipt'))
    elif a.cmd=='export':out=st.register_export(a.id,a.path,a.revision,a.hook)
    elif a.cmd=='bind':st.bind(a.platform,a.account,a.ad,a.export);out={'bound':True}
    elif a.cmd=='import':out=import_csv(st,Path(a.csv).read_text(),read(a.settings))
    elif a.cmd=='results':out=analyze(st)
    elif a.cmd=='operations':out=operations(st)
    elif a.cmd=='decision':out=save_decision(st,a.id,read(a.file))
    elif a.cmd=='iterate':out=next_iteration(st,a.decision,a.title)
    elif a.cmd=='compare':out=compare([st.get(x) for x in a.ids])
    elif a.cmd=='review':out={'review_id':st.add_review(a.id,'human',read(a.file),a.revision)}
    print(json.dumps(out,indent=2,ensure_ascii=False,allow_nan=False))
except (Invalid,ValueError) as e:p.exit(1,str(e)+'\n')
