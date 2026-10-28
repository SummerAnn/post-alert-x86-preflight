#!/usr/bin/env python3
"""Resumable bounded runner for the eight-episode multi-agent pilot."""
import argparse, json, subprocess, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--manifest',type=Path,required=True); ap.add_argument('--out-root',type=Path,required=True); ap.add_argument('--artifact',type=Path,required=True); a=ap.parse_args()
    m=json.loads(a.manifest.read_text()); a.out_root.mkdir(parents=True,exist_ok=True); results=[]
    for ep in sorted(m['episodes'], key=lambda x:x['order_index']):
        out=a.out_root/ep['episode_id']
        if out.exists() and (out/'_multiagent_meta.json').exists(): results.append({'episode_id':ep['episode_id'],'status':'existing'}); continue
        cmd=[sys.executable,str(Path(__file__).with_name('run_multiagent_episode.py')),'--artifact',str(a.artifact),'--artifact-id',ep['artifact_id'],'--repair-rep',str(ep['repair_rep']),'--order-index',str(ep['order_index']),'--arm',ep['arm'],'--model',ep['model'],'--out',str(out),'--execute']
        p=subprocess.run(cmd,text=True,capture_output=True)
        row={'episode_id':ep['episode_id'],'status':'complete' if p.returncode==0 else 'failed','returncode':p.returncode,'stdout':p.stdout[-2000:],'stderr':p.stderr[-2000:]}; results.append(row)
        (a.out_root/'pilot_status.json').write_text(json.dumps(results,indent=2))
        if p.returncode != 0: raise SystemExit(json.dumps(row))
    print(json.dumps(results,indent=2))
if __name__=='__main__': main()
