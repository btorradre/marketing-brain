#!/usr/bin/env python3
"""Start/status/stop the dedicated local server and make consistent backups."""
import argparse, json, os, signal, socket, sqlite3, subprocess, sys, time, urllib.request, zipfile
from datetime import datetime
from pathlib import Path
HERE=Path(__file__).resolve().parent;DATA=HERE/'data';PID=DATA/'server.json';PORT=8791

def status():
    saved=json.loads(PID.read_text()) if PID.exists() else {}
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:{PORT}/api/health',timeout=2) as response:health=json.load(response)
        process=saved.get('pid')
        if process:
            command=subprocess.check_output(['ps','-p',str(process),'-o','command='],text=True).strip()
            if str(HERE/'server.py') not in command:process=None
        return dict(running=True,url=f'http://127.0.0.1:{PORT}',pid=process,health=health)
    except Exception:return dict(running=False,pid=saved.get('pid'))

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['start','status','stop','backup']);a=p.parse_args();DATA.mkdir(exist_ok=True)
    if a.action=='status':return print(json.dumps(status(),indent=2))
    if a.action=='start':
        s=status()
        if s['running']:return print(json.dumps(s,indent=2))
        with socket.socket() as sock:
            sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            try:sock.bind(('127.0.0.1',PORT))
            except OSError:raise SystemExit('Port is occupied. Existing process preserved.')
        with (DATA/'server.log').open('ab') as log:
            proc=subprocess.Popen([sys.executable,str(HERE/'server.py'),'--port',str(PORT)],cwd=HERE,stdout=log,stderr=log,start_new_session=True)
        PID.write_text(json.dumps(dict(pid=proc.pid,started=datetime.now().isoformat(),port=PORT)))
        for _ in range(25):
            s=status()
            if s['running']:return print(json.dumps(s,indent=2))
            if proc.poll() is not None:raise SystemExit('Server stopped during startup. See data/server.log.')
            time.sleep(.2)
        raise SystemExit('Server has not responded; inspect its current process/log before retrying.')
    if a.action=='stop':
        s=status()
        if not s.get('pid') or not s['running']:return print('No verified owned server to stop.')
        os.kill(s['pid'],signal.SIGTERM)
        for _ in range(20):
            if not status()['running']:break
            time.sleep(.1)
        print('Stopped the verified Ad Studio process.');return
    folder=HERE/'backups';folder.mkdir(exist_ok=True);stamp=datetime.now().strftime('%Y%m%d-%H%M%S');db=folder/(stamp+'.sqlite3')
    with sqlite3.connect(DATA/'system.sqlite3') as source,sqlite3.connect(db) as destination:source.backup(destination)
    out=folder/(stamp+'.zip')
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        z.write(db,'data/system.sqlite3')
        for f in DATA.rglob('*'):
            if f.is_file() and f.name not in {'system.sqlite3','system.sqlite3-wal','system.sqlite3-shm','server.json','server.log'}:z.write(f,str(f.relative_to(HERE)))
    db.unlink();print(str(out))
if __name__=='__main__':main()
