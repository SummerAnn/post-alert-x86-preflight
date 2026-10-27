# Minimal case overlap audit — 2026-10-27

The evidence-preservation case is technically scoreable, but its broad claim
is not clearly novel.

- SecRespond already occupies post-compromise agent incident response.
- R2Act explicitly separates diagnosis, recovery action, and service-health
  verification; its best diagnosis scores substantially exceed recovery-validity
  scores.
- Real-Time Detection and Repair of LLM Agent Failures includes deterministic
  verification of required calls and stated outcomes.

The proposed case could still be distinct only if it demonstrates a specific
causal tradeoff: an action that improves immediate containment while destroying
the independently recoverable evidence needed for later scope reconstruction or
closure. A generic benchmark showing that evidence preservation is desirable is
not enough.

## Decision

Do not spend model API credits on the current case yet. First build a
deterministic state-transition table and verify that the evidence-destroying
action can pass immediate containment but must fail later closure, while the
preserving action has a measurable utility cost. If that separation cannot be
made, close the branch.
