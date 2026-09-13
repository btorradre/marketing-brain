"""AES-256-GCM encryption for storing Meta access tokens at rest."""

import os
import secrets

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def _get_key() -> bytes:
    """Load the 32-byte encryption key from ENCRYPTION_KEY env var (hex-encoded)."""
    key_hex = os.environ.get("ENCRYPTION_KEY", "")
    if not key_hex:
        raise RuntimeError("ENCRYPTION_KEY env var not set")
    return bytes.fromhex(key_hex)


def encrypt(plaintext: str) -> str:
    """Encrypt a string with AES-256-GCM. Returns 'nonce_hex:ciphertext_hex'."""
    key = _get_key()
    nonce = secrets.token_bytes(12)
    aesgcm = AESGCM(key)
    ct = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    return f"{nonce.hex()}:{ct.hex()}"


def decrypt(ciphertext: str) -> str:
    """Decrypt an AES-256-GCM ciphertext. Expects 'nonce_hex:ciphertext_hex'."""
    key = _get_key()
    nonce_hex, ct_hex = ciphertext.split(":", 1)
    nonce = bytes.fromhex(nonce_hex)
    ct = bytes.fromhex(ct_hex)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ct, None).decode("utf-8")
