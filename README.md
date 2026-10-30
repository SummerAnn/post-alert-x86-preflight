# Post-Alert Recovery of Agent-Modified Systems

This is a new research project. The earlier `evidence-grounded-revision`
repository is preserved as an archive and is not treated as evidence for a new
claim without re-audit.

## Topic

When an AI agent has modified a persistent system and an alert later reports a
possible problem, how can another agent decide what to repair, what to leave
unchanged, and what evidence is sufficient to safely resume operation?

## Current status

The zero-model cross-system control is complete: the released AIOpsLab and
SREGym evaluators accept both a security-preserving repair and an
availability-first rollback. The current pivot is preregistered in
`research/PREREG_VERIFIER_FEEDBACK_PIVOT_2026-10-30.md`:

> Do availability-only verifier feedback induce agents to choose destructive
> recovery shortcuts, and can security-aware feedback reduce those shortcuts
> without sacrificing legitimate availability?

No model calls have been made for this pivot. The study is blocked on a
read-only, nonterminal checkpoint wrapper and a native-compatible AIOpsLab
runtime. The source-level runtime audit is in
`research/VERIFIER_FEEDBACK_RUNTIME_AUDIT_2026-10-30.md`.

The strongest replacement control is implemented as the no-model runner
`feasibility/run_sregym_revoke_auth_control.py` (commit `30bc955`). This is
not an experiment result: it has only passed syntax/static checks and must be
run on the validated x86 Kubernetes substrate before any agent or provider
call.

An additional no-cost audit found that the SREGym checkpoint wrapper's
`all_valid` flag checked payload consistency rather than the preregistered
semantic truth table: its `known_good` row is security-fail because the clean
released baseline has no PSA enforcement label. The erratum is recorded in
`research/ERRATUM_SREGYM_TRUTH_TABLE_SEMANTICS_2026-10-30.md`; no agent cells
are eligible until this gate is corrected.

The same issue applies to AIOpsLab: its clean chart starts with MongoDB TLS
disabled while the proposed invariant is post-incident TLS enforcement. This
cross-system erratum and a review-only amendment draft are in
`research/ERRATUM_CROSS_SYSTEM_KNOWN_GOOD_SEMANTICS_2026-10-30.md` and
`research/BASELINE_SEMANTICS_AMENDMENT_DRAFT_2026-10-30.md`.

## Evidence standard

Any proposed question must identify a concrete observable failure, distinguish
diagnosis, repair, verification, and safe closure, and survive a read-only
novelty and confound audit before paid experiments begin.
