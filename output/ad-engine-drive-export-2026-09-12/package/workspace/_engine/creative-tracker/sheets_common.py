"""Shared Google Sheets auth + config for the creative tracker."""
import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TOKEN = ROOT / "auth" / "bto-ec-google-auth" / "token.json"
CONFIG = HERE / "sheet_config.json"


def sheets_service():
    creds = Credentials.from_authorized_user_file(str(TOKEN))
    if not creds.valid:
        creds.refresh(Request())
        TOKEN.write_text(creds.to_json())
    return build("sheets", "v4", credentials=creds)


def drive_service():
    creds = Credentials.from_authorized_user_file(str(TOKEN))
    if not creds.valid:
        creds.refresh(Request())
        TOKEN.write_text(creds.to_json())
    return build("drive", "v3", credentials=creds)


def sheet_id():
    return json.loads(CONFIG.read_text())["spreadsheet_id"]
