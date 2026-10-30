# Amendment — native incident prompt semantics (2026-10-30)

Status: **committed before any model calls**.

## Trigger

The pre-call audit compared the actual released incident descriptions with the
frozen prompt contract. Both released tasks name their mechanism in the native
description: AIOpsLab mentions TLS, and SREGym describes Pod Security Admission.
Therefore an availability arm that forbids those words would require rewriting
the released task and would not be a faithful released-system study.

## Frozen correction

The native-alert arm now preserves each released system's task text verbatim.
The diagnostic contrast is:

1. **released native alert:** no additional preservation requirement;
2. **explicit preservation contract:** the identical native alert plus one
   sentence requiring the named invariant to remain enforced.

The independent security oracle, oracle results, evaluator implementation, and
expected arm labels remain hidden. The official evaluator and all budgets remain
unchanged. The claim is narrowed accordingly: this tests whether an explicit
preservation obligation changes durable recovery, not whether agents can recover
security when the incident mechanism is lexically undisclosed.

The adapter validation and unit tests were updated to enforce identical native
messages and absence of only the appended requirement in the native arm.
No model or provider calls occurred before or after this amendment.
