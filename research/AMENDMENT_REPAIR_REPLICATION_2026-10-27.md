# Amendment: independent repair replication unit

The original protocol called three fresh-process evaluator repetitions a cell
replication. That validates evaluator stability but does not replicate the
model-generated repair. It is insufficient for a repair-rate or model
comparison claim.

Before confirmatory analysis, targeted arms are therefore amended to require
three independently generated repair artifacts per `(mechanism, model)` using
the frozen prompt, model ID, temperature, and budget. Each repair artifact is
then evaluated in three fresh processes. The resulting design is:

`3 mechanisms × 2 targeted models × 3 independent repairs × 3 evaluator repeats`
plus positive and rollback controls.

The controls remain deterministic and are not treated as model replications.
No repair artifact may be copied across independent-repair indices. If any
required repair artifact is missing or malformed, that targeted cell is
incomplete and no model comparison is reported.

This amendment strengthens the study; it does not change the research question,
evaluator, prompts, models, or outcome definitions.
