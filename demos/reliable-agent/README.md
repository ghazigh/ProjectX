# Reliable Agent

A small reference implementation of a **production-grade agentic loop** — the
parts most agent demos skip. The agentic loop itself is ~30 lines; the value is
the reliability scaffolding around it:

- **Guardrails** — input validation, a prompt-injection heuristic, PII redaction, and output validation.
- **Tool allowlist** — the agent can only execute registered tools; anything else is refused and logged. `calculate` uses a safe AST evaluator (never `eval()`).
- **Grounding** — the agent answers from a knowledge base via a tool, not from memory, and declines what it can't ground.
- **Tracing** — every step (model call, tool call, guardrail decision) is recorded; export the full trace as JSONL.
- **Evaluation** — a labelled test set and a scorer, so quality is *measured*, not asserted.

This is the discipline that takes an agent from "works in the demo" to "safe to
run." It's deliberately dependency-light (just the Anthropic SDK) so the ideas
are easy to read.

## Run it

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

# Answer a question (grounded in the knowledge base), and see the trace summary:
python -m reliable_agent.cli run "If I send 3 transfers of $4000, will I exceed my daily limit?" --trace trace.jsonl

# Run the evaluation suite:
python -m reliable_agent.cli eval
```

The example domain is a payments-app support assistant (`data/kb.json`) — swap
the knowledge base, tools, and system prompt for your own use case.

## How it works

```
query → [guardrail: input] → agent loop:
            model → (tool_use? → allowlist check → execute → trace → loop)
                  → final answer → [guardrail: output] → result + trace
```

- `reliable_agent/agent.py` — the orchestrator (loop + guardrails + allowlist + tracing)
- `reliable_agent/guardrails.py` — input/output checks, redaction
- `reliable_agent/tools.py` — the tool registry, schemas, safe calculator, KB search
- `reliable_agent/trace.py` — structured tracing
- `reliable_agent/evals.py` — test cases + scorer (`answer_fn` injected, so it's unit-testable)
- `evals/cases.jsonl` — the labelled test set

## Why it matters

Most agentic AI projects stall in the gap between a prototype and a system you
can trust. Evals tell you whether a change helped or hurt; guardrails stop the
agent doing something wrong; tracing lets you debug it at 2 a.m. Building these
in from the start is the difference between a demo and production.

## Tests

The non-model components (guardrails, tools, tracing, the eval scorer) are
deterministic and unit-tested in `tests/` — run `python -m pytest` or
`python tests/test_core.py`.
