# agents/decision_agent.py — FINAL STABLE VERSION
from llm.model import unified_email_decision
import json

def analyze_email(subject: str, body: str, sender: str) -> dict:
    """
    Calls the unified LLM analyzer and ensures clean return structure.
    """

    try:
        data = unified_email_decision(subject=subject, body=body, sender=sender)

        # Normalize and enforce valid keys
        return {
            "should_reply": bool(data.get("should_reply", False)),
            "category": data.get("category", "informational"),
            "reply_text": data.get("reply_text", "") or "",
            "schedule": data.get("schedule", None),
            "notes": data.get("notes", "")
        }

    except Exception as e:
        # fallback safe output
        return {
            "should_reply": False,
            "category": "informational",
            "reply_text": "",
            "schedule": None,
            "notes": f"decision_agent_error: {e}"
        }
