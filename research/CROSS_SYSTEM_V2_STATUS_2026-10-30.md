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

The AIOpsLab x86 authorization workflow currently verifies only the secure arm.
The required paired x86 control (secure arm plus availability-first arm) does
not yet exist as evidence. Therefore the v2 preflight fails closed and no model
calls are authorized. The next concrete action is to add and run that one
zero-model AIOpsLab paired control; only if it passes should the adapter dry run
and the 24-call pilot be considered.

I prepared the native-amd64 paired-control workflow, but the connected GitHub
integration rejected the repository write with HTTP 403. No public workflow was
changed, and no runner or model call was started. The local protocol and
preflight remain the source of truth until that write is authorized or the
workflow is added manually.

