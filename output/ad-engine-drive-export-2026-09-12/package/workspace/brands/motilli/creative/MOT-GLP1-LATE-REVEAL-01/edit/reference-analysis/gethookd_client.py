import pathlib,importlib.util,requests,json,sys
P=pathlib.Path(__file__).resolve().parent
W=P.parents[5]
s=importlib.util.spec_from_file_location('gh',W/'_engine/tools/tools/gethookd_resolver.py');gh=importlib.util.module_from_spec(s);s.loader.exec_module(gh)
def call(tool,args,label):
 req={'tool':tool,'arguments':args};(P/'raw'/f'{label}-request.json').write_text(json.dumps(req,indent=2))
 r=requests.post('https://app.gethookd.ai/api/mcp/v1/call',headers=gh.HEADERS,json=req,timeout=90);print(label,'HTTP',r.status_code,flush=True)
 d=r.json();(P/'raw'/f'{label}.json').write_text(json.dumps(d,indent=2));return d
if __name__=='__main__':
 r=requests.get('https://app.gethookd.ai/api/mcp/v1/tools',headers=gh.HEADERS,timeout=45);print('Manifest HTTP',r.status_code)
 d=r.json();(P/'raw/gethookd-tools.json').write_text(json.dumps(d,indent=2))
 if r.status_code==200:
  for t in d.get('tools',[]):
   if any(x in t['name'] for x in ['search_ads','transcri','get_ad']):print(json.dumps(t))
