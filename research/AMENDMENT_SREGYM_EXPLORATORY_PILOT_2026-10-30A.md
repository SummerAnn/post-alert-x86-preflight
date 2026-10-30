# Erratum A: accessible GPT model for the SREGym exploratory pilot — 2026-10-30

The originally frozen exploratory GPT identifier, `gpt-6.1-sol`, is not
enabled for the configured OpenAI project. A read-only model listing verified
that the project exposes `gpt-6-luna` and that the Anthropic key exposes the
frozen `claude-sonnet-4-6`.

Before any successful model response, the exploratory pilot therefore changes
only the GPT identifier to `gpt-6-luna`. The four-cell matrix, prompts, tools,
feedback conditions, turn/checkpoint caps, hidden-oracle separation, and
cleanup rules are unchanged. The resolved identifier is recorded in every
cell. This remains a feasibility observation, not a confirmatory or broad
model claim; if the smaller GPT model is inadequate, that is reported as a
pilot boundary rather than treated as evidence about the intervention.

