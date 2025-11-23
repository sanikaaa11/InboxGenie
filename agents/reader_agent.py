# agents/reader_agent.py

from tools.gmail_tool import list_emails
from agents.decision_agent import analyze_email
from tools.gmail_tool import ensure_label_exists

def list_and_analyze(limit=8):
    emails = list_emails(limit=limit)
    output = []

    drafted_label_id = ensure_label_exists("InboxGenie / Drafted")

    for e in emails:

        # NEW: skip emails already drafted
        if drafted_label_id in e.get("labelIds", []):
            e["decision"] = {"should_reply": False}
            continue

        subj = e.get("subject", "")
        body = e.get("body", "")
        sender = e.get("sender", "")

        decision = analyze_email(subj, body, sender)
        e["decision"] = decision
        output.append(e)

    return output
