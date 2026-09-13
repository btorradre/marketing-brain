#!/usr/bin/env python3
"""
Plaid Link Server — CFO Agent
Runs a local Flask server with Plaid Link UI so you can authenticate
with Wells Fargo, Amex, and any other bank. Stores access tokens locally.
"""

import json
import os
import sys
import webbrowser
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template_string

# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

# --- Config ---
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "development")

DATA_DIR = Path(__file__).parent / "data"
TOKENS_FILE = DATA_DIR / "access_tokens.json"

if not PLAID_CLIENT_ID or not PLAID_SECRET:
    print("ERROR: PLAID_CLIENT_ID and PLAID_SECRET must be set in .env")
    sys.exit(1)

# --- Plaid Client ---
env_map = {
    "sandbox": plaid.Environment.Sandbox,
    "development": plaid.Environment.Sandbox,  # Dev keys work against sandbox host
    "production": plaid.Environment.Production,
}

configuration = plaid.Configuration(
    host=env_map.get(PLAID_ENV, "https://development.plaid.com"),
    api_key={
        "clientId": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET,
    },
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# --- Token Storage ---
def load_tokens():
    if TOKENS_FILE.exists():
        return json.loads(TOKENS_FILE.read_text())
    return {}

def save_token(institution_name, access_token, item_id):
    tokens = load_tokens()
    tokens[institution_name] = {
        "access_token": access_token,
        "item_id": item_id,
        "linked_at": datetime.now().isoformat(),
    }
    TOKENS_FILE.write_text(json.dumps(tokens, indent=2))
    print(f"  Saved access token for: {institution_name}")

# --- Flask App ---
app = Flask(__name__)

LINK_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CFO Agent — Link Bank Account</title>
    <script src="https://cdn.plaid.com/link/v2/stable/link-initialize.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            text-align: center;
            max-width: 500px;
            padding: 40px;
        }
        h1 { font-size: 28px; margin-bottom: 8px; color: #fff; }
        .subtitle { color: #888; margin-bottom: 32px; font-size: 14px; }
        .btn {
            display: inline-block;
            padding: 14px 32px;
            background: #3b82f6;
            color: #fff;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin: 8px;
            transition: background 0.2s;
        }
        .btn:hover { background: #2563eb; }
        .btn:disabled { background: #333; color: #666; cursor: not-allowed; }
        .linked {
            margin-top: 24px;
            padding: 16px;
            background: #111;
            border-radius: 8px;
            border: 1px solid #222;
        }
        .linked h3 { color: #10b981; margin-bottom: 8px; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
        .linked-item {
            padding: 8px 0;
            border-bottom: 1px solid #1a1a1a;
            font-size: 14px;
        }
        .linked-item:last-child { border-bottom: none; }
        .status { margin-top: 16px; font-size: 13px; color: #666; }
        .success { color: #10b981; }
        .error { color: #ef4444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>CFO Agent</h1>
        <p class="subtitle">Link your bank accounts for spending analysis</p>

        <button class="btn" id="link-btn" onclick="openPlaidLink()">
            + Connect Bank Account
        </button>

        <div class="linked" id="linked-section" style="display:none;">
            <h3>Linked Accounts</h3>
            <div id="linked-list"></div>
        </div>

        <p class="status" id="status"></p>
    </div>

    <script>
        let linkHandler = null;

        // Load existing linked accounts on page load
        fetch('/api/linked_accounts')
            .then(r => r.json())
            .then(data => {
                if (data.accounts && data.accounts.length > 0) {
                    const section = document.getElementById('linked-section');
                    const list = document.getElementById('linked-list');
                    section.style.display = 'block';
                    data.accounts.forEach(name => {
                        list.innerHTML += `<div class="linked-item">&#9989; ${name}</div>`;
                    });
                }
            });

        async function openPlaidLink() {
            const btn = document.getElementById('link-btn');
            const status = document.getElementById('status');
            btn.disabled = true;
            status.textContent = 'Initializing Plaid Link...';
            status.className = 'status';

            try {
                const resp = await fetch('/api/create_link_token', { method: 'POST' });
                const data = await resp.json();

                if (data.error) {
                    status.textContent = 'Error: ' + data.error;
                    status.className = 'status error';
                    btn.disabled = false;
                    return;
                }

                const handler = Plaid.create({
                    token: data.link_token,
                    onSuccess: async (public_token, metadata) => {
                        status.textContent = 'Exchanging token...';
                        const institution = metadata.institution.name;

                        const exchResp = await fetch('/api/exchange_token', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                public_token: public_token,
                                institution_name: institution,
                            }),
                        });
                        const exchData = await exchResp.json();

                        if (exchData.success) {
                            status.textContent = `${institution} linked successfully!`;
                            status.className = 'status success';

                            const section = document.getElementById('linked-section');
                            const list = document.getElementById('linked-list');
                            section.style.display = 'block';
                            list.innerHTML += `<div class="linked-item">&#9989; ${institution}</div>`;
                        } else {
                            status.textContent = 'Error saving token: ' + (exchData.error || 'unknown');
                            status.className = 'status error';
                        }
                        btn.disabled = false;
                    },
                    onExit: (err) => {
                        btn.disabled = false;
                        if (err) {
                            status.textContent = 'Link exited: ' + err.display_message;
                            status.className = 'status error';
                        } else {
                            status.textContent = '';
                        }
                    },
                });
                handler.open();
            } catch (e) {
                status.textContent = 'Error: ' + e.message;
                status.className = 'status error';
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(LINK_HTML)

@app.route("/api/create_link_token", methods=["POST"])
def create_link_token():
    try:
        req = LinkTokenCreateRequest(
            products=[Products("transactions")],
            client_name="CFO Agent",
            country_codes=[CountryCode("US")],
            language="en",
            user=LinkTokenCreateRequestUser(client_user_id="cfo-agent-user"),
        )
        response = client.link_token_create(req)
        return jsonify({"link_token": response["link_token"]})
    except plaid.ApiException as e:
        error_response = json.loads(e.body)
        return jsonify({"error": error_response.get("error_message", str(e))}), 400

@app.route("/api/exchange_token", methods=["POST"])
def exchange_token():
    data = request.json
    public_token = data.get("public_token")
    institution_name = data.get("institution_name", "Unknown")

    try:
        exchange_req = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = client.item_public_token_exchange(exchange_req)
        access_token = exchange_response["access_token"]
        item_id = exchange_response["item_id"]

        save_token(institution_name, access_token, item_id)
        return jsonify({"success": True, "institution": institution_name})
    except plaid.ApiException as e:
        error_response = json.loads(e.body)
        return jsonify({"error": error_response.get("error_message", str(e))}), 400

@app.route("/api/linked_accounts")
def linked_accounts():
    tokens = load_tokens()
    return jsonify({"accounts": list(tokens.keys())})

if __name__ == "__main__":
    port = 8234
    print(f"\n  CFO Agent — Plaid Link Server")
    print(f"  Open http://localhost:{port} to connect your bank accounts")
    print(f"  Press Ctrl+C to stop\n")
    webbrowser.open(f"http://localhost:{port}")
    app.run(port=port, debug=False)
