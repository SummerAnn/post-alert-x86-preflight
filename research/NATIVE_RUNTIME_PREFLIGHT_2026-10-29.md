# Native runtime preflight — 2026-10-29

Status: **blocked before model calls**. This is an infrastructure gate, not a
study result.

## Local machine

- Docker Desktop Kubernetes node: `arm64`.
- AIOpsLab's key application images (`yg397/media-frontend:xenial` and
  `deathstarbench/social-network-microservices:latest`) are single-architecture
  manifests and are not a native ARM64 execution path.
- MongoDB, Redis, and Memcached dependency images do publish ARM64 variants.
- The prior zero-model AIOpsLab control used a locally rebuilt ARM64 application
  image. The frozen study explicitly does not pool that substituted image with
  native-image confirmatory cells.

Running the released application under x86 emulation would violate the frozen
native-image requirement and could alter startup timing or failure behavior.

## DSI read-only check

The configured `fe.ds` host is reachable and reports `x86_64`, but the login
host has no `docker` or `kubectl`. It has `podman`, but a read-only `podman
info` fails because the cluster user namespace mapping lacks the required
`newgidmap` setup. No remote files, jobs, containers, or model calls were
created.

An allocated `dev` node (`g009`) was also checked with short, read-only Slurm
probes. It is `x86_64` and has Docker 29.9.2, Podman 4.9.3, and Apptainer, but
the account is not in the `docker` group (`/var/run/docker.sock` is
`root:docker`), Podman fails with the same `newgidmap`/sub-ID restriction even
when pointed at temporary user-owned storage, and no `kubectl`, Kind, or
Minikube installation or user kubeconfig exists. Slurm's configuration reports
no container plugin (`JobContainerType = (null)`). Apptainer therefore cannot
stand in for the released Docker/Kubernetes orchestration without changing the
system under test.

## Gate decision

The cross-system agent study must not start on the local ARM cluster or the DSI
login/compute environment as currently provisioned. A native x86 Kubernetes /
container runtime with account access is required first (for example, Docker
group access plus Kind, or an existing kubeconfig). The provider keys and exact
model IDs are valid, and both released agent paths now import in the isolated
Python 3.12 environment, but those facts do not waive the native-runtime gate.

