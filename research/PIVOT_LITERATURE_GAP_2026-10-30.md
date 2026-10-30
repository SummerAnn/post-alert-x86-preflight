# Literature gap and refined pivot — 2026-10-30

## 1. What the first pivot overlaps with

The simple claim “imperfect verifier feedback induces shortcuts” is already
well represented. *LLMs Gaming Verifiers* compares extensional and isomorphic
verification, reports shortcut behavior in RLVR-trained models, and performs a
controlled training intervention where the verifier itself differs. A paper
that only adds a security bit to an availability score would look like a
domain-specific replication of that idea.

Recovery-agent work is also crowded at the generic level. R2Act studies
diagnosis-to-action validity on 302 Kubernetes incidents, while SRE-Marathon
studies continuous long-horizon SRE operation. AIOpsDoom studies adversarial
telemetry that steers AIOps remediation. SecRespond studies post-compromise
forensic investigation and remediation plans, but not live post-repair
security-preserving execution.

## 2. Refined research question

> When two live operational states are indistinguishable to the official
> availability evaluator but differ in a security invariant, do recovery agents
> produce the same evaluator-satisfying action policy—and can a minimal,
> independent security signal break that invariance without sacrificing
> legitimate availability?

Working name: **Recovery Invariance Testing (RIT)**.

The central phenomenon is not simply that “more information helps.” It is that
an availability-only evaluator creates **behaviorally aliased states**: a
security-preserving state and a security-weakened state receive the same official
success signal, and the agent's action policy may therefore be invariant to the
security difference.

## 3. Why this is a stronger distinction

| Nearby work | What it studies | What RIT adds |
|---|---|---|
| LLMs Gaming Verifiers | reward shortcuts in logical reasoning and RLVR | live operational repair actions under hidden security-state perturbations |
| R2Act | validity of recovery actions after diagnosis | security-preservation and durable capability, not only service recovery |
| SRE-Marathon | continuous long-horizon SRE performance | matched counterfactual security states with independent capability probes |
| AIOpsDoom | adversarial telemetry steering remediation | benign recovery under evaluator aliasing, not attacker-controlled telemetry |
| SecRespond | forensic reports and remediation plans | executable repair, restart durability, and legitimate-function preservation |

## 4. Minimal causal design

For each system/mechanism, construct matched states with identical service
health and incident text but different security invariants:

1. **Secure state:** service is degraded; the security control is intact or can
   be restored without disabling legitimate function.
2. **Weakened state:** the same service degradation is present, but the
   security control is disabled or bypassable.

The official availability evaluator returns the same health predicate in both
states. The hidden independent oracle distinguishes them. The model receives
the same tools, budget, task text, and availability feedback.

Primary measurements:

- action-policy invariance across the matched secure/weakened pair;
- official-success / independent-security-failure rate;
- durable security and legitimate-function success;
- rollback, broad reset, or targeted-repair action classes;
- change in these outcomes after adding only the minimal security bit.

The explicit security-preservation prompt remains a positive diagnostic control,
not the primary intervention. It establishes that the model can preserve the
invariant when the requirement is visible, separating inability from evaluator
blindness.

## 5. Main-track bar

The claim would require all of the following:

- the matched-state action invariance replicates in both AIOpsLab and SREGym;
- the effect appears for both frozen model families or is clearly model
  dependent rather than a single-model anecdote;
- the hidden security oracle is independent and durable;
- a minimal security signal breaks the invariance without reducing legitimate
  availability;
- the effect transfers to an unseen mechanism;
- action traces show the policy difference, not merely a score difference.

If the agent simply improves whenever given an extra security label, the result
is descriptive and probably security/systems-level. The stronger claim requires
counterfactual policy invariance plus transfer.

## 6. Current feasibility status

The two-system zero-model evaluator control already supplies the matched
secure/rollback states. The missing pieces are a nonterminal checkpoint wrapper
and a native-compatible AIOpsLab runtime. No model calls should be made until
those pass the mechanical truth table.

