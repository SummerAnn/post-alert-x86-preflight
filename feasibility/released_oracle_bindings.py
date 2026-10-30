"""Bindings to the released availability predicates.

Imports are intentionally deferred.  The local development environment does
not contain all benchmark dependencies, and importing this module must never
silently substitute a reimplemented evaluator.
"""

from __future__ import annotations

from typing import Any


def aiopslab_availability_checkpoint(task: Any, *, timeout: float | None = None) -> bool:
    """Invoke AIOpsLab's released mitigation health helper read-only.

    ``MitigationTask.wait_until_pods_healthy`` is the same predicate used by
    the released mitigation evaluator for the selected TLS task.  The adapter
    does not call ``submit`` and does not set the task's solution or results.
    """
    checker = getattr(task, "wait_until_pods_healthy", None)
    namespace = getattr(task, "namespace", None)
    if not callable(checker) or not isinstance(namespace, str) or not namespace:
        raise RuntimeError("AIOpsLab task is not a released mitigation task")
    result = checker(namespace, timeout=timeout) if timeout is not None else checker(namespace)
    if not isinstance(result, bool):
        raise RuntimeError("AIOpsLab health predicate returned a non-boolean result")
    return result


def sregym_availability_checkpoint(oracle: Any) -> bool:
    """Invoke SREGym's released ``DeploymentReadinessOracle.evaluate``.

    The caller must construct the released oracle for the live problem.  This
    binding only reads its result and returns the official success bit; it does
    not call the conductor's submit endpoint or advance a stage.
    """
    evaluator = getattr(oracle, "evaluate", None)
    if not callable(evaluator):
        raise RuntimeError("SREGym object has no released evaluate method")
    result = evaluator()
    if not isinstance(result, dict) or not isinstance(result.get("success"), bool):
        raise RuntimeError("SREGym readiness oracle returned a malformed result")
    return result["success"]

