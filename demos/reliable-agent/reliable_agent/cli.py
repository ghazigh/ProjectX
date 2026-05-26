"""CLI: run a query, or run the eval suite.

    python -m reliable_agent.cli run "What's the fee on a card transaction?"
    python -m reliable_agent.cli eval
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import anthropic

from .agent import ReliableAgent
from .evals import load_cases, report, run_evals

_CASES = os.path.join(os.path.dirname(__file__), "..", "evals", "cases.jsonl")


def _need_key() -> bool:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        return True
    return False


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Reliable Agent — production-grade agentic loop.")
    sub = p.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("run", help="Answer a single query.")
    pr.add_argument("query")
    pr.add_argument("--trace", help="Write the full trace to this JSONL path.")
    pr.add_argument("--model", default=None)
    pe = sub.add_parser("eval", help="Run the evaluation suite.")
    pe.add_argument("--cases", default=_CASES)
    pe.add_argument("--model", default=None)
    args = p.parse_args(argv)

    if _need_key():
        return 1
    kwargs = {"model": args.model} if getattr(args, "model", None) else {}
    agent = ReliableAgent(**kwargs)

    try:
        if args.cmd == "run":
            result = agent.run(args.query)
            print(result.answer)
            print(f"\n[tools used: {result.tools_used or 'none'} | {json.dumps(result.tracer.summary())}]")
            if args.trace:
                result.tracer.write(args.trace)
                print(f"[trace written to {args.trace}]")
        elif args.cmd == "eval":
            cases = load_cases(args.cases)
            results = run_evals(lambda q: (lambda r: (r.answer, r.tools_used))(agent.run(q)), cases)
            print(report(results))
            return 0 if all(r.passed for r in results) else 2
    except anthropic.AuthenticationError:
        print("Error: invalid ANTHROPIC_API_KEY.", file=sys.stderr)
        return 1
    except anthropic.APIError as e:
        print(f"API error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
