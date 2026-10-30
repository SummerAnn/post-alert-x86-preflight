# Runtime audit for verifier-feedback intervention — 2026-10-30

**Status:** read-only source audit; no model calls and no live task mutation

## Finding

The released AIOpsLab and SREGym interfaces do not natively expose a
nonterminal evaluator-feedback checkpoint. Their normal `submit` operation is
a terminal or stage-advancing action. Therefore the verifier-feedback study
cannot be run by merely appending a second prompt condition.

## AIOpsLab source path

- `aiopslab/orchestrator/orchestrator.py::start_problem` calls the agent until
  the environment returns `SubmissionStatus.VALID_SUBMISSION`.
- The mitigation task's `submit()` action returns `VALID_SUBMISSION` when a
  submission is made.
- Only after the loop exits does `start_problem` call
  `problem.eval(...)`, including `wait_until_pods_healthy`.
- The agent therefore receives no official evaluator result before the episode
  terminates.

## SREGym source path

- `sregym/conductor/conductor.py::submit` accepts the submission and evaluates
  the current stage in a background worker.
- `clients/stratus/tools/submit_tool.py` turns a successful response into
  `Submission complete. No further action is needed.` and marks the agent
  submitted.
- The released client does not expose the resulting oracle dictionary as an
  observation to the same mitigation episode.

## Consequence

The current 24-episode preregistration is not executable as written until a
checkpoint wrapper exists. Adding an independent oracle after the episode
would test evaluator disagreement, not verifier-induced policy behavior.

## Required wrapper before any model call

Build and test a separate `check_recovery` controller that:

1. invokes the unchanged released availability oracle in a read-only,
   nonterminal mode;
2. invokes the hidden independent security oracle outside the agent container;
3. returns only the frozen feedback payload from
   `feasibility/verifier_feedback.py`;
4. leaves the released final submission and final evaluator unchanged;
5. records raw return codes, timestamps, and state hashes without exposing
   hidden probe details;
6. enforces a fixed checkpoint/turn budget and randomized condition order.

The wrapper must demonstrate on mechanical controls that it returns:

| state | availability | security-aware security field |
|---|---:|---:|
| known-good | pass | pass |
| secure repair | pass | pass |
| rollback | pass | fail |

If the released oracle cannot be called read-only before final submission, the
study must either (a) obtain an official maintainer-supported checkpoint API,
or (b) stop. A separately implemented health proxy would not be the released
evaluator and would invalidate the intended claim.

## Current decision

The pivot remains scientifically plausible, but it is **not ready for paid
model execution**. The next work block is a zero-model wrapper feasibility
gate. The native x86 runtime requirement remains a separate blocker for the
AIOpsLab arm.
