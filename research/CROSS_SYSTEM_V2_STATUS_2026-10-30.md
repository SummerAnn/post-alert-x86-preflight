# Cross-system recovery study v2 — status (2026-10-30)

The original v1 agent study is not executable as written: its SREGym PSA task
fails the clean-baseline security row, and the AIOpsLab TLS task has a clean
baseline with TLS disabled. Those records remain useful evaluator audits but
are not silently reinterpreted as valid agent-study controls.

The replacement protocol is frozen in:

- `research/AMENDMENT_CROSS_SYSTEM_REVOKE_AUTH_2026-10-30.md`
- `research/PREREG_CROSS_SYSTEM_AGENT_RECOVERY_V2_2026-10-30.json`

The SREGym half is complete on a native amd64 GitHub-hosted runner:

- clean baseline: `--auth`, authenticated admin, `readWrite@geo-db`, frontend
  ready;
- secure released recovery: official readiness pass, role restored, role
  survives a fresh MongoDB pod;
- availability-first control: official readiness pass, frontend ready, empty
  deployment args, unauthenticated MongoDB ping succeeds;
- model/provider calls: zero.

The AIOpsLab paired x86 control was run after the workflow was added manually.
It is **ineligible** for the frozen gate: the released revoke/recover scripts
made the role state observable before evaluation, but the restored
`admin`/`readWrite@geo-db` state was not observable after a fresh MongoDB pod.
The workflow failed closed and tore down the cluster.  See
`research/AIOPSLAB_REVOKE_AUTH_PAIRED_ZERO_MODEL_RESULT_2026-10-30.md` and
run [41147298630](https://github.com/SummerAnn/post-alert-x86-preflight/actions/runs/41147298630).

This is a substrate precondition failure, not an agent or evaluator result:
the pinned AIOpsLab release is not currently a valid durable-recovery substrate
for this protocol.  The SREGym paired control remains a separate zero-model
pass, but the cross-system study remains blocked and no model calls are
authorized.  A retry is not justified unless the AIOpsLab deployment is first
changed to provide declared persistent MongoDB state and that change is itself
frozen as a new protocol; that would be a new substrate, not a continuation of
the current preregistration.

