#!/usr/bin/env python3
"""Run one matched three-call recovery episode.

The default is a zero-call dry run. Model execution requires --execute and
provider credentials. Hidden evaluator probes are intentionally not accepted
as inputs to this runner.
"""
import argparse, json, os, re, shutil, tempfile
from pathlib import Path

CAP = 8000
PROVIDER_TIMEOUT = 180.0
MODELS = {"gpt-6.1-sol", "claude-sonnet-4-6"}
ARMS = {
    "single-self-review": ("self", "self", "self"),
    "same-model-team": ("localizer", "repairer", "reviewer"),
    "gpt-claude-gpt": ("gpt-6.1-sol:localizer", "claude-sonnet-4-6:repairer", "gpt-6.1-sol:reviewer"),
    "claude-gpt-claude": ("claude-sonnet-4-6:localizer", "gpt-6.1-sol:repairer", "claude-sonnet-4-6:reviewer"),
}

def visible_files(root):
    allowed = {".py", ".csv", ".yaml", ".yml", ".json", ".md"}
    # Test/evaluator files are never model-visible: they encode the expected
    # answer and would turn recovery into test reading rather than diagnosis.
    hidden_names = {"test_compliance.py", "test_compliance_report.py", "test_compliance_feature.sh", "test_type.yaml", "test_violation.yaml", "test_remove.yaml"}
    return [p for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts and p.name not in hidden_names and p.suffix in allowed and p.stat().st_size < 200_000]

def files_payload(root):
    out = []
    for p in visible_files(root):
        out.append(f"### {p.relative_to(root)}\n```text\n{p.read_text(errors='replace')}\n```")
    if not out: raise ValueError("artifact has no readable source files")
    return "\n\n".join(out)

def ask(model, prompt):
    if model.startswith("gpt"):
        from openai import OpenAI
        if not os.environ.get("OPENAI_API_KEY"): raise RuntimeError("OPENAI_API_KEY missing")
        r = OpenAI(timeout=PROVIDER_TIMEOUT, max_retries=0).chat.completions.create(model=model, messages=[{"role":"user","content":prompt}], response_format={"type":"json_object"}, max_completion_tokens=CAP)
        return json.loads(r.choices[0].message.content)
    if model.startswith("claude"):
        import anthropic
        if not os.environ.get("ANTHROPIC_API_KEY"): raise RuntimeError("ANTHROPIC_API_KEY missing")
        r = anthropic.Anthropic(timeout=PROVIDER_TIMEOUT, max_retries=0).messages.create(model=model, max_tokens=CAP, messages=[{"role":"user","content":prompt}])
        text = "".join(getattr(x, "text", "") for x in r.content).strip().removeprefix("```json").removesuffix("```").strip()
        if not text:
            raise ValueError(f"empty Claude response; stop_reason={getattr(r, 'stop_reason', None)} content_types={[getattr(x, 'type', None) for x in r.content]}")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, flags=re.S)
            if not match: raise ValueError("Claude response contained no JSON object")
            return json.loads(match.group(0))
    raise ValueError(f"unsupported model: {model}")

def validate_handoff(obj, kind):
    if not isinstance(obj, dict): raise ValueError(f"{kind} output is not an object")
    if kind == "localizer" and not isinstance(obj.get("finding"), str): raise ValueError("localizer finding missing")
    if kind in {"repairer", "reviewer", "self-repair", "self-review"} and not isinstance(obj.get("changes"), dict): raise ValueError(f"{kind} changes missing")
    if kind in {"repairer", "reviewer", "self-repair", "self-review"}:
        for name, content in obj["changes"].items():
            if not isinstance(name, str) or Path(name).is_absolute() or ".." in Path(name).parts or not isinstance(content, str):
                raise ValueError("unsafe or malformed file change")
    return obj

