"""Configuration loader — reads .env and validates required settings."""

import os
import sys
from dotenv import load_dotenv


def load_config(env_path: str = None) -> dict:
    """Load and validate configuration from .env file.

    Returns a dict with all required config values.
    Exits with a clear error if any required value is missing.
    """
    # Load from explicit path or auto-discover .env (skip if no file exists, e.g. serverless)
    if env_path and os.path.exists(env_path):
        load_dotenv(env_path)
    elif not env_path:
        load_dotenv()

    config = {
        "access_token": os.getenv("META_ACCESS_TOKEN"),
        "ad_account_id": os.getenv("META_AD_ACCOUNT_ID"),
        "api_version": os.getenv("META_API_VERSION", "v21.0"),
        "app_id": os.getenv("META_APP_ID", ""),
        "app_secret": os.getenv("META_APP_SECRET", ""),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }

    # Validate required fields
    missing = []
    if not config["access_token"]:
        missing.append("META_ACCESS_TOKEN")
    if not config["ad_account_id"]:
        missing.append("META_AD_ACCOUNT_ID")

    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}. "
            "Set them in Vercel env vars or in a .env file."
        )

    # Ensure ad account ID has the act_ prefix
    if not config["ad_account_id"].startswith("act_"):
        config["ad_account_id"] = f"act_{config['ad_account_id']}"

    return config
