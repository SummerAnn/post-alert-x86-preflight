#!/usr/bin/env python3
"""Validate and summarize preregistered durable-recovery result rows."""
import argparse, json
from pathlib import Path
from collections import defaultdict
from jsonschema import validate

SCHEMA = json.loads((Path(__file__).with_name('durable_result_schema.json')).read_text())

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('jsonl',type=Path); args=ap.parse_args()
    rows=[]; invalid=[]
    for i,line in enumerate(args.jsonl.read_text().splitlines(),1):
        if not line.strip(): continue
        try:
            row=json.loads(line); validate(row,SCHEMA); rows.append(row)
        except Exception as e: invalid.append({'line':i,'error':str(e)})
    groups=defaultdict(list)
    for r in rows:
        if r['valid']: groups[(r['artifact'],r['model'],r['arm'])].append(r)
    summary=[]
    for (artifact,model,arm),rs in sorted(groups.items()):
        summary.append({'artifact':artifact,'model':model,'arm':arm,'n':len(rs),'active_rate':sum(r['active'] for r in rs)/len(rs),'durable_rate':sum(r['durable'] for r in rs)/len(rs),'legitimate_rate':sum(r['legitimate'] for r in rs)/len(rs),'collateral_rate':sum(r['collateral'] for r in rs)/len(rs)})
    print(json.dumps({'rows':len(rows),'invalid_rows':invalid,'summary':summary},indent=2,sort_keys=True))
    if invalid: raise SystemExit(2)

if __name__=='__main__': main()
