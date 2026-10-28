# AIOpsLab novelty addendum (2026-10-28)

The exact AIOpsLab idea was checked against current primary literature before
any implementation.

## Results

* [R2Act](https://arxiv.org/abs/2607.04623) already evaluates the transition
  from diagnosis to valid recovery action on 302 quality-audited Kubernetes
  incidents. It reports high root-cause accuracy but only 36.8–60.3% recovery
  validity, including invalid actions after correct diagnosis. Therefore
  “agents diagnose incidents but perform unsafe/invalid recovery” is already a
  measured phenomenon.
* [AIOpsDoom/AIOpsShield](https://www.usenix.org/conference/usenixsecurity26/presentation/pasquini)
  already shows that adversarial telemetry can steer AIOps agents toward
  infrastructure-compromising remediation and evaluates a sanitization
  defense. Therefore a generic control-integrity or telemetry-trust claim is
  also occupied.

## Consequence

The proposed AIOpsLab extension—hidden security probes for MongoDB auth/TLS
plus availability checks—would be a useful engineering evaluator, but by
itself it is not a strong new research question. It would combine existing
substrate components with an already-established recovery-validity and
telemetry-manipulation theme.

To become publishable, it would need a genuinely new intervention or causal
finding beyond those papers, such as a reproducible security–availability
phase transition that is not explained by ordinary invalid-action error or
telemetry deception. No such finding is currently observed.

## Final gate

Do not build or run the AIOpsLab extension yet. The current post-alert-recovery
line has no justified next experiment from the available evidence. Further
work should begin only after identifying a new causal phenomenon with a
verified released substrate; otherwise the project should be closed as a
rigorous feasibility/evaluator study.
