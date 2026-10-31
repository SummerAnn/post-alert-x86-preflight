# Cross-system agent adapter dry run — 2026-10-30

Status: **PASS**. No model or provider requests were made, no Kubernetes episode
was started, and no hidden oracle state was read.

## What was exercised

The frozen adapter contract was executed with synthetic released prompt text for
both systems and both frozen model identifiers:

- AIOpsLab message shape: released system documentation rendering followed by
  the released user instruction message.
- SREGym message shape: released system text followed by the released conductor
  task message.
- The availability-only condition and the security-preservation condition were
  constructed from the same native task text; the latter adds only the frozen
  preservation requirement.
- Model identifiers are fail-closed (`gpt-6.1-sol` and
  `claude-sonnet-4-6`); no substitution path exists.
- The dry-run summaries contain no provider payload, credentials, or oracle
  output and report `provider_requests: 0` and `model_calls: 0`.

Command and result:

```text
PYTHONPATH=feasibility python3 -m unittest \
  test_cross_system_adapters test_adapter_preflight test_aiopslab_recovery_oracle
..............
Ran 14 tests in 0.038s
OK
```

The additional three tests cover the raw-action trace contract: exact model
text is retained, missing or ambiguous actions become explicit voids, and
invalid turn records fail closed.  No trace is silently converted into a
successful repair.

## Runtime import check

`feasibility/adapter_preflight.py` was first run against the system Python 3.9.6
and correctly failed closed because the pinned releases require Python 3.11--
3.12.  A disposable Python **3.12.9** environment was then created with the
declared runtime dependencies.  In that environment all released adapter paths
imported successfully:

| released path | local result |
|---|---|
| AIOpsLab prompt template | importable |
| AIOpsLab ReAct/orchestrator | importable |
| SREGym prompt module | importable |
| SREGym conductor | importable |

The Python 3.9 failure was an environment issue, not an agent or recovery
result.  The Python 3.12 rerun imported the released AIOpsLab `clients.react`
agent path and `aiopslab.orchestrator`, plus SREGym's `mini_sre` prompt module
and `sregym.conductor`.  It then constructed the native AIOpsLab system/user
messages and native SREGym system/user messages, applied the two frozen
conditions, and passed all assertions.  Both summaries reported
`provider_requests: 0` and `model_calls: 0`.

## Gate interpretation

The adapter logic is contract-valid and executable against the pinned released
Python runtime. The model pilot is now explicitly authorized by the user after
the x86 gate passed. This changes execution permission only; it does not change
any frozen model, prompt, budget, condition, repetition, or void rule. The
required order now is:

1. capture the same dry-run summary in the pinned x86 runner (the local
   Python-3.12 run is already clean);
2. verify raw action traces, fresh-process probes, and fail-closed void handling;
3. run the 24-call pilot unchanged, then test an unseen security mechanism only if the
   preregistered policy-invariance signal appears in both systems.

## Pinned x86 adapter gate

The same import and prompt-construction check passed in the public x86 runner:

- workflow run: https://github.com/SummerAnn/post-alert-x86-preflight/actions/runs/41156467348
- workflow commit: `fae56a0`
- job: `adapter-dry-run` (`124404242230`)
- logged `provider_requests: 0`, `model_calls: 0`
- both released interfaces imported and both frozen condition arms were
  constructed from the native task text.

No claim about agent behavior is made by this file; the first claim-bearing
artifact will be a complete, fail-closed per-cell result from the preregistered
runner.
