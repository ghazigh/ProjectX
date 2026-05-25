"""Tool schemas exposed to the model, and dispatch into the backend.

Booking and lead capture are real side effects, so these run through an
explicit dispatch (not auto-executed) — that's the seam where a production
build adds confirmation gates, logging, and validation.
"""

from __future__ import annotations

import json

from .backend import Backend

TOOL_SCHEMAS = [
    {
        "name": "get_availability",
        "description": (
            "Get real open appointment slots. ALWAYS call this before offering or "
            "confirming any time — never invent availability. Returns a list of "
            "slots with slot_id and a human-readable label."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "date_from": {"type": "string", "description": "Earliest date, YYYY-MM-DD. Optional; defaults to today."},
                "date_to": {"type": "string", "description": "Latest date, YYYY-MM-DD. Optional."},
            },
            "required": [],
        },
    },
    {
        "name": "save_lead",
        "description": (
            "Save or update the lead's captured details and qualification status. "
            "Call this once you have the lead's name and contact info, even if they "
            "don't end up booking, so the business can follow up."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "phone": {"type": "string"},
                "email": {"type": "string"},
                "service": {"type": "string"},
                "urgency": {"type": "string"},
                "qualified": {"type": "boolean"},
                "notes": {"type": "string"},
            },
            "required": ["name"],
        },
    },
    {
        "name": "book_appointment",
        "description": (
            "Book a confirmed appointment. Only call after the lead has explicitly "
            "agreed to a specific slot_id returned by get_availability, and you have "
            "their name, phone, and the service."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "slot_id": {"type": "string", "description": "A slot_id returned by get_availability."},
                "name": {"type": "string"},
                "phone": {"type": "string"},
                "service": {"type": "string"},
                "notes": {"type": "string"},
            },
            "required": ["slot_id", "name", "phone", "service"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": (
            "Flag the conversation for a human callback — use when the request is "
            "out of scope, high-value/complex, an emergency, or the lead explicitly "
            "asks for a person."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {"type": "string"},
                "summary": {"type": "string", "description": "Short summary of the lead and what they need."},
            },
            "required": ["reason", "summary"],
        },
    },
]


def dispatch(name: str, tool_input: dict, backend: Backend) -> str:
    """Execute a tool call and return a JSON string result for the model."""
    try:
        if name == "get_availability":
            result = {"slots": backend.get_availability(tool_input.get("date_from"), tool_input.get("date_to"))}
        elif name == "save_lead":
            result = backend.save_lead(**tool_input)
        elif name == "book_appointment":
            result = backend.book_appointment(
                slot_id=tool_input["slot_id"],
                name=tool_input["name"],
                phone=tool_input["phone"],
                service=tool_input["service"],
                notes=tool_input.get("notes", ""),
            )
        elif name == "escalate_to_human":
            result = backend.escalate(tool_input.get("reason", ""), tool_input.get("summary", ""))
        else:
            result = {"ok": False, "error": f"Unknown tool: {name}"}
    except KeyError as e:
        result = {"ok": False, "error": f"Missing required field: {e}"}
    except Exception as e:  # surfaced back to the model so it can recover
        result = {"ok": False, "error": str(e)}
    return json.dumps(result)
