# Released-agent adapter preflight — 2026-10-29

Status: **message contract passed; execution environment incomplete**. No model
or provider calls were made, no Kubernetes problem was started, and no oracle
state was read.

## What was validated

- The shared prompt contract remains frozen: the availability arm is the
  released task text plus no preservation requirement; the contract arm differs
  only by the exact appended requirement.
- AIOpsLab's native context shape is preserved: a system message containing the
  released `clients.utils.templates.DOCS` rendering, followed by the released
  instruction message. The API map is partitioned into telemetry, shell, and
  submit sections exactly as the released ReAct client does.
- SREGym's native mini-SRE shape is preserved: its released system prompt,
  followed by the released conductor task text and the same condition suffix.
  The adapter does not add a hidden probe, evaluator output, or expected-arm
  label.
- Requested model IDs are fail-closed to `gpt-6.1-sol` and
  `claude-sonnet-4-6`; no substitution path exists.
- Unit tests passed: 9 adapter/prompt tests and the existing 5 AIOps oracle
  tests (11 tests in the combined run before adding this record).

## Runtime result

`feasibility/adapter_preflight.py` imports the released modules in a fresh
subprocess and reports bounded diagnostics:

| released path | result |
|---|---|
| AIOpsLab prompt template (`clients.utils.templates`) | importable |
| AIOpsLab ReAct/orchestrator | **not importable: `wandb` missing** |
| SREGym mini-SRE prompt module | importable |
| SREGym conductor module | importable |

The AIOpsLab checkout declares additional dependencies in its pinned
`pyproject.toml` (including `wandb`, `prometheus-api-client`, Elasticsearch,
Azure identity, FastAPI, and others) that are not all present in the shared
`/private/tmp/sregym-venv`. This is an environment setup issue, not evidence
about either model or recovery behavior.

## Gate interpretation

The 24-episode study is **not executable yet**. Installing or selecting a
source-pinned AIOpsLab runtime is required before any model call. The next
safe action is to create or identify a dedicated environment for the pinned
AIOpsLab commit, rerun this preflight, and only then perform a provider/model
resolution check. No model episode should start while this gate is red.

