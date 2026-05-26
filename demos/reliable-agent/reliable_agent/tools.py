"""Tools the agent may call — and only these (allowlist).

`calculate` uses a safe AST evaluator, never `eval()`, so a tool argument can't
execute arbitrary code. `search_kb` grounds answers in a local knowledge base so
the agent answers from facts, not from its parametric memory.
"""

from __future__ import annotations

import ast
import json
import operator
import os
import re

# ---- calculate (safe arithmetic) -------------------------------------
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("unsupported expression")


def calculate(expression: str) -> dict:
    try:
        return {"result": _safe_eval(ast.parse(expression, mode="eval"))}
    except Exception as e:
        return {"error": f"could not evaluate '{expression}': {e}"}


# ---- search_kb (grounding) -------------------------------------------
_KB = None


def _load_kb() -> list[dict]:
    global _KB
    if _KB is None:
        path = os.path.join(os.path.dirname(__file__), "..", "data", "kb.json")
        with open(path, encoding="utf-8") as f:
            _KB = json.load(f)
    return _KB


def search_kb(query: str) -> dict:
    terms = set(re.findall(r"[a-z0-9]+", query.lower()))
    scored = []
    for entry in _load_kb():
        words = set(re.findall(r"[a-z0-9]+", (entry["title"] + " " + entry["content"]).lower()))
        score = len(terms & words)
        if score:
            scored.append((score, entry))
    scored.sort(key=lambda x: -x[0])
    results = [e for _, e in scored[:3]]
    return {"results": results or [{"note": "no matching policy found"}]}


# ---- registry + schemas ----------------------------------------------
REGISTRY = {"search_kb": search_kb, "calculate": calculate}

SCHEMAS = [
    {
        "name": "search_kb",
        "description": "Search the company knowledge base for policies and facts. Use this for any question about the company; answer only from what it returns.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "calculate",
        "description": "Evaluate an arithmetic expression (e.g. '3 * 4000'). Use for any math rather than computing it yourself.",
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    },
]
