import json
import os

MEM_FILE = "processed_emails.json"

def load_memory():
    if not os.path.exists(MEM_FILE):
        return set()
    try:
        with open(MEM_FILE, "r") as f:
            data = json.load(f)
            return set(data.get("processed_ids", []))
    except:
        return set()

def save_memory(processed_ids):
    with open(MEM_FILE, "w") as f:
        json.dump({"processed_ids": list(processed_ids)}, f, indent=4)

def mark_processed(email_id):
    mem = load_memory()
    mem.add(email_id)
    save_memory(mem)
