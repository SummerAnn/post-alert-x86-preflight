#!/usr/bin/env python3
"""Plan/run independent repair generations without overwriting artifacts."""
import argparse, json, subprocess, sys
from pathlib import Path

JOBS = {
  'remote-config': {
    'gpt-6.1-sol': ('pilot_config_validator_repair.py', '/tmp/config_validator_secret_clean'),
    'claude-sonnet-4-6': ('pilot_config_validator_repair_anthropic.py', '/tmp/config_validator_secret'),
  },
  'compliance-disclosure': {
    'gpt-6.1-sol': ('pilot_config_validator_repair.py', '/tmp/config_validator_reconstructed'),
    'claude-sonnet-4-6': ('pilot_compliance_patch_anthropic.py', '/tmp/config_validator_reconstructed'),
  },
  'merchant-enrichment': {
    'gpt-6.1-sol': ('pilot_expense_enrichment_repair.py', '/tmp/controlarena-artifacts/expense_HEAD'),
    'claude-sonnet-4-6': ('pilot_expense_patch_anthropic.py', '/tmp/controlarena-artifacts/expense_HEAD'),
  },
}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out-root',type=Path,required=True); ap.add_argument('--dry-run',action='store_true'); a=ap.parse_args()
    plan=[]
    for mech,models in JOBS.items():
        for model,(script,source) in models.items():
            for rep in range(3):
                out=a.out_root/mech/model/f'repair_{rep}'
                plan.append({'mechanism':mech,'model':model,'repair_rep':rep,'script':script,'source':source,'out':str(out)})
    missing=[j for j in plan if not Path(j['source']).is_dir()]
    if missing: raise SystemExit('missing source workspaces: '+', '.join(j['source'] for j in missing))
    if a.dry_run: print(json.dumps({'jobs':len(plan),'plan':plan},indent=2)); return
    for j in plan:
        out=Path(j['out'])
        if out.exists() and any(out.iterdir()): raise SystemExit(f'refusing to overwrite {out}')
        out.parent.mkdir(parents=True,exist_ok=True)
        cmd=[sys.executable,str(Path(__file__).with_name(j['script'])),'--workspace',j['source'],'--out',str(out)]
        if j['model'].startswith('gpt'): cmd += ['--model',j['model']]
        subprocess.run(cmd,check=True)
    print(json.dumps({'jobs_completed':len(plan)}))

if __name__=='__main__': main()
