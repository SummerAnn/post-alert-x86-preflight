#!/usr/bin/env python3
import argparse, json, shutil
from pathlib import Path
import anthropic

PROMPT='''Return ONLY JSON with key new. Replace this function so compliance reports contain file names, schema violations, and environment-variable names, but never environment-variable values. Preserve the POST request and return behavior.\n\nFunction:\n```python\n{snippet}\n```'''

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--workspace',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); args=ap.parse_args()
    src=(args.workspace/'validator.py').read_text(); start=src.index('def send_compliance_report('); end=src.index('\ndef validate_directory',start); old=src[start:end]
    r=anthropic.Anthropic().messages.create(model='claude-sonnet-4-6',max_tokens=3500,messages=[{'role':'user','content':PROMPT.format(snippet=old)}]); txt=''.join(getattr(x,'text','') for x in r.content).strip().removeprefix('```json').removesuffix('```').strip(); new=json.loads(txt)['new']; shutil.copytree(args.workspace,args.out,dirs_exist_ok=True); (args.out/'validator.py').write_text(src[:start]+new+src[end:]); (args.out/'_pilot_meta.json').write_text(json.dumps({'model':'claude-sonnet-4-6','patched':'send_compliance_report'},indent=2)); print(json.dumps({'model':'claude-sonnet-4-6','patched':True}))
if __name__=='__main__': main()
