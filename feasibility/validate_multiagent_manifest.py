#!/usr/bin/env python3
"""Fail-closed validation for the matched multi-agent study manifest.

This performs no model calls. It checks that an episode can be compared fairly
before any paid run is allowed.
"""
import argparse, json
from pathlib import Path

REQUIRED = {
    "protocol", "models", "mechanisms", "arms", "calls_per_episode",
    "max_output_tokens_total", "per_call_output_tokens", "repair_replicates_per_cell",
    "evaluator_repetitions_per_repair", "randomization_seed", "pairing", "reviewer_revision_limit", "handoff_schema_version", "role_sequences", "episodes"
}
EXPECTED_ARMS = {"single-self-review", "same-model-team", "gpt-claude-gpt", "claude-gpt-claude"}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("manifest", type=Path); args = ap.parse_args()
    m = json.loads(args.manifest.read_text())
    missing = REQUIRED - set(m)
    errors = []
    if missing: errors.append(f"missing fields: {sorted(missing)}")
    if set(m.get("arms", [])) != EXPECTED_ARMS: errors.append("arms must include baseline, same-model, and both heterogeneous directions")
    seq = m.get("role_sequences", {})
    for arm in EXPECTED_ARMS:
        if arm not in seq or len(seq[arm]) != 3: errors.append(f"missing three-role sequence for {arm}")
    if m.get("calls_per_episode") != 3: errors.append("calls_per_episode must be 3")
    if m.get("max_output_tokens_total") != 24000: errors.append("total token cap must be 24000")
    if m.get("per_call_output_tokens") != 8000: errors.append("each role must have an 8000-token cap")
    if m.get("repair_replicates_per_cell") != 3: errors.append("three independent repairs required")
    if m.get("evaluator_repetitions_per_repair") != 3: errors.append("three fresh-process evaluator repetitions required")
    if m.get("pairing") != "artifact_id+repair_rep": errors.append("pairing must be artifact_id+repair_rep")
    if m.get("reviewer_revision_limit") != 1: errors.append("reviewer revision limit must be one")
    seen = set()
    for i, ep in enumerate(m.get("episodes", [])):
        for k in ("episode_id", "artifact_id", "model", "mechanism", "arm", "repair_rep", "order_index"):
            if k not in ep: errors.append(f"episode {i}: missing {k}")
        key = ep.get("episode_id")
        if key in seen: errors.append(f"duplicate episode_id: {key}")
        seen.add(key)
        if ep.get("arm") not in EXPECTED_ARMS: errors.append(f"episode {i}: invalid arm")
        if ep.get("calls_per_episode") != 3: errors.append(f"episode {i}: call count mismatch")
        if ep.get("max_output_tokens_total") != 24000: errors.append(f"episode {i}: token budget mismatch")
        if ep.get("per_call_output_tokens") != 8000: errors.append(f"episode {i}: per-call budget mismatch")
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2)); raise SystemExit(1)
    print(json.dumps({"valid": True, "episodes": len(m.get("episodes", [])), "arms": sorted(EXPECTED_ARMS)}, indent=2))

if __name__ == "__main__": main()
