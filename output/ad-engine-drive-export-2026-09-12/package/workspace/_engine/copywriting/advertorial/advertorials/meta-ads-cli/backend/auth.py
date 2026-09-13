"""JWT authentication decorator — validates Supabase Auth JWTs on API requests."""

import os
from functools import wraps

import jwt
from jwt import PyJWKClient
from flask import request, jsonify, g

from meta_ads.utils.logger import setup_logger

logger = setup_logger()

# JWKS client — fetches public keys from Supabase to verify JWTs.
# Supports both legacy HS256 and new ECC (P-256) signing keys.
_jwks_client = None


def _get_jwks_client():
    global _jwks_client
    if _jwks_client is None:
        supabase_url = os.environ.get("SUPABASE_URL", "").strip()
        if not supabase_url:
            raise RuntimeError("SUPABASE_URL env var not set")
        jwks_url = f"{supabase_url}/auth/v1/.well-known/jwks.json"
        _jwks_client = PyJWKClient(jwks_url, cache_keys=True, lifespan=3600)
    return _jwks_client


def require_auth(f):
    """Decorator that validates the Supabase JWT and sets g.user_id."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing authorization token"}), 401

        token = auth_header.split(" ", 1)[1]
        try:
            jwks_client = _get_jwks_client()
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["ES256", "HS256"],
                audience="authenticated",
            )
            g.user_id = payload["sub"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired — please log in again"}), 401
        except jwt.InvalidTokenError as e:
            logger.warning("JWT validation failed: %s", e)
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            logger.error("Auth error: %s", e)
            return jsonify({"error": "Authentication failed"}), 401

        return f(*args, **kwargs)
    return decorated
