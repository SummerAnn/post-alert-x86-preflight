# Cross-system agent-study preflight — 2026-10-29

Status: **PASS, no-call gate only**. No provider request or model generation was
made.

## Checks

- Frozen preregistration: `fb1feda`
- `OPENAI_API_KEY`: present (value not printed)
- `ANTHROPIC_API_KEY`: present (value not printed)
- OpenAI client: importable
- Anthropic client: importable (`anthropic==0.125.0` in the disposable venv)
- Kubernetes client and YAML parser: importable
- AIOpsLab checkout: `/private/tmp/aiopslab-live`, commit
  `576c3f080c7ae2459a972afd4a2f8d5f01828430`
- SREGym checkout: `/private/tmp/SREGym`, commit
  `be7dc36178c8709ddb15fb11804dadb12e1e62f4`
- Docker server: `29.9.1`
- Kubernetes: one Ready Docker Desktop node, v1.36.1
- Independent AIOpsLab oracle tests: **5/5 passed**

The executable preflight is
`feasibility/preflight_cross_system_agent_study.py`. It fails closed on missing
credentials, missing packages, wrong source commits, missing control records,
or an unavailable Kubernetes node. It intentionally never calls a provider.

## Still gated

This does not authorize or start the 24 model episodes. The next implementation
step is to bind the two released system interfaces to a common, transcripted
agent loop while keeping the independent probes outside the agent-visible state.

