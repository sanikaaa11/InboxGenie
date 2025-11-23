# agents/task_agent.py

from llm.model import unified_email_decision
from tools.calendar_tool import create_event
from dateutil.parser import isoparse
from datetime import timedelta


def schedule_from_decision(message_id, subject, body, decision):
    """
    Safely schedules events ONLY if decision["schedule"] is valid.
    Prevents .get() errors when schedule is None.
    """

    schedule = decision.get("schedule")


    # No schedule → stop early
    if schedule is None:
        return None

    # If schedule is not dict → stop
    if not isinstance(schedule, dict):
        return None

    start_iso = schedule.get("start_iso")
    duration = schedule.get("duration_minutes", 60)
    end_iso = schedule.get("end_iso")

    # Must have proper ISO datetime
    if not start_iso or "T" not in start_iso:
        return None

    # Validate start time
    try:
        start_dt = isoparse(start_iso)
    except Exception:
        return None

    # Compute end time if missing
    if not end_iso:
        end_dt = start_dt + timedelta(minutes=duration)
        end_iso = end_dt.isoformat(timespec="seconds")

    # Call Google Calendar API
    try:
        event = create_event(
            summary=subject,
            start_iso=start_iso,
            end_iso=end_iso,
            description=body[:1000]
        )
        return event

    except Exception as e:
        print(" - Scheduling failed:", e)
        return None
