"""Booking + lead store backing the agent's tools.

JSON-backed and deliberately simple so the demo runs with zero external
services. The method surface (availability / book / save lead / escalate) is
the integration seam: swap this class for one that talks to Google Calendar,
Calendly, a CRM, or a database, and the agent code above it does not change.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime, time, timedelta

from .config import BusinessConfig

_WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def _parse_hhmm(s: str) -> time:
    h, m = s.split(":")
    return time(int(h), int(m))


class Backend:
    def __init__(self, config: BusinessConfig, data_dir: str = "lead_agent_data", *, now: datetime | None = None):
        self.config = config
        self.data_dir = data_dir
        self._now = now  # injectable for deterministic tests/demos
        self._lock = threading.Lock()
        os.makedirs(data_dir, exist_ok=True)
        self._path = os.path.join(data_dir, f"{config.tenant_id}.json")
        self._state = self._load()

    # ---- persistence -------------------------------------------------
    def _load(self) -> dict:
        if os.path.exists(self._path):
            with open(self._path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"booked": {}, "leads": [], "escalations": []}

    def _save(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._state, f, indent=2)

    def now(self) -> datetime:
        return self._now or datetime.now()

    # ---- availability ------------------------------------------------
    def get_availability(self, date_from: str | None = None, date_to: str | None = None, limit: int = 8) -> list[dict]:
        start_day = _to_date(date_from) or self.now().date()
        horizon = self.now().date() + timedelta(days=self.config.booking_horizon_days)
        end_day = _to_date(date_to) or horizon
        if end_day > horizon:
            end_day = horizon

        slots: list[dict] = []
        day = start_day
        now = self.now()
        while day <= end_day and len(slots) < limit:
            hours = self.config.business_hours.get(_WEEKDAYS[day.weekday()])
            if hours:
                open_t, close_t = _parse_hhmm(hours[0]), _parse_hhmm(hours[1])
                cursor = datetime.combine(day, open_t)
                close_dt = datetime.combine(day, close_t)
                while cursor + timedelta(minutes=self.config.slot_minutes) <= close_dt:
                    slot_id = cursor.isoformat(timespec="minutes")
                    if cursor > now and slot_id not in self._state["booked"]:
                        slots.append({
                            "slot_id": slot_id,
                            "label": cursor.strftime("%a %b %d, %I:%M %p"),
                        })
                        if len(slots) >= limit:
                            break
                    cursor += timedelta(minutes=self.config.slot_minutes)
            day += timedelta(days=1)
        return slots

    # ---- mutations ---------------------------------------------------
    def book_appointment(self, slot_id: str, name: str, phone: str, service: str, notes: str = "") -> dict:
        with self._lock:
            if slot_id in self._state["booked"]:
                return {"ok": False, "error": "That slot was just taken. Please pick another."}
            try:
                dt = datetime.fromisoformat(slot_id)
            except ValueError:
                return {"ok": False, "error": "Invalid slot_id. Call get_availability and use a returned slot_id."}
            booking = {
                "slot_id": slot_id,
                "when": dt.strftime("%A %B %d at %I:%M %p"),
                "name": name,
                "phone": phone,
                "service": service,
                "notes": notes,
                "created_at": self.now().isoformat(timespec="seconds"),
            }
            self._state["booked"][slot_id] = booking
            self._save()
            return {"ok": True, "confirmation": booking}

    def save_lead(self, **fields) -> dict:
        with self._lock:
            fields["updated_at"] = self.now().isoformat(timespec="seconds")
            self._state["leads"].append(fields)
            self._save()
            return {"ok": True, "saved_fields": sorted(fields.keys())}

    def escalate(self, reason: str, summary: str) -> dict:
        with self._lock:
            entry = {"reason": reason, "summary": summary, "at": self.now().isoformat(timespec="seconds")}
            self._state["escalations"].append(entry)
            self._save()
            return {"ok": True, "message": "Flagged for human callback."}


def _to_date(s: str | None):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s).date()
    except ValueError:
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            return None
