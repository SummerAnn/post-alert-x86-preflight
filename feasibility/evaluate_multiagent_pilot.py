#!/usr/bin/env python3
"""Evaluate completed pilot repair artifacts in fresh processes."""
import argparse, json, subprocess, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args(); rows=[]
    for p in sorted(a.root.glob('pilot-remote-config-*')):
        meta=p/'_multiagent_meta.json'
        if not meta.exists() or p.name.endswith('_partial') or p.name.endswith('_failed_parser'): continue
        m=json.loads(meta.read_text()); proc=subprocess.run([sys.executable,'feasibility/evaluate_config_validator_durable.py','--workspace',str(p),'--arm','targeted','--model',m['sequence'][0].split(':')[0],'--rep','0','--reps','3'],capture_output=True,text=True)
        try: payload=json.loads(proc.stdout)
        except Exception: payload={'valid':False,'void_reason':'malformed evaluator output','stdout':proc.stdout,'stderr':proc.stderr}
        rows.append({'episode_id':p.name,'arm':m['arm'],'sequence':m['sequence'],'payload':payload,'returncode':proc.returncode})
    a.out.write_text(json.dumps(rows,indent=2,sort_keys=True)); print(json.dumps({'episodes':len(rows),'out':str(a.out)}))
if __name__=='__main__': main()
