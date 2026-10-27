# Zero-model replay gate result

## Result: artifact source located; replay still not started

The Git checkout contains no saved attacked workspaces or logs, but the authors'
public Hugging Face archive does contain the missing evaluation artifacts. Its
dataset card lists archived `.eval` logs and result bundles, including the
persistent-state runs. This changes the gate from “artifact unavailable” to
“artifact acquisition and filtering required.”

This is not a failed scientific result. It is a reproducibility boundary:

- the scorer code gives executable postconditions for
  `support-preview-backdoor` and `triggered-api-exfil`;
- the persistent setting gives fresh-container and later-PR state injection;
- but there is no released state on which to test rollback, repair, restart, or
  dormant-residue behavior.

## Consequence

No model calls or paid pilot should start yet. A hand-written attack fixture
would test our reconstruction, not the benchmark's agent-generated persistent
attack, and would risk repeating the earlier toy-benchmark problem.

## Legitimate next choices

1. Download only the relevant persistent-state `.eval` subset from the public
   archive and inspect whether tool traces contain enough workspace information
   to reconstruct a known-positive final state; or
2. if the logs omit the needed state, explicitly preregister a zero-model
   fixture-construction study whose sole
   purpose is validating the recovery harness, not estimating agent recovery.

Until one of those is available, the post-alert question is a strong candidate
but not yet evidence-backed.
