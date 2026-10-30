# GitHub x86 preflight — 2026-10-29

The repository now contains a manual-only, no-call workflow at
`.github/workflows/native-x86-preflight.yml`. It is intended to be run on a
standard public-repository GitHub Actions `ubuntu-24.04` runner, which is an
x86 runner with Docker access. The workflow:

1. asserts `x86_64` and Docker access;
2. installs and hashes the pinned Kind binary;
3. checks out the exact pinned AIOpsLab and SREGym commits;
4. verifies the two AIOpsLab application manifests support `linux/amd64`;
5. creates a disposable x86 Kind cluster using the released AIOpsLab config;
6. checks the Kubernetes node architecture; and
7. tears the cluster down even when a prior step fails.

It has no provider secrets, does not read model keys, and cannot launch model
episodes. It is a runtime feasibility check only. Standard GitHub runners have
less disk/CPU than the recommended full SREGym setup, so a passing preflight
would establish a possible free route, not guarantee that the full campaign
fits.
