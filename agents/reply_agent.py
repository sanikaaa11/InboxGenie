# agents/reply_agent.py — FINAL SAFE VERSION

from tools.gmail_tool import create_draft_if_not_exists

def draft_reply_using_decision(message_id, subject, body, decision):
    """
    Creates a draft ONLY if one does NOT already exist for the thread.
    """

    reply_text = decision.get("reply_text", "").strip()
    if not reply_text:
        return {"draft_id": None, "skipped": True}

    # Create OR skip if duplicate
    result = create_draft_if_not_exists(message_id, reply_text)

    return {
        "draft_id": result.get("draft_id"),
        "skipped": (result.get("status") == "exists")
    }
