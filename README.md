📬 InboxGenie

AI-powered email assistant that analyzes emails, categorizes them, drafts replies, and schedules meetings using Google Gemini, Gmail API, and Calendar API.

<p align="center">
  <img src="https://raw.githubusercontent.com/<sanikaaa11>/<repo>/main/banner.png" width="100%" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Google%20Gemini-API-orange?style=for-the-badge&logo=google" />
  <img src="https://img.shields.io/badge/Gmail%20API-Enabled-red?style=for-the-badge&logo=gmail" />
  <img src="https://img.shields.io/badge/Google%20Calendar-API-blue?style=for-the-badge&logo=google-calendar" />
  <img src="https://img.shields.io/badge/Kaggle-Notebook-blue?style=for-the-badge&logo=kaggle" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>


⭐ Features

AI-based email understanding

Automatic categorization

Smart context-aware draft replies

Calendar event scheduling

Thread-safe draft deduplication

Blocked-sender support

Secure OAuth authentication

🏗️ System Architecture

Architecture Diagram

Agent Workflow

Processing Pipeline

📁 Project Structure

InboxGenie/
│
├── agents/
│   ├── reader_agent.py
│   ├── decision_agent.py
│   ├── categorizer_agent.py
│   ├── reply_agent.py
│   └── task_agent.py
│
├── tools/
│   ├── gmail_tool.py
│   ├── calendar_tool.py
│
├── llm/
│   ├── model.py
│   └── genai_guard.py
│
├── assets/
│   └── images/
│       ├── architecture.png
│       ├── workflow.png
│       └── pipeline.png
│
├── main.py
├── requirements.txt
├── blocked_senders.json
├── processed_emails.json
└── README.md

⚙️ Setup
1. Install dependencies
pip install -r requirements.txt

2. Add your Gemini API key

Create a .env file:

GEMINI_API_KEY=YOUR_API_KEY

3. Add Google OAuth credentials

Download your credentials.json from Google Cloud and place it in the project root.

Run once to generate token.json:

python main.py

4. Run InboxGenie
python main.py

🔐 Security Notes

No email is auto-sent (drafts only)

OAuth tokens are not included in the repository

Authentication happens on the user's machine

Email analysis is limited to required fields

Duplicate drafts are prevented

❤️ Built With

Google Gemini 2.0 Flash

Gmail API

Google Calendar API

Python
