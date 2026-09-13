import importlib.util,pathlib,json,concurrent.futures,sys
ROOT=pathlib.Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[3]
s=importlib.util.spec_from_file_location('tt',WORKSPACE/'_engine/research/nuora-trendtrack-2026-09-07/fetch_transcripts.py');tt=importlib.util.module_from_spec(s);s.loader.exec_module(tt);tt.ROOT=ROOT

def run(j):
 name,args,label=j
 (ROOT/'raw'/f'{label}-request.json').write_text(json.dumps({'name':name,'arguments':args},indent=2))
 try:
  d,h=tt.call(name,args,label);data=d['result'].get('structuredContent',{});print(label,json.dumps(data,ensure_ascii=False)[:900],flush=True)
 except Exception as e:print(label,str(e),flush=True)
if __name__=='__main__':
 jobs=json.loads(pathlib.Path(sys.argv[1]).read_text())
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(run,jobs))
