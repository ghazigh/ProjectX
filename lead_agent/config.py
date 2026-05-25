"""Business configuration — the per-tenant 're-skin' layer.

Everything that makes the agent specific to one business lives in a JSON file.
Onboarding a new client = writing one config. This is what turns a bespoke
build into a repeatable product.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class Service:
    name: str
    description: str = ""


@dataclass
class BusinessConfig:
    tenant_id: str
    name: str
    industry: str
    services: list[Service] = field(default_factory=list)
    service_area: str = ""
    timezone: str = "UTC"
    # day name (lowercase) -> ["HH:MM", "HH:MM"] or null/None when closed
    business_hours: dict[str, list[str] | None] = field(default_factory=dict)
    slot_minutes: int = 60
    booking_horizon_days: int = 14
    required_fields: list[str] = field(default_factory=lambda: ["name", "phone", "service"])
    qualifying_questions: list[str] = field(default_factory=list)
    escalation_rules: list[str] = field(default_factory=list)
    tone: str = "warm, concise, professional"
    greeting: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "BusinessConfig":
        services = [Service(**s) if isinstance(s, dict) else Service(name=str(s)) for s in d.get("services", [])]
        known = {
            "tenant_id", "name", "industry", "service_area", "timezone",
            "business_hours", "slot_minutes", "booking_horizon_days",
            "required_fields", "qualifying_questions", "escalation_rules",
            "tone", "greeting",
        }
        kwargs = {k: v for k, v in d.items() if k in known}
        kwargs["services"] = services
        return cls(**kwargs)


def load_config(path: str) -> BusinessConfig:
    with open(path, "r", encoding="utf-8") as f:
        return BusinessConfig.from_dict(json.load(f))
