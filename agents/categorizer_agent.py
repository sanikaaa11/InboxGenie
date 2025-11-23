# agents/categorizer_agent.py
from tools.gmail_tool import ensure_label_exists, add_label_to_message

LABEL_PREFIX = "InboxGenie / "

def apply_label_from_decision(message_id: str, decision: dict):
    category = decision.get("category", "other")
    label_name = LABEL_PREFIX + category.capitalize()
    label_id = ensure_label_exists(label_name)
    return add_label_to_message(message_id, label_id)
