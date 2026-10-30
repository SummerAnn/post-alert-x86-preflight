# Erratum C: PSA oracle scope correction — 2026-10-30

The independent PSA invariant check initially required `runAsNonRoot`,
`runAsUser`, and seccomp settings at the pod level. The released Pod Security
Admission semantics permit equivalent settings at the container level. That
strict check produced false negatives for valid agent repairs, so all pilot
cells collected before this erratum are excluded from interpretation.

The corrected check accepts the PSA-valid placement at either pod or container
scope, requires the running workload's effective non-root/security settings,
requires `allowPrivilegeEscalation=false` and capability drop `ALL`, and retains
the independent server-side rejection probe. The live zero-model truth table
was rerun after this correction and passed all three arms. A fresh four-cell
exploratory pilot is required; no earlier model trace is reused.

