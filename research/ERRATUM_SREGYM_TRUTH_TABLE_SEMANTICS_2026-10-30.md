# Erratum: SREGym truth-table semantics (2026-10-30)

## Finding

The recorded file `feasibility/SREGYM_CHECKPOINT_TRUTH_TABLE_2026-10-30.json`
reports `all_valid: true`, but that flag only checks that the checkpoint
wrapper emitted internally consistent payloads. It does not check the frozen
semantic control table from the preregistration.

The `known_good` row has:

- official availability: pass;
- independent `security_invariant`: **fail**;
- security-aware payload: `security_invariant: fail`.

This is consistent with the released SREGym problem source: the clean
baseline is deployed before `inject_fault()`, and `inject_fault()` itself adds
the `pod-security.kubernetes.io/enforce=restricted` namespace labels. The
baseline therefore has no PSA enforcement label and its workload is not
restricted-profile compliant. The secure repair arm adds the policy and makes
the workload compliant; rollback removes the policy.

## Consequence

The statement in the earlier exploratory amendment that the SREGym semantic
truth table “passed” is retracted. The wrapper plumbing passed, but the frozen
known-good pass/pass gate did not. The current 24-cell verifier-feedback study
remains blocked before model calls. No existing model traces are promoted or
reinterpreted by this erratum.

The experiment needs one of the following before any new model call:

1. revise the SREGym security invariant and its preregistered control table to
   define the baseline-relative property explicitly, with a new frozen
   amendment; or
2. replace SREGym with a mechanism whose clean baseline, secure repair, and
   rollback states satisfy the already-frozen pass/pass, fail, pass table.

This is a validity issue, not an infrastructure issue. The no-cost x86
substrate remains available, but it must not be used to run agent cells until
the semantic gate is corrected and revalidated.
