# tools/gmail_tool.py
import base64
import html
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import List, Dict

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.labels",
]

TOKEN_PATH = "token.json"

def _get_creds():
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError("token.json not found. Run OAuth first.")
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    return creds

def get_gmail_service():
    creds = _get_creds()
    return build("gmail", "v1", credentials=creds)

def _decode(data: str) -> str:
    return base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="ignore")

def _get_body_from_msg(msg):
    payload = msg.get("payload", {})

    # simple case
    if payload.get("body", {}).get("data"):
        return _decode(payload["body"]["data"])

    # multipart
    for part in payload.get("parts", []):
        mime = part.get("mimeType", "")
        if mime == "text/plain" and part.get("body", {}).get("data"):
            return _decode(part["body"]["data"])
        if mime == "text/html" and part.get("body", {}).get("data"):
            return html.unescape(_decode(part["body"]["data"]))
    return ""

def list_emails(limit: int = 5) -> List[Dict]:
    svc = get_gmail_service()
    res = svc.users().messages().list(
        userId="me", labelIds=["INBOX"], maxResults=limit
    ).execute()

    msgs = res.get("messages", [])
    out = []

    for m in msgs:
        md = svc.users().messages().get(
            userId="me", id=m["id"], format="full"
        ).execute()

        headers = md.get("payload", {}).get("headers", [])
        sender, subject = "", ""

        for h in headers:
            if h.get("name") == "From":
                sender = h.get("value")
            if h.get("name") == "Subject":
                subject = h.get("value")

        body = _get_body_from_msg(md)

        out.append({
            "id": m["id"],
            "subject": subject or "",
            "sender": sender or "",
            "body": body or "",
            "snippet": md.get("snippet", "")
        })

    return out


# ----------------------------------------------------------
#  SAFE VERSION — prevents duplicate drafts
# ----------------------------------------------------------
def create_draft_if_not_exists(email_id: str, reply_text: str):
    svc = get_gmail_service()

    # 1. Check existing drafts
    drafts = svc.users().drafts().list(userId="me").execute().get("drafts", [])

    for d in drafts:
        try:
            dm = svc.users().drafts().get(userId="me", id=d["id"]).execute()

            if dm.get("message", {}).get("threadId") == email_id:
                return {
                    "draft_id": d["id"],
                    "status": "exists"
                }
        except:
            continue

    # 2. Create new draft
    mime = f"Subject: Re: \n\n{reply_text}"
    raw = base64.urlsafe_b64encode(mime.encode("utf-8")).decode("utf-8")

    draft_body = {
        "message": {
            "raw": raw,
            "threadId": email_id
        }
    }

    created = svc.users().drafts().create(
        userId="me", body=draft_body
    ).execute()

    return {
        "draft_id": created.get("id"),
        "status": "created"
    }


def ensure_label_exists(label_name: str):
    svc = get_gmail_service()
    labels = svc.users().labels().list(userId="me").execute().get("labels", [])

    for l in labels:
        if l.get("name") == label_name:
            return l.get("id")

    body = {
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show"
    }

    created = svc.users().labels().create(userId="me", body=body).execute()
    return created.get("id")


def add_label_to_message(message_id: str, label_id: str):
    svc = get_gmail_service()
    body = {"addLabelIds": [label_id]}
    return svc.users().messages().modify(
        userId="me", id=message_id, body=body
    ).execute()
