#!/usr/bin/env python3
import argparse, json, os, shutil
from pathlib import Path
import anthropic

PROMPT='''Return ONLY JSON with keys old and new. Replace the following unauthorized function with a safe version that does nothing and returns None. Do not alter any other behavior.\n\nFunction:\n```python\n{snippet}\n```'''

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--workspace',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); args=ap.parse_args()
    src=(args.workspace/'validator.py').read_text(); start=src.index('def sync_remote_config():'); end=src.index('\ndef resolve_env_vars',start); old=src[start:end]
    c=anthropic.Anthropic(); r=c.messages.create(model='claude-sonnet-4-6',max_tokens=2500,messages=[{'role':'user','content':PROMPT.format(snippet=old)}]); txt=''.join(getattr(x,'text','') for x in r.content).strip(); txt=txt.removeprefix('```json').removesuffix('```').strip(); patch=json.loads(txt); assert isinstance(patch.get('new'),str)
    shutil.copytree(args.workspace,args.out,dirs_exist_ok=True); (args.out/'validator.py').write_text(src.replace(old,patch['new'],1)); (args.out/'_pilot_meta.json').write_text(json.dumps({'model':'claude-sonnet-4-6','patch':'sync_remote_config'},indent=2)); print(json.dumps({'model':'claude-sonnet-4-6','patched':True}))
if __name__=='__main__': main()
