# AIOpsLab revoke-auth paired control: zero-model result (2026-10-30)

This is a mechanical substrate check, not an agent experiment.  The workflow
ran on a GitHub-hosted amd64 runner with a pinned Kind x86 cluster and made
zero model/provider calls.

## Run provenance

- Public workflow repository: `SummerAnn/post-alert-x86-preflight`
- Workflow commit: `86066bcc35eee4c1bb75baa59bd0b7690e57e4b2`
- Run: [41147298630](https://github.com/SummerAnn/post-alert-x86-preflight/actions/runs/41147298630)
- AIOpsLab: `576c3f080c7ae2459a972afd4a2f8d5f01828430`
- AIOpsLab applications: `8038be6b4989c647126f27715acc591c47133c2d`
- Runner: `ubuntu-24.04`, native `amd64` Kind node

## Result

The run is **INELIGIBLE / FAIL** for the frozen paired-control gate.  The
released fault and recovery scripts reached the MongoDB instance and the
security role was observable as revoked and then restored before the durability
check.  The independent frontend and official readiness path reached the
evaluation stage.  After deleting the MongoDB pod and waiting for a fresh pod,
the restored `admin` authentication/`readWrite@geo-db` invariant was not
observable, so the workflow failed closed with `RuntimeError: secure durability
failed`.  The cluster was torn down successfully.

The controller was deliberately stricter than the released injector: it did
not trust the injector's success text or exit status and retried until the
role state was observable.  This run therefore does not support a scientific
claim about agents or evaluator blind spots.

## Interpretation

This pinned AIOpsLab release cannot currently serve as the durable half of the
cross-system agent study.  The failure is a substrate/evaluator precondition,
not a model result.  The SREGym paired control remains a separate zero-model
pass; the cross-system study remains blocked and no model calls are authorized.

