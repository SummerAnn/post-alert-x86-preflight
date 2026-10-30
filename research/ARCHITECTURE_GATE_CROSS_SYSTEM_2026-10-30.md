# Cross-system agent-study architecture gate — 2026-10-30

Status: **blocked before model calls**.

The local Docker Desktop Kubernetes cluster has one node, `arm64`. The frozen
cross-system preregistration permits the earlier locally rebuilt AIOpsLab ARM64
image as feasibility evidence, but explicitly forbids silently pooling that
image with native-image confirmatory cells. The published AIOpsLab
`yg397/media-frontend:xenial` image was the source of the prior ARM startup
failure, so this host cannot satisfy the native-image gate.

SREGym itself is runnable locally, but launching only its cells would no longer
be the preregistered two-system study. No model or provider calls were made.
The preflight now fails closed unless at least one ready `amd64` Kubernetes node
is available.

The next valid action is either:

1. obtain an approved x86/amd64 Kubernetes substrate and rerun the no-call
   preflight; or
2. stop with the completed two-system zero-model evaluator result and do not
   make an agent-behavior claim.

No local ARM emulation or image substitution should be used for the
confirmatory study.
