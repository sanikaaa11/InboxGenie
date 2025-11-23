# llm/model.py — FINAL STABLE VERSION

import os
import json
from typing import Optional
from dotenv import load_dotenv
import google.genai as genai

# -------------------------------------------------
# Load environment (.env)
# -------------------------------------------------
load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY missing in .env")

# Gemini Client
client = genai.Client(api_key=API_KEY)

# Default model
DEFAULT_MODEL = os.getenv("INBOXGENIE_MODEL", "gemini-2.0-flash")


# -------------------------------------------------
# Low-level model call
# -------------------------------------------------
def _call_model(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 512) -> str:
    """
    Raw call to the Gemini model.
    """
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"max_output_tokens": max_tokens},
    )

    try:
        return response.text.strip()
    except:
        return str(response)


# -------------------------------------------------
# COMPATIBILITY WRAPPER (for older agents)
# -------------------------------------------------
def call_llm(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 512) -> str:
    """
    Wrapper expected by older agent modules.
    Delegates to _call_model().
    """
    return _call_model(prompt, model=model, max_tokens=max_tokens)


# -------------------------------------------------
# Unified Email Decision
# -------------------------------------------------
def unified_email_decision(
    subject: str,
    body: str,
    sender: str,
    timezone: Optional[str] = None
) -> dict:

    prompt = f"""
You are InboxGenie. 
Analyze the email and OUTPUT ONLY valid JSON. 
NO text outside the JSON. NO explanations. NO commentary.

Email details:
- sender: {sender}
- subject: {subject}
- body: {body[:2000]}

You must decide:
1. should_reply → true/false
2. category → one of:
   "informational", "urgent", "spam", "follow-up", "personal", "other"
3. reply_text → short, polite, helpful (empty string if no reply)
4. schedule → null OR an object:
   {{
     "start_iso": "YYYY-MM-DDTHH:MM",
     "end_iso": "YYYY-MM-DDTHH:MM",
     "duration_minutes": number
   }}
5. notes → short explanation

RULES:
- DO NOT decline meetings unless sender themselves is declining.
- Assume the user is cooperative & available unless stated otherwise.
- Replies must be short, polite, neutral, and helpful.
- Only create schedule if email explicitly contains a date AND a time.
- If unsure → schedule must be null.
- Your output must be EXACTLY one JSON object.

Return ONLY this JSON object:
{{
  "should_reply": boolean,
  "category": "string",
  "reply_text": "string",
  "schedule": null or {{
        "start_iso": "YYYY-MM-DDTHH:MM",
        "end_iso": "YYYY-MM-DDTHH:MM",
        "duration_minutes": number
  }},
  "notes": "string"
}}
"""

    raw = _call_model(prompt)


    # Try to extract valid JSON safely
    try:
        start = raw.find("{")
        end = raw.rfind("}")
        json_str = raw[start:end + 1]
        data = json.loads(json_str)
    except Exception as e:
        return {
            "should_reply": False,
            "category": "informational",
            "reply_text": "",
            "schedule": None,
            "notes": f"parse_error: {e}, raw: {raw[:200]}"
        }

    # Normalize keys
    return {
        "should_reply": bool(data.get("should_reply", False)),
        "category": data.get("category", "informational"),
        "reply_text": data.get("reply_text", "") or "",
        "schedule": data.get("schedule", None),
        "notes": data.get("notes", "")
    }
