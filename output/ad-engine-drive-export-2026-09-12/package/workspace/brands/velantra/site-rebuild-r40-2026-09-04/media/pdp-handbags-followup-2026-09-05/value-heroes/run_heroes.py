"""Existing Kie engine orchestration, preserving prompts, receipts and provider files."""
import argparse, hashlib, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[5]
sys.path.insert(0, str(REPO / '_engine/mcp/ad-engine'))
import db
from engines import kie

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['submit','poll'])
    parser.add_argument('--families', nargs='*')
    args = parser.parse_args()
    path = ROOT / 'prompts-and-provenance.json'
    manifest = json.loads(path.read_text()); db.init_db()
    def save(): path.write_text(json.dumps(manifest,indent=2)+'\n')
    for row in manifest['panels']:
        if args.families and row['family'] not in args.families: continue
        if args.action == 'submit':
            if row['status'] != 'planned': continue
            balance = kie.balance()
            if balance is None or balance < 100: raise RuntimeError(f'Insufficient confirmed credits: {balance}')
            row['credits_before_submission'] = balance
            crop = row['source_crop']
            if not crop.get('uploaded_url'):
                crop['uploaded_url'] = kie.upload(crop['path'], upload_path='velantra-pdp-craft-2026-09-05'); save()
            row['submission'] = kie.generate(manifest['model'], {'prompt':row['prompt'],'input_urls':[crop['uploaded_url']], 'aspect_ratio':manifest['aspect_ratio'], 'resolution':manifest['resolution']}, brand='velantra', concept='pdp-handbags-craft-2026-09-05')
            row['status'] = row['submission']['status']; save()
            print(row['id'],row['submission'],flush=True)
        elif row['status'] == 'running':
            result = kie.status(row['submission']['job_id']); row['status'] = result['status']
            (ROOT/'receipts').mkdir(exist_ok=True)
            (ROOT/'receipts'/(row['id']+'.json')).write_text(json.dumps(result,indent=2)+'\n')
            if row['status'] == 'success':
                asset = next(a for a in db.list_assets(job_id=row['submission']['job_id'],limit=10) if a.get('path'))
                outdir=ROOT/'final';outdir.mkdir(exist_ok=True);dest=outdir/(row['id']+'.png')
                if dest.exists(): raise RuntimeError('Refusing output overwrite: '+str(dest))
                shutil.copy2(asset['path'],dest); row['output']=str(dest); row['output_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest();row['provider_asset']=asset
            save();print(row['id'],row['status'],flush=True)

if __name__ == '__main__': main()
