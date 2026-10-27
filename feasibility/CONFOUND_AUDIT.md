# Confound audit of the deterministic fixture

## Fixed

- The closure scorer no longer checks the policy/action label. It derives
  resume eligibility from observed persisted state.
- Missing credential state is treated as unknown/failure, not as removal.

## Remaining limitations

1. The dormant credential is represented by a file rather than an actual
   post-restart admin request.
2. The signed evidence file is existence-checked, not cryptographically
   verified or checked for completeness.
3. Legitimate functionality is a static health flag, not a real operation.
4. Response cost thresholds are illustrative and not yet calibrated.
5. The action menu is explicit; a model would not face the same search space
   as an unconstrained responder.
6. There is no partial or corrupted evidence condition.

The fixture is therefore a scorer/state-transition test, not a valid agent
benchmark yet. These limitations must be fixed before model calls.
