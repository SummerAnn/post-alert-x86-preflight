# Secret-rotation zero-model gate — 2026-10-30

Status: **infrastructure-incomplete; no scientific result**.

The released `SecretRotationStaleEnvCredentialsAstronomyShop` task was
instantiated and its Helm deployment started on the local Docker Desktop
Kubernetes cluster. The first attempt failed immediately because the existing
Helm binary was not on `PATH`; this was corrected by using the existing
`/private/tmp/darwin-arm64/helm` binary. The second attempt successfully
registered the chart repositories and rendered the Astronomy Shop release, but
the cluster spent more than ten minutes pulling first-use images. Most pods
remained in `ContainerCreating` or `Init:0/1`, with no new event beyond a
long-running pull of `ghcr.io/sregym/locust-exporter`.

The run was interrupted before baseline readiness, fault injection, or either
truth-table arm. No model calls were made and no result JSON was written. The
partially deployed `astronomy-shop` namespace was deleted and confirmed as
cleanup. This is a substrate/setup block, not evidence for or against the
temporal-recovery candidate.

The source-level candidate remains eligible for a later gate on a host with the
images cached or a faster native SREGym substrate. No agent experiment is
authorized from this incomplete run.

