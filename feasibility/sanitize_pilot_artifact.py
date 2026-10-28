#!/usr/bin/env python3
"""Create a pilot-only copy with credential-like literals replaced.

The sanitizer preserves source structure and attack behavior while preventing
accidental transmission of real or credential-shaped values to a model API.
"""
import argparse, re, shutil
from pathlib import Path

PATTERNS = [
    (r"sk-[A-Za-z0-9_-]+", "sk-SYNTHETIC_KEY"),
    (r"whsec_[A-Za-z0-9_-]+", "whsec_SYNTHETIC"),
    (r"bearer_token_[A-Za-z0-9_-]+", "bearer_token_SYNTHETIC"),
    (r"supersecret[A-Za-z0-9_-]*", "SYNTHETIC_SECRET"),
]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("src",type=Path); ap.add_argument("dst",type=Path); a=ap.parse_args()
    if a.dst.exists(): raise SystemExit(f"refusing to overwrite {a.dst}")
    shutil.copytree(a.src, a.dst)
    changed=0
    for p in a.dst.rglob("*"):
        if p.is_file() and p.stat().st_size < 2_000_000:
            try: s=p.read_text()
            except UnicodeDecodeError: continue
            t=s
            for pat,repl in PATTERNS: t=re.sub(pat,repl,t)
            if t != s: p.write_text(t); changed += 1
    print({"sanitized_files":changed,"output":str(a.dst)})

if __name__ == "__main__": main()
