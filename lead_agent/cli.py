"""Demo runner for the lead agent.

Interactive mode (you play the inbound lead):
    python -m lead_agent.cli --config configs/sample_home_services.json

Scenario replay (deterministic — great for recording an outbound demo video):
    python -m lead_agent.cli --config configs/sample_home_services.json \\
        --scenario configs/sample_scenario.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime

import anthropic

from .agent import LeadAgent
from .backend import Backend
from .config import load_config


def _print_tools(turn) -> None:
    for ev in turn.tool_events:
        print(f"    \033[2m[tool] {ev.name}({json.dumps(ev.input)}) -> {ev.result}\033[0m")


def run_scenario(agent: LeadAgent, messages: list[str]) -> None:
    print(f"\n=== Scenario demo: {agent.config.name} ===\n")
    for msg in messages:
        print(f"Lead:  {msg}")
        turn = agent.respond(msg)
        _print_tools(turn)
        print(f"Agent: {turn.reply}\n")


def run_interactive(agent: LeadAgent) -> None:
    print(f"\n=== {agent.config.name} — lead chat (Ctrl-C or 'quit' to exit) ===")
    if agent.config.greeting:
        print(f"Agent: {agent.config.greeting}\n")
    while True:
        try:
            msg = input("Lead:  ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if msg.lower() in {"quit", "exit"}:
            break
        if not msg:
            continue
        turn = agent.respond(msg)
        _print_tools(turn)
        print(f"Agent: {turn.reply}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lead-response & booking agent demo.")
    parser.add_argument("--config", "-c", required=True, help="Path to a business config JSON.")
    parser.add_argument("--scenario", "-s", default=None, help="Path to a scenario JSON (list of lead messages) for deterministic replay.")
    parser.add_argument("--model", "-m", default=None, help="Override the model.")
    parser.add_argument("--data-dir", "-d", default="lead_agent_data", help="Where to persist bookings/leads.")
    parser.add_argument("--fixed-date", default=None, help="Pin 'now' (YYYY-MM-DD) for reproducible demos.")
    args = parser.parse_args(argv)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key.", file=sys.stderr)
        return 1

    config = load_config(args.config)
    now = None
    if args.fixed_date:
        now = datetime.fromisoformat(args.fixed_date + "T09:00:00")
    backend = Backend(config, data_dir=args.data_dir, now=now)
    kwargs = {"model": args.model} if args.model else {}
    agent = LeadAgent(config, backend, **kwargs)

    try:
        if args.scenario:
            with open(args.scenario, "r", encoding="utf-8") as f:
                messages = json.load(f)
            run_scenario(agent, messages)
        else:
            run_interactive(agent)
    except anthropic.AuthenticationError:
        print("Error: invalid ANTHROPIC_API_KEY.", file=sys.stderr)
        return 1
    except anthropic.APIError as e:
        print(f"API error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
