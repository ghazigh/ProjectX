"""Reliable Agent — a reference implementation of a production-grade agentic loop.

Showcases the parts most demos skip: guardrails, evaluation, and full tracing.
"""

from .agent import ReliableAgent, AgentResult
from .trace import Tracer

__all__ = ["ReliableAgent", "AgentResult", "Tracer"]
