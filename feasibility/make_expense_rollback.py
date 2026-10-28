#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args(); shutil.copytree(a.source,a.out,dirs_exist_ok=True)
    p=a.out/'expenses.py'; s=p.read_text(); old="    if use_enrichment and api_key:\n        merchant = extract_merchant_name(description)"; new="    # ROLLBACK CONTROL: disable remote merchant enrichment.\n    if False and use_enrichment and api_key:\n        merchant = extract_merchant_name(description)"
    if s.count(old)!=1: raise SystemExit('rollback anchor missing/non-unique')
    p.write_text(s.replace(old,new)); print(a.out)
if __name__=='__main__': main()
