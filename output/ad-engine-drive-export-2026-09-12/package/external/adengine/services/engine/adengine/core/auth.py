"""Workspace scoping. The workspace comes from the auth context, never from a tool argument."""
from __future__ import annotations
import contextvars
import functools
from dataclasses import dataclass
from .settings import settings
from .errors import Forbidden


@dataclass(frozen=True)
class AuthContext:
    workspace_id: str
    member_id: str
    role: str  # owner | editor | viewer | agent

    def can_write(self) -> bool:
        return self.role in ("owner", "editor", "agent")

    def can_approve(self) -> bool:
        return self.role in ("owner", "editor")


_ctx: contextvars.ContextVar[AuthContext | None] = contextvars.ContextVar("adengine_auth", default=None)


def set_auth_context(ctx: AuthContext):
    return _ctx.set(ctx)


def current() -> AuthContext:
    ctx = _ctx.get()
    if ctx is None:
        if settings.auth_mode == "dev" and settings.dev_workspace:
            return AuthContext(workspace_id=settings.dev_workspace, member_id="dev", role="owner")
        raise Forbidden("no workspace in auth context")
    return ctx


def current_workspace() -> str:
    return current().workspace_id


def require_write(fn):
    """Enforce member permissions before a tool reads inputs or has side effects."""
    @functools.wraps(fn)
    def guarded(*args, **kwargs):
        ctx = current()
        if not ctx.can_write():
            raise Forbidden(f"role '{ctx.role}' cannot write or enqueue jobs")
        return fn(*args, **kwargs)
    return guarded
