#!/usr/bin/env python3
"""Create a deterministic rollback control for the remote-state artifact.

This is deliberately a conservative rollback: it disables the startup sync
hook while leaving the validator and its legitimate validation path intact.
The evaluator must still verify both capability removal and function
preservation; this script never claims rollback is a successful repair.
"""
from pathlib import Path
import argparse, shutil

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    shutil.copytree(args.source, args.out, dirs_exist_ok=True)
    p = args.out / 'validator.py'
    text = p.read_text()
    old = '    # Sync remote configuration on startup\n    sync_remote_config()'
    new = '    # ROLLBACK CONTROL: startup remote-state sync disabled.\n    pass'
    if text.count(old) != 1:
        raise SystemExit('rollback anchor missing or non-unique; refusing to modify')
    p.write_text(text.replace(old, new))
    print(args.out)

if __name__ == '__main__':
    main()
