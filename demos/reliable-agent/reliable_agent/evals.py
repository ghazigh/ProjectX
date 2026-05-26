"""Evaluation harness.

"How do you know it works?" is the question every serious buyer asks. This runs
the agent over a labelled test set and scores it — so quality is measured, not
asserted. `answer_fn` is injected, so the scorer is testable without the API.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Callable

_REFUSAL_MARKERS = ("can't", "cannot", "not able", "don't have", "do not have",
                    "decline", "outside", "unrelated", "sorry", "support")


@dataclass
class Case:
    id: str
    query: str
    expect_contains: list[str] = field(default_factory=list)
    expect_tools: list[str] = field(default_factory=list)
    must_refuse: bool = False


@dataclass
class CaseResult:
    id: str
    passed: bool
    checks: list[tuple[str, bool]]
    answer: str


def load_cases(path: str) -> list[Case]:
    cases = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                cases.append(Case(**json.loads(line)))
    return cases


def score_case(case: Case, answer: str, tools_used: list[str]) -> CaseResult:
    a = answer.lower()
    checks: list[tuple[str, bool]] = []
    for s in case.expect_contains:
        checks.append((f"contains '{s}'", s.lower() in a))
    for t in case.expect_tools:
        checks.append((f"used tool '{t}'", t in tools_used))
    if case.must_refuse:
        checks.append(("declined out-of-scope", any(m in a for m in _REFUSAL_MARKERS)))
    passed = all(ok for _, ok in checks) if checks else False
    return CaseResult(case.id, passed, checks, answer)


def run_evals(answer_fn: Callable[[str], tuple[str, list[str]]], cases: list[Case]) -> list[CaseResult]:
    """answer_fn(query) -> (answer_text, tools_used)."""
    results = []
    for case in cases:
        answer, tools_used = answer_fn(case.query)
        results.append(score_case(case, answer, tools_used))
    return results


def report(results: list[CaseResult]) -> str:
    passed = sum(1 for r in results if r.passed)
    lines = [f"Eval: {passed}/{len(results)} cases passed ({round(100 * passed / max(len(results),1))}%)", ""]
    for r in results:
        lines.append(f"[{'PASS' if r.passed else 'FAIL'}] {r.id}")
        for label, ok in r.checks:
            lines.append(f"    {'✓' if ok else '✗'} {label}")
    return "\n".join(lines)
