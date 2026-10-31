# AIOpsLab revoke-auth paired control: zero-model result (2026-10-30)

This is a mechanical substrate check, not an agent experiment.  The workflow
ran on a GitHub-hosted amd64 runner with a pinned Kind x86 cluster and made
zero model/provider calls.

## Run provenance

- Public workflow repository: `SummerAnn/post-alert-x86-preflight`
- Workflow commit: `3ea868ad82491af915b61b5b59faa134eeebbc4a`
- Successful run: [41148306107](https://github.com/SummerAnn/post-alert-x86-preflight/actions/runs/41148306107)
- AIOpsLab: `576c3f080c7ae2459a972afd4a2f8d5f01828430`
- AIOpsLab applications: `8038be6b4989c647126f27715acc591c47133c2d`
- Runner: `ubuntu-24.04`, native `amd64` Kind node

## Result

The final run is **PASS** for the frozen paired-control gate.  In the secure
arm, the released fault and recovery scripts reached MongoDB, the role was
observably revoked and restored, the official readiness evaluator passed, the
frontend probe passed, and the restored `admin` authentication/
`readWrite@geo-db` invariant remained present after a fresh MongoDB pod.  In
the availability-first control, the official evaluator and frontend still
passed while the deployment had no `--auth` argument and unauthenticated Mongo
ping succeeded.  The cluster was torn down successfully.

The controller was deliberately stricter than the released injector: it did
not trust the injector's success text or exit status and retried until the
role state was observable.  It also waited for the role probe after a fresh
pod became Ready.  An earlier run with the same controller but an immediate
post-Ready probe failed; that was a harness race and is not counted as a
scientific result.  This final run still makes no claim about agents.

## Interpretation

This pinned AIOpsLab release now passes the mechanical durability precondition.
Together with the independent SREGym paired pass, the two released evaluator
implementations have a valid zero-model control.  The cross-system study is
still not an agent result: the next gate is an adapter dry run that checks the
frozen prompts, action loop, raw traces, and independent probes.  No model calls
are authorized by this record.

