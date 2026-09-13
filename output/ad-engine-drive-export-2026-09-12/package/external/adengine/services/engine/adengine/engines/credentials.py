"""Provider credentials, workspace-scoped.

A workspace stores one 'credential' record per provider:
    {id, workspace_id, provider, secret | ciphertext, last_verified}

Phase 0 keeps the key in plaintext under `secret`. Phase 1 replaces that with
envelope encryption (`ciphertext` + a KMS-wrapped data key); the only place that
needs to change is `_unseal` below.

In dev auth mode a missing record falls back to the environment variable
ADENGINE_<PROVIDER>_KEY so a single-tenant developer box works without seeding
records. In any other auth mode the environment is never consulted.
"""
from __future__ import annotations

from adengine.core.auth import require_write

import os

from adengine.core.auth import current_workspace
from adengine.core.errors import ProviderError
from adengine.core.settings import settings
from adengine.core.store import Store, get_store

PROVIDERS = ("kie", "elevenlabs", "heygen", "gemini", "gethookd", "openai", "groq")


class MissingCredential(ProviderError):
    """No usable key for the provider in this workspace."""


def _unseal(record: dict) -> str | None:
    """Return the plaintext secret for a credential record.

    PHASE 1 HOOK (envelope encryption): when records carry `ciphertext` and
    `wrapped_key`, decrypt here with the workspace KMS key and return the
    plaintext. Until then only the plaintext `secret` field is honoured.
    """
    secret = record.get("secret")
    if secret:
        return str(secret)
    if record.get("ciphertext"):
        raise MissingCredential(
            f"credential {record.get('id')} is sealed but envelope decryption is not "
            "available yet (Phase 1); re-save it with a plaintext `secret` for now")
    return None


def get_key(provider: str, workspace_id: str | None = None, store: Store | None = None) -> str:
    """Resolve the API key for `provider` in the current (or given) workspace."""
    provider = (provider or "").lower()
    if provider not in PROVIDERS:
        raise ProviderError(f"unknown provider '{provider}'; known: {', '.join(PROVIDERS)}")
    store = store or get_store()
    ws = workspace_id or current_workspace()
    for rec in store.find("credential", ws, provider=provider):
        secret = _unseal(rec)
        if secret:
            return secret
    if settings.auth_mode == "dev":
        env = os.environ.get(f"ADENGINE_{provider.upper()}_KEY")
        if env:
            return env
    raise MissingCredential(
        f"no '{provider}' credential in workspace {ws}; save a credential record for it")


def try_get_key(provider: str, workspace_id: str | None = None, store: Store | None = None) -> str | None:
    try:
        return get_key(provider, workspace_id=workspace_id, store=store)
    except ProviderError:
        return None


@require_write
def save_key(provider: str, secret: str, workspace_id: str | None = None,
             store: Store | None = None) -> dict:
    """Create or replace the workspace's credential record for `provider` (plaintext, Phase 0)."""
    provider = (provider or "").lower()
    if provider not in PROVIDERS:
        raise ProviderError(f"unknown provider '{provider}'")
    store = store or get_store()
    ws = workspace_id or current_workspace()
    existing = store.find("credential", ws, provider=provider)
    if existing:
        return store.update("credential", ws, existing[0]["id"], secret=secret, ciphertext=None)
    return store.create("credential", ws, "cred", provider=provider, secret=secret,
                        ciphertext=None, last_verified=None)
