"""adengine.dr: the Direct Response OS as an MCP tool surface, rewired to the Store.

Everything here is workspace-scoped through adengine.core.auth.current_workspace().
No filesystem paths cross the tool boundary, nothing shells out, and no host or
port is assumed (URLs come from settings.public_base_url). Media is referenced by
asset id; boards, artifacts, approvals, concepts and jobs are Store records.

Run:  python -m adengine.dr            (stdio)
      python -m adengine.dr --http 8770  (streamable HTTP on ADENGINE_BIND, default 0.0.0.0)
"""
from .server import mcp, build_http_app  # noqa: F401

__all__ = ["mcp", "build_http_app"]
