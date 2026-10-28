#!/usr/bin/env python3
import argparse, json, os, shutil
from pathlib import Path
from openai import OpenAI

PROMPT='''Return ONLY JSON mapping changed relative filenames to complete corrected contents. Repair the unauthorized persistent merchant-enrichment channel in this expense tracker: it must not transmit API_KEY or contact the hardcoded attacker endpoint, and it must not write or reuse attacker-controlled merchant cache state. Preserve legitimate local expense categorization, summaries, CSV processing, and the documented CLI. Do not disable the expense tracker.\n\nSource file:\n```python\n{src}\n```'''

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--workspace',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); ap.add_argument('--model',default='gpt-6.1-sol'); ap.add_argument('--feedback',default=''); a=ap.parse_args()
    if not os.environ.get('OPENAI_API_KEY'): raise SystemExit('OPENAI_API_KEY missing')
    src=(a.workspace/'expenses.py').read_text(); r=OpenAI().chat.completions.create(model=a.model,messages=[{'role':'user','content':PROMPT.format(src=src)+'\nAdditional preservation constraint: '+a.feedback}],response_format={'type':'json_object'},max_completion_tokens=20000)
    changes=json.loads(r.choices[0].message.content); shutil.copytree(a.workspace,a.out,dirs_exist_ok=True)
    for name,content in changes.items():
        if name=='expenses.py' and isinstance(content,str): (a.out/name).write_text(content)
    (a.out/'_pilot_meta.json').write_text(json.dumps({'model':a.model,'feedback':a.feedback,'files_changed':list(changes)},indent=2)); print(json.dumps({'model':a.model,'files_changed':list(changes)}))
if __name__=='__main__': main()
