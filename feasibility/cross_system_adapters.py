"""Dry-run adapters for the two released agent interfaces.

This module deliberately stops at message construction.  It does not import a
provider SDK, contact a provider, start a Kubernetes problem, or expose the
independent oracle.  A later execution driver may use the returned messages,
but it must opt into that separately and record the provider's resolved model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from cross_system_prompts import condition_suffix


MODEL_SPECS: dict[str, dict[str, object]] = {
    "gpt-6.1-sol": {
        "provider": "openai",
        "reasoning_effort": "medium",
        "temperature": 1.0,
    },
    "claude-sonnet-4-6": {
        "provider": "anthropic",
        "temperature": 1.0,
    },
}


@dataclass(frozen=True)
class PreparedEpisode:
    """The agent-visible context and audit metadata for one episode."""

    system: str
    model: str
    messages: tuple[dict[str, str], ...]
    condition: str
    visible_service_label: str


def model_spec(model: str) -> dict[str, object]:
    """Return a copy of a frozen model spec; fail closed on substitutions."""
    if model not in MODEL_SPECS:
        raise ValueError(f"model is not frozen in the preregistration: {model}")
    return dict(MODEL_SPECS[model])


def _append_condition(task_text: str, *, condition: str, requirement: str) -> str:
    """Append only the preregistered condition suffix to native task text."""
    return task_text.rstrip() + condition_suffix(condition=condition, requirement=requirement)


def _stringify_apis(apis: Mapping[str, str]) -> str:
    return "\n\n".join(f"{name}\n{description}" for name, description in apis.items())


def prepare_aiopslab(
    *,
    problem_desc: str,
    instructions: str,
    apis: Mapping[str, str],
    model: str,
    condition: str,
    requirement: str,
    docs_template: str,
    service_label: str = "URL-shortener service",
) -> PreparedEpisode:
    """Prepare an AIOpsLab-native ReAct conversation without starting it.

    ``docs_template`` must be the released ``clients.utils.templates.DOCS``
    value, supplied by the execution driver after it pins the source commit.
    The hidden independent probes are not accepted as an argument.
    """
    model_spec(model)
    if not isinstance(problem_desc, str) or not isinstance(instructions, str):
        raise TypeError("released task text must be strings")
    if not apis or not all(isinstance(k, str) and isinstance(v, str) for k, v in apis.items()):
        raise ValueError("released API map is empty or malformed")
    system_text = docs_template.format(
        prob_desc=problem_desc,
        telemetry_apis=_stringify_apis({k: v for k, v in apis.items() if "exec_shell" not in k and "submit" not in k}),
        shell_api=_stringify_apis({k: v for k, v in apis.items() if "exec_shell" in k}),
        submit_api=_stringify_apis({k: v for k, v in apis.items() if "submit" in k}),
    )
    task_text = _append_condition(instructions, condition=condition, requirement=requirement)
    return PreparedEpisode(
        system="aiopslab",
        model=model,
        messages=(
            {"role": "system", "content": system_text},
            {"role": "user", "content": task_text},
        ),
        condition=condition,
        visible_service_label=service_label,
    )


def prepare_sregym(
    *,
    system_text: str,
    task_text: str,
    model: str,
    condition: str,
    requirement: str,
    service_label: str = "recommendation service",
) -> PreparedEpisode:
    """Prepare the SREGym mini-SRE conversation without contacting a model.

    ``system_text`` and ``task_text`` are produced by SREGym's released
    ``mini.system_text`` and ``mini.instance_text`` functions.  The adapter
    only appends the frozen condition suffix; it does not add oracle results or
    evaluator implementation details.
    """
    model_spec(model)
    if not isinstance(system_text, str) or not isinstance(task_text, str):
        raise TypeError("released SREGym prompt text must be strings")
    return PreparedEpisode(
        system="sregym",
        model=model,
        messages=(
            {"role": "system", "content": system_text},
            {"role": "user", "content": _append_condition(task_text, condition=condition, requirement=requirement)},
        ),
        condition=condition,
        visible_service_label=service_label,
    )


def validate_prepared_episode(episode: PreparedEpisode, *, requirement: str) -> None:
    """Check the non-leakage and frozen-model properties before execution."""
    model_spec(episode.model)
    if episode.condition not in {"availability_only_alert", "security_preservation_contract"}:
        raise ValueError(f"unknown condition: {episode.condition}")
    joined = "\n".join(message["content"] for message in episode.messages)
    if episode.condition == "availability_only_alert":
        for forbidden in ("security", "tls", "psa", "restricted", "capability", "policy"):
            if forbidden in joined.casefold():
                raise ValueError(f"availability prompt leaks forbidden term: {forbidden}")
        if requirement.casefold() in joined.casefold():
            raise ValueError("availability prompt leaks the preservation requirement")
    else:
        if requirement not in joined:
            raise ValueError("preservation requirement is missing from contract prompt")


def dry_run_summary(episode: PreparedEpisode, *, requirement: str) -> dict[str, Any]:
    """Return safe metadata for logs; never include credentials or hidden probes."""
    validate_prepared_episode(episode, requirement=requirement)
    return {
        "dry_run": True,
        "system": episode.system,
        "requested_model": episode.model,
        "condition": episode.condition,
        "visible_service_label": episode.visible_service_label,
        "message_roles": [message["role"] for message in episode.messages],
        "message_chars": [len(message["content"]) for message in episode.messages],
        "provider_requests": 0,
        "model_calls": 0,
    }
