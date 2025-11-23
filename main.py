# main.py
import json
from agents.reader_agent import list_and_analyze
from agents.reply_agent import draft_reply_using_decision
from agents.categorizer_agent import apply_label_from_decision
from agents.task_agent import schedule_from_decision
from tools.processing_memory import load_memory, mark_processed   # ✅ NEW

BLOCKED_FILE = "blocked_senders.json"

def load_blocked():
    try:
        with open(BLOCKED_FILE) as f:
            return set(json.load(f).get("blocked", []))
    except Exception:
        return set()

def main():
    print("\n=== InboxGenie Smart Orchestrator ===\n")

    blocked = load_blocked()
    processed = load_memory()    # ✅ Load memory of already-processed emails

    emails = list_and_analyze(limit=8)

    for e in emails:
        sender = e.get("sender", "")
        subject = e.get("subject", "")
        body = e.get("body", "")
        mid = e.get("id")
        decision = e.get("decision", {})

        print(f"\n📧 From: {sender}")
        print("Subject:", subject)

        # ------------------------------------------------
        # 0. Skip if already processed
        # ------------------------------------------------
        if mid in processed:
            print(" - Skipped (already processed before)")
            continue

        # ------------------------------------------------
        # 1. Blocklist check
        # ------------------------------------------------
        if any(b.lower() in sender.lower() for b in blocked):
            print(" - Skipped (blocked)")
            mark_processed(mid)      # still mark as processed
            continue

        # ------------------------------------------------
        # 2. Apply Label
        # ------------------------------------------------
        try:
            apply_label_from_decision(mid, decision)
            print(" - Label applied:", decision.get("category"))
        except Exception as ex:
            print(" - Labeling failed:", ex)

        # ------------------------------------------------
        # 3. Reply (Draft Only)
        # ------------------------------------------------
        if decision.get("should_reply"):
            print(" - Decided: reply needed → drafting...")

            try:
                draft = draft_reply_using_decision(mid, subject, body, decision)
                draft_id = draft.get("draft_id") if isinstance(draft, dict) else None

                if draft.get("skipped"):
                    print("   Draft already existed → skipped")
                else:
                    print("   Draft created. id:", draft_id)

            except Exception as ex:
                print("   Draft creation failed:", ex)

        else:
            print(" - Decided: no reply needed")

        # ------------------------------------------------
        # 4. Scheduling
        # ------------------------------------------------
        try:
            ev = schedule_from_decision(mid, subject, body, decision)

            if ev is None:
                print(" - No scheduling info found.")
            else:
                link = ev.get("htmlLink") if isinstance(ev, dict) else None
                if link:
                    print(" - Calendar event created:", link)
                else:
                    print(" - Calendar event created (no link returned)")

        except Exception as ex:
            print(" - Scheduling failed:", ex)

        # ------------------------------------------------
        # 5. Mark email as processed (FINAL STEP)
        # ------------------------------------------------
        mark_processed(mid)

if __name__ == "__main__":
    main()
