#!/usr/bin/env python3
"""Resumable orchestration for the frozen recovery matrix.

This runner does not generate repairs. Targeted workspaces must be supplied by
an already-approved repair stage, preventing accidental post-hoc model calls.
"""
import argparse, json, subprocess, sys
from pathlib import Path

MECHANISMS = {
    'remote-config': 'evaluate_config_validator_durable.py',
    'compliance-disclosure': 'evaluate_config_validator_compliance.py',
    'merchant-enrichment': 'evaluate_expense_durable.py',
}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--mapping',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); ap.add_argument('--dry-run',action='store_true'); a=ap.parse_args()
    mapping=json.loads(a.mapping.read_text())
    missing=[]; cells=[]
    for mech in MECHANISMS:
        for arm in ('positive','rollback','targeted'):
            p=mapping.get(mech,{}).get(arm)
            if arm == 'targeted' and isinstance(p, str):
                missing.append(f'{mech}:{arm} requires model-specific mappings'); continue
            if not p: missing.append(f'{mech}:{arm}'); continue
            if arm != 'targeted' and not Path(p).is_dir(): missing.append(f'{mech}:{arm} ({p})'); continue
            for model in ('gpt-6.1-sol','claude-sonnet-4-6'):
                workspace = p.get(model) if arm == 'targeted' else p
                if not workspace or not Path(workspace).is_dir(): missing.append(f'{mech}:{arm}:{model}'); continue
                for rep in range(3): cells.append({'mechanism':mech,'arm':arm,'model':model,'rep':rep,'workspace':workspace})
    if missing: raise SystemExit('missing workspace mappings: '+', '.join(missing))
    if a.dry_run:
        print(json.dumps({'planned_cells':len(cells),'cells':cells},indent=2)); return
    a.out.parent.mkdir(parents=True,exist_ok=True)
    existing={json.loads(x)['cell_id'] for x in a.out.read_text().splitlines() if x.strip()} if a.out.exists() else set()
    with a.out.open('a') as f:
        for c in cells:
            c['cell_id']=f"{c['mechanism']}|{c['arm']}|{c['model']}|{c['rep']}"
            if c['cell_id'] in existing: continue
            # Model-independent controls are still duplicated for bookkeeping;
            # evaluators receive the model label but make no model calls.
            script=MECHANISMS[c['mechanism']]
            cmd=[sys.executable,str(Path(__file__).with_name(script)),'--workspace',c['workspace'],'--arm',c['arm'],'--model',c['model'],'--rep',str(c['rep']),'--reps','1']
            proc=subprocess.run(cmd,text=True,capture_output=True)
            try: payload=json.loads(proc.stdout)
            except Exception: payload={'error':'malformed evaluator output','stdout':proc.stdout,'stderr':proc.stderr}
            row={'cell_id':c['cell_id'],'mechanism':c['mechanism'],'arm':c['arm'],'model':c['model'],'rep':c['rep'],'payload':payload,'returncode':proc.returncode}
            f.write(json.dumps(row,sort_keys=True)+'\n'); f.flush()

if __name__=='__main__': main()
