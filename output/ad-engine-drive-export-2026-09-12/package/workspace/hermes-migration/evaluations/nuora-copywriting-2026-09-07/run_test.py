from pathlib import Path
import subprocess,os,json,time
staging=Path('/root/hermes-nuora-staging-20260907')
started=time.time()
env=os.environ.copy();env['HERMES_HOME']='/root/.hermes-paperclip';env['PYTHONUNBUFFERED']='1'
cmd=['/root/.hermes/hermes-agent/venv/bin/python','/root/.hermes/hermes-agent/cli.py','--query',(staging/'test-brief.txt').read_text(),'--toolsets','skills,terminal','--max_turns','12','--quiet']
with (staging/'test-output.txt').open('w') as out,(staging/'test-stderr.txt').open('w') as err:
 try:
  result=subprocess.run(cmd,env=env,cwd='/opt/vault/marketing-brain',stdout=out,stderr=err,timeout=420)
  summary={'exitCode':result.returncode,'seconds':round(time.time()-started,1)}
 except subprocess.TimeoutExpired:
  summary={'exitCode':None,'timedOut':True,'seconds':round(time.time()-started,1)}
(staging/'test-status.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
