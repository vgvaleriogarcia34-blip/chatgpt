import os
from dotenv import load_dotenv

load_dotenv()

MS_CLIENT_ID = os.getenv("MS_CLIENT_ID", "")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET", "")
MS_TENANT = os.getenv("MS_TENANT", "common")
MS_REDIRECT_URI = os.getenv("MS_REDIRECT_URI", "http://localhost:8000/auth/callback")

MS_AUTHORITY = f"https://login.microsoftonline.com/{MS_TENANT}"
MS_SCOPES = ["Mail.Read", "Mail.Send", "User.Read"]
GRAPH_BASE = "https://graph.microsoft.com/v1.0"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

SESSION_SECRET = os.getenv("SESSION_SECRET", "dev-secret-change-me")
