"""Bearer-token auth middleware hook for the HTTP transport.

auth_mode == "dev": requests pass through; adengine.core.auth.current() falls
back to ADENGINE_DEV_WORKSPACE with an owner role.

auth_mode == "oauth": every HTTP request must carry `Authorization: Bearer
<token>`. The token goes through the pluggable resolver
`resolve_token(token) -> AuthContext`; the resulting context is set for the
request so every tool call is scoped to that workspace and member. The default
resolver is a stub that raises Forbidden. Phase 1 wires it to the real OAuth
server with set_token_resolver(fn) (validate the JWT / introspect it, map the
subject to workspace_id, member_id, role).

Context propagation: the AuthContext is a contextvar set in the request task.
The streamable-HTTP app is run stateless in oauth mode so every request's tool
handlers execute inside that request's task and inherit the context.
"""
from __future__ import annotations

import json
from typing import Awaitable, Callable

from adengine.core.auth import AuthContext, set_auth_context, _ctx
from adengine.core.errors import Forbidden
from adengine.core.settings import settings

ResolveToken = Callable[[str], AuthContext]


def _stub_resolve(token: str) -> AuthContext:
    raise Forbidden("token resolution is not wired in this build (Phase 1: connect the OAuth server)")


resolve_token: ResolveToken = _stub_resolve


def set_token_resolver(fn: ResolveToken) -> None:
    global resolve_token
    resolve_token = fn


def _json_response(status: int, body: dict):
    payload = json.dumps(body).encode()
    headers = [(b"content-type", b"application/json"), (b"content-length", str(len(payload)).encode())]
    if status == 401:
        headers.append((b"www-authenticate", b"Bearer"))

    async def send_it(send):
        await send({"type": "http.response.start", "status": status, "headers": headers})
        await send({"type": "http.response.body", "body": payload})
    return send_it


class AuthMiddleware:
    """Pure ASGI middleware. Wrap the Starlette app returned by mcp.streamable_http_app()."""

    def __init__(self, app, mode: str | None = None):
        self.app = app
        self.mode = mode or settings.auth_mode

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or self.mode != "oauth":
            return await self.app(scope, receive, send)
        headers = {k.decode().lower(): v.decode() for k, v in scope.get("headers") or []}
        auth = headers.get("authorization", "")
        if not auth.lower().startswith("bearer ") or not auth[7:].strip():
            return await _json_response(401, {"error": "missing bearer token"})(send)
        try:
            ctx = resolve_token(auth[7:].strip())
        except Forbidden as exc:
            return await _json_response(403, {"error": str(exc)})(send)
        token = set_auth_context(ctx)
        try:
            await self.app(scope, receive, send)
        finally:
            _ctx.reset(token)
