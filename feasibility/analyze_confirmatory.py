#!/usr/bin/env python3
"""Aggregate completed confirmatory rows without imputing missing cells."""
import argparse, json
from collections import defaultdict
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('jsonl',type=Path); a=ap.parse_args(); rows=[]; seen=set(); malformed=[]
    for i,line in enumerate(a.jsonl.read_text().splitlines(),1):
        if not line.strip(): continue
        try:
            r=json.loads(line); cid=r['cell_id']
            if cid in seen: malformed.append({'line':i,'error':'duplicate cell'}); continue
            seen.add(cid); rows.append(r)
        except Exception as e: malformed.append({'line':i,'error':str(e)})
    expected=54; groups=defaultdict(list)
    for r in rows: groups[(r['mechanism'],r['arm'],r['model'])].append(r)
    print(json.dumps({'completed_rows':len(rows),'missing_rows':expected-len(rows),'malformed':malformed,'groups':{('|'.join(k)):{'n':len(v)} for k,v in sorted(groups.items())}},indent=2,sort_keys=True))
if __name__=='__main__': main()
