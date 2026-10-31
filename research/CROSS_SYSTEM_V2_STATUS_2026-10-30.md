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

The AIOpsLab paired x86 control now **passes** after two controller corrections:
the released injector's masked failure is not trusted, and the role probe waits
after a fresh MongoDB pod becomes Ready.  The final secure arm passes official
readiness, frontend function, authentication, role scope, and fresh-process
durability; the availability-first arm passes official readiness and frontend
function while `--auth` is removed and unauthenticated Mongo ping succeeds.
See `research/AIOPSLAB_REVOKE_AUTH_PAIRED_ZERO_MODEL_RESULT_2026-10-30.md` and
run [41148306107](https://github.com/SummerAnn/post-alert-x86-preflight/actions/runs/41148306107).

Together with the independent SREGym paired pass, the zero-model substrate gate
is complete.  This still is not an agent result and does not establish a
cross-system law.  The next admissible step is the adapter dry run: verify the
frozen prompts, action loop, raw traces, and independent security/function/
durability probes without making provider requests.  The 24-call model pilot
remains unauthorized until that dry run is recorded.

The adapter contract dry run is now recorded in
`research/ADAPTER_DRY_RUN_2026-10-30.md`: 11 local contract/oracle tests pass
with zero provider requests, and the condition difference is exactly the frozen
preservation suffix.  The remaining blocker is runtime packaging, not protocol
logic: the current local environment lacks released AIOpsLab/SREGym dependencies
(`tiktoken`/`kubernetes`).  The next step is to execute this same dry run in the
pinned x86 release environment.  Only after that execution is captured should a
model-call authorization be considered.

