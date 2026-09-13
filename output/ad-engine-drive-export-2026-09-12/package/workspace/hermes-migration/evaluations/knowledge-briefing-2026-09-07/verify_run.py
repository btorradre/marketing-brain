"""Read the Hermes audit trace and saved workflow note; no model reasoning export."""
from pathlib import Path
import json
import subprocess

REMOTE_CODE = r'''
from pathlib import Path
import sqlite3,json
c=sqlite3.connect('file:/root/.hermes-paperclip/state.db?mode=ro',uri=True)
s=c.execute("SELECT session_id FROM messages WHERE role='user' AND content LIKE 'Load and use the AI UGC/VSL copywriting knowledge base Codex installed%' ORDER BY timestamp DESC LIMIT 1").fetchone()
assert s, 'Briefing session missing'
model=c.execute('SELECT model FROM sessions WHERE id=?',s).fetchone()[0]
calls=[]
for row in c.execute('SELECT tool_calls FROM messages WHERE session_id=? AND tool_calls IS NOT NULL ORDER BY id',s):
 for call in json.loads(row[0]):
  f=call.get('function',{}); args=f.get('arguments','{}')
  calls.append({'tool':f.get('name'),'arguments':json.loads(args) if isinstance(args,str) else args})
memory_results=[r[0] for r in c.execute("SELECT content FROM messages WHERE session_id=? AND role='tool' AND tool_name='memory' ORDER BY id",s)]
p=Path('/root/.hermes-paperclip/memories/MEMORY.md')
memory=p.read_text() if p.exists() else ''
print(json.dumps({'session':s[0],'model':model,'toolCallCount':len(calls),'calls':calls,'memoryResults':memory_results,'memoryPath':str(p),'savedCopywritingEntries':[e for e in memory.split('\n\u00a7\n') if 'ai-ugc-vsl-swipe-copywriting' in e or 'HERMES-KNOWLEDGE-INDEX' in e]},indent=2))
'''

result = subprocess.run(
    ['ssh', '-S', 'none', '-o', 'BatchMode=yes', 'root@187.124.249.12', 'python3 -'],
    input=REMOTE_CODE, text=True, capture_output=True, check=True,
)
data = json.loads(result.stdout)
(Path(__file__).parent / 'tool-trace.json').write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps({k: v for k, v in data.items() if k != 'calls'}, indent=2))
