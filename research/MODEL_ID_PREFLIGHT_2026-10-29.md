# Frozen model identity preflight — 2026-10-29

Status: **PASS for model identity; no generation occurred.** Two provider
metadata requests were made (`models.retrieve`), with zero model calls and no
study episode launched.

## Results

| requested ID | provider | result | resolved ID |
|---|---|---|---|
| `gpt-6.1-sol` | OpenAI | available | `gpt-6.1-sol` |
| `claude-sonnet-4-6` | Anthropic | available | `claude-sonnet-4-6` |

The process-level `OPENAI_API_KEY` was rejected by OpenAI. The user-provided
desktop key file contained a key-value line whose parsed OpenAI value was
accepted and resolved the exact frozen ID. No key value is stored in this
repository, printed in logs, or written back to the environment. The future
execution wrapper must load that value only in its child process and must fail
closed if the file format or model resolution differs.

## Gate state

- Dedicated Python 3.12 runtime: ready.
- AIOpsLab and SREGym released agent/orchestrator imports: ready.
- Prompt/adaptor and independent-oracle tests: passing.
- Official zero-model controls: already passing in the prerequisite records.
- Model generation episodes: **not started**.

