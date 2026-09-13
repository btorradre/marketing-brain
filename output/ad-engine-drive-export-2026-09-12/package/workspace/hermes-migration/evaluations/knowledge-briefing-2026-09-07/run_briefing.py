from pathlib import Path
import subprocess, os, json, time

staging = Path('/root/hermes-nuora-staging-20260907/knowledge-briefing')
env = os.environ.copy()
env['HERMES_HOME'] = '/root/.hermes-paperclip'
env['PYTHONUNBUFFERED'] = '1'
started = time.time()
command = [
    '/root/.hermes/hermes-agent/venv/bin/python',
    '/root/.hermes/hermes-agent/cli.py',
    '--query', (staging / 'brief.txt').read_text(),
    '--toolsets', 'skills,terminal,memory', '--max_turns', '36', '--quiet',
]
with (staging / 'output.md').open('w') as out, (staging / 'stderr.txt').open('w') as err:
    try:
        result = subprocess.run(command, env=env, cwd='/opt/vault/marketing-brain', stdout=out, stderr=err, timeout=600)
        status = {'exitCode': result.returncode, 'seconds': round(time.time() - started, 1)}
    except subprocess.TimeoutExpired:
        status = {'exitCode': None, 'timedOut': True, 'seconds': round(time.time() - started, 1)}
(staging / 'status.json').write_text(json.dumps(status, indent=2) + '\n')
print(json.dumps(status))
