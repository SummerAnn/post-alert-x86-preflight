# Cross-system agent adapter dry run — 2026-10-30

Status: **contract pass; released-runtime import gate incomplete**. No model or
provider requests were made, no Kubernetes episode was started, and no hidden
oracle state was read.

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
...........
Ran 11 tests in 0.033s
OK
```

## Runtime import check

`feasibility/adapter_preflight.py` was also run against the pinned source
checkouts. Prompt modules import, but the current local environment does not
contain all released runtime dependencies:

| released path | local result |
|---|---|
| AIOpsLab prompt template | importable |
| AIOpsLab ReAct/orchestrator | blocked by missing `tiktoken` / `kubernetes` |
| SREGym prompt module | importable |
| SREGym conductor | blocked by missing `kubernetes` |

These are environment setup failures, not agent or recovery results. The
source-pinned x86 control runner has already shown that both live substrates can
boot and pass the paired zero-model security/function/durability checks. The
remaining mechanical work is to run this adapter contract inside that pinned
x86 environment and capture raw action-loop traces without making a provider
request.

## Gate interpretation

The adapter logic is contract-valid, but the **model pilot is not yet
authorized or executable** from this local runtime. The required order remains:

1. execute the adapter dry run in the pinned x86 release environments;
2. verify raw action traces, fresh-process probes, and fail-closed void handling;
3. obtain an explicit authorization for the 24-call pilot;
4. run the pilot unchanged, then test an unseen security mechanism only if the
   preregistered policy-invariance signal appears in both systems.

No claim about agent behavior is made by this file.
