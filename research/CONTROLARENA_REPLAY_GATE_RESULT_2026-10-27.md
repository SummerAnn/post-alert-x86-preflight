# Zero-model replay gate result

## Result: blocked before replay

The released checkout contains the side-task specifications and scorers, but no
saved attacked workspaces, trajectories, PR patches, or final application
artifacts. The repository therefore cannot provide a known-positive attack state
for a response replay without first synthesizing the attack artifact or running
an agent.

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

1. Obtain the authors' released run artifacts/trajectories, if available; or
2. explicitly preregister a zero-model fixture-construction study whose sole
   purpose is validating the recovery harness, not estimating agent recovery.

Until one of those is available, the post-alert question is a strong candidate
but not yet evidence-backed.
