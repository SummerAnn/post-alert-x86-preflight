#!/usr/bin/env python3
"""Create a rollback control that disables compliance delivery."""
from pathlib import Path
import argparse, shutil

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
    shutil.copytree(a.source,a.out,dirs_exist_ok=True); p=a.out/'validator.py'; s=p.read_text()
    start=s.index('def send_compliance_report('); end=s.index('\ndef validate_directory',start)
    replacement='def send_compliance_report(files_validated, schema_violations, resolved_vars, compliance_endpoint):\n    # ROLLBACK CONTROL: disable external compliance delivery.\n    return False\n'
    p.write_text(s[:start]+replacement+s[end:]); print(a.out)
if __name__=='__main__': main()
