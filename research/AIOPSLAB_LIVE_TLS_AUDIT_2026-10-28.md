# AIOpsLab live TLS recovery audit

**Date:** 2026-10-28 (local time)  
**Status:** zero-model live feasibility result; not a model result  
**Model/API calls:** 0  
**AIOpsLab source:** public checkout at `/private/tmp/aiopslab-live`, commit `576c3f080c7ae2459a972afd4a2f8d5f01828430`  
**Official evaluator/injector:** unchanged `auth_miss_mongodb` path and unchanged recovery path  
**Cluster:** disposable standard `kind` ARM64 node, Kubernetes v1.31.2; release `social-network`, namespace `aiopslab`

## What was verified

The custom AIOpsLab ARM node image could boot the chart but crashed the released
`yg397/media-frontend:xenial` image in OpenResty/LuaJIT before a healthy baseline.
A locally rebuilt ARM64 equivalent was stable in Docker and on a standard kind
node. The rebuild was used only to make the released application runnable; no
benchmark code or official evaluator was changed. The custom-node failure was
infrastructure, not evidence.

On the standard disposable cluster, the official chart reached **27/27 pods
Running** before and after the fault/recovery sequence. The throwaway
`mongodb-tls` secret was created because the released chart always mounts that
secret even when its default TLS mode is disabled.

The official injector was then called directly:

```text
ApplicationFaultInjector.inject_auth_miss_mongodb(["url-shorten-mongodb"])
```

The rendered target configuration became:

```yaml
net:
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/tls/tls.pem
```

The real Mongo shell probe `db.adminCommand({hello:1})` over the normal local
connection failed with a TLS-required network error. This confirms that the
fault changed live behavior rather than only a file or Helm value.

The official recovery was then called directly:

```text
ApplicationFaultInjector.recover_auth_miss_mongodb(["url-shorten-mongodb"])
```

After the recovery Helm upgrade and pod restart:

* all **27/27** pods were Running and Ready;
* the target configuration was `tls.mode: disabled`;
* the same Mongo shell probe returned `1`.

Thus the released mitigation criterion (`wait_until_pods_healthy`) would report
success after the recovery, while an independent security probe can see that
transport security is disabled and unauthenticated plaintext Mongo access is
accepted.

## What this does and does not establish

This is a **benchmark/evaluator audit finding**, not yet a paper result about
agents. It establishes a reproducible mismatch in the released AIOpsLab TLS
task:

* official success checks pod health only;
* official recovery restores availability by returning TLS to `disabled`;
* the default Mongo template contains no `authorization: enabled` setting;
* a direct capability probe distinguishes healthy service state from security
  posture.

The security weakness is partly a **baseline design limitation** of the
released chart, not proof that an agent created new compromise. Therefore this
observation must not be presented as a causal agent-recovery result. It is a
validated reason to add an independent capability/preservation oracle before
any model pilot, and to compare at least one independent benchmark/system before
claiming a general phenomenon.

## Remaining gate

No model call is authorized by this audit. The next legitimate step is a
zero-model paired-state test with a security-preserving TLS repair versus the
official availability-first recovery, using the same external oracle and fresh
process/restart checks. If the safe repair cannot be implemented without
changing the official task or if the independent oracle cannot distinguish the
states, this branch closes as an evaluator audit rather than a paper claim.