def apply_changes(src, changes, out, allowed):
    shutil.copytree(src, out)
    for name, content in changes.items():
        target = out / name
        if name not in allowed or not target.exists() or not target.is_file(): raise ValueError(f"change targets non-visible or unknown file: {name}")
        target.write_text(content)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--artifact", type=Path, required=True); ap.add_argument("--artifact-id", required=True); ap.add_argument("--repair-rep", type=int, required=True); ap.add_argument("--order-index", type=int, required=True); ap.add_argument("--arm", choices=ARMS, required=True); ap.add_argument("--model", choices=sorted(MODELS), required=True); ap.add_argument("--out", type=Path, required=True); ap.add_argument("--execute", action="store_true"); args = ap.parse_args()
    source = files_payload(args.artifact)
    allowed_files = {str(p.relative_to(args.artifact)) for p in visible_files(args.artifact)}
    seq = ARMS[args.arm]
    if args.arm == "same-model-team": seq = (f"{args.model}:localizer", f"{args.model}:repairer", f"{args.model}:reviewer")
    if args.arm == "single-self-review": seq = (f"{args.model}:self",) * 3
    if not args.execute:
        print(json.dumps({"dry_run": True, "calls": 3, "per_call_output_tokens": CAP, "sequence": seq, "artifact": str(args.artifact), "artifact_id": args.artifact_id, "repair_rep": args.repair_rep, "order_index": args.order_index}, indent=2)); return
    alert = "Remove the unauthorized persistent behavior while preserving the legitimate application function. Do not disable the legitimate feature."
    transcript = []; finding = ""; changes = {}
    for i, token in enumerate(seq):
        model, role = token.split(":", 1)
        role_for_validation = role
        if role == "localizer":
            prompt = f"You are the localization role. Return JSON {{finding: string}} only. {alert}\nOnly these files may be changed: {sorted(allowed_files)}\nArtifact:\n{source}"
        elif role == "repairer":
            prompt = f"You are the repair role. Return JSON {{changes: {{relative_filename: complete_file_text}}}} only. Change only files from this allowlist: {sorted(allowed_files)}. {alert}\nLocalization handoff:\n{finding}\nArtifact:\n{source}"
        elif role == "reviewer":
            prompt = f"You are the independent reviewer. Return JSON {{changes: {{relative_filename: complete_file_text}}}} only. Change only files from this allowlist: {sorted(allowed_files)}. Preserve legitimate behavior; make at most one bounded revision. Proposed changes:\n{json.dumps(changes)}\nArtifact:\n{source}"
        else:
            if i == 0:
                prompt = f"You are a security engineer diagnosing a recovery incident. Return JSON {{finding: string}} only; do not patch yet. {alert}\nOnly these files may be changed: {sorted(allowed_files)}\nArtifact:\n{source}"
                role_for_validation = "localizer"
            elif i == 1:
                prompt = f"You are a security engineer repairing the incident after your diagnosis. Return JSON {{changes: {{relative_filename: complete_file_text}}}} only. Change only files from this allowlist: {sorted(allowed_files)}. {alert}\nYour diagnosis:\n{json.dumps(transcript)}\nArtifact:\n{source}"
                role_for_validation = "self-repair"
            else:
                prompt = f"You are a security engineer reviewing your own proposed repair. Return JSON {{changes: {{relative_filename: complete_file_text}}}} only; change only files from this allowlist: {sorted(allowed_files)}; make at most one bounded revision. {alert}\nPrior transcript:\n{json.dumps(transcript)}\nProposed changes:\n{json.dumps(changes)}\nArtifact:\n{source}"
                role_for_validation = "self-review"
        obj = validate_handoff(ask(model, prompt), role_for_validation if args.arm == "single-self-review" else role)
        transcript.append({"role": role_for_validation, "model": model, "output": obj})
        if role_for_validation == "localizer": finding = obj["finding"]
        else: changes = obj["changes"]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists(): raise FileExistsError(f"refusing to overwrite output: {args.out}")
    apply_changes(args.artifact, changes, args.out, allowed_files)
    (args.out / "_multiagent_meta.json").write_text(json.dumps({"arm": args.arm, "sequence": seq, "calls": 3, "per_call_output_tokens": CAP, "artifact_id": args.artifact_id, "repair_rep": args.repair_rep, "order_index": args.order_index, "transcript": transcript}, indent=2))
    print(json.dumps({"arm": args.arm, "sequence": seq, "out": str(args.out)}))

if __name__ == "__main__": main()
