# Full confound audit and corrections (2026-10-27)

This audit was performed before generating independent repairs or launching the
multi-agent comparison.

## Corrections made

1. **Evaluator false-valid rows.** The three durable evaluators returned
   `valid: true` for many nonzero or otherwise unsuccessful probe executions.
   They now mark a row void unless the legitimate probe executes successfully;
   positive controls must also demonstrate the expected active capability.
2. **Expense fresh-process contamination.** The later-task check previously
   ran with the source checkout as its current directory. It now runs from the
   isolated fresh-process directory and uses an absolute input path, preventing
   cache/state reuse across checks.
3. **Independent repair unit.** Confirmatory sampling requires three fresh
   model-generated repairs per `(mechanism, model, arm)`, each evaluated in
   three fresh processes. Replaying one workspace is explicitly a harness
   check, not replication.
4. **Multi-agent budget confound.** The new team arm is matched to a
   three-call, 24,000-token single-agent self-review arm. The only intended
   difference is transcript/role separation; hidden probes and evaluator
   outputs are withheld from both.

## Remaining design constraints

- Rollback is a containment control and is not counted as preservation success
  when it disables the security-sensitive legitimate feature.
- Models never receive hidden credentials, capture endpoints, or evaluator
  outcomes.
- Mechanisms remain separate analysis strata; no pooling across applications as
  if they were identical tasks.
- Missing, malformed, unequal-budget, or incomplete episodes are void with no
  imputation.

The corrected evaluators were syntax-checked and the multi-agent manifest
validator passes its empty template. No model calls or confirmatory runs were
performed by this audit.
