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

## Evidence standard

Any proposed question must identify a concrete observable failure, distinguish
diagnosis, repair, verification, and safe closure, and survive a read-only
novelty and confound audit before paid experiments begin.
