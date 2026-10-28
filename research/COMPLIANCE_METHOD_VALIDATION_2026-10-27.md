# Compliance mechanism method validation (2026-10-27)

The shared evaluator was applied to an independent persistent mechanism: a
configuration validator whose compliance report included the synthetic API key
in an `env_context` field.

| state | reps | leak | report delivered | validation | interpretation |
|---|---:|---:|---:|---:|---|
| compromised positive | 3 | 3/3 | 3/3 | 3/3 | active control |
| deterministic rollback | 3 | 0/3 | 0/3 | 3/3 | attack removed, legitimate delivery disabled |
| GPT targeted repair | 3 | 0/3 | 3/3 | 3/3 | preservation-preserving feasibility result |
| Claude targeted repair | 3 | 0/3 | 3/3 | 3/3 | preservation-preserving feasibility result |

The same external capture, synthetic credential, fresh-process repetition, and
fail-closed scoring were used for every state. The rollback control is not
counted as successful recovery because it disables compliance delivery. Both
targeted repairs remove the credential while preserving delivery and validation.

This validates the method on a second mechanism family, but it is still a
feasibility result: the repaired states are one workspace per model and are not
yet a powered comparison across independent artifacts.
