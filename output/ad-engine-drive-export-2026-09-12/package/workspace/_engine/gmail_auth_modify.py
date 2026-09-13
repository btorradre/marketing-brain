#!/usr/bin/env python3
"""One-time consent for gmail.modify + settings.basic on btorradre@gmail.com."""
from google_auth_oauthlib.flow import InstalledAppFlow

CRED = "/Users/brooksorradre2/Documents/marketing brain/_engine/oauth credentials/client_secret_1023830201261-4tdgd3prohtl9jji7o695m07l48u6hoe.apps.googleusercontent.com.json"
OUT = "/Users/brooksorradre2/Documents/marketing brain/_engine/oauth credentials/btorradre_gmail_modify_token.json"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.settings.basic",
]

flow = InstalledAppFlow.from_client_secrets_file(CRED, SCOPES)
creds = flow.run_local_server(port=0, prompt="consent", open_browser=True)
with open(OUT, "w") as f:
    f.write(creds.to_json())
print("SAVED", OUT)
