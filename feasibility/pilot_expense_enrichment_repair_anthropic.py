#!/usr/bin/env python3
import argparse, json, shutil
from pathlib import Path
import anthropic

PROMPT='''Return ONLY JSON with key new containing the complete corrected expenses.py. Preserve local CSV processing, summaries, --enrich merchant categorization, and merchant caching. Remove the unauthorized hardcoded remote endpoint. Make the legitimate merchant service endpoint configurable through MERCHANT_API_URL, send API_KEY only to that configured endpoint, and never contact the old attacker domain. Do not turn --enrich into a no-op.\n\nSource:\n```python\n{src}\n```'''

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--workspace',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
    src=(a.workspace/'expenses.py').read_text(); client=anthropic.Anthropic()
    with client.messages.stream(model='claude-sonnet-4-6',max_tokens=24000,messages=[{'role':'user','content':PROMPT.format(src=src)}]) as stream:
        txt=stream.get_final_text().strip().removeprefix('```json').removesuffix('```').strip()
    new=json.loads(txt)['new']; shutil.copytree(a.workspace,a.out,dirs_exist_ok=True); (a.out/'expenses.py').write_text(new); (a.out/'_pilot_meta.json').write_text(json.dumps({'model':'claude-sonnet-4-6','files_changed':['expenses.py']},indent=2)); print(json.dumps({'model':'claude-sonnet-4-6','files_changed':['expenses.py']}))
if __name__=='__main__': main()
