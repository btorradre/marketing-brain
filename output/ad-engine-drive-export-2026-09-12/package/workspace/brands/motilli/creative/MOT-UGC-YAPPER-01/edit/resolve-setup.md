# DaVinci Resolve setup — 2026-09-09

Latest user instruction makes DaVinci Resolve the default editor going forward. Workspace AGENTS.md updated accordingly. Existing edit projects have not been modified.

- Official requested repository: https://github.com/samuelgursky/davinci-resolve-mcp
- Local source install: `/Users/brooksorradre2/.local/share/davinci-resolve-mcp`
- Python environment and dependencies installed; compound server entry: `src/server.py`.
- Codex configuration registered under `[mcp_servers.davinci-resolve]` in `~/.codex/config.toml`; other configured servers retained.
- Resolve app is running, installed version 21.1.0. The scripting module loads.
- **Live Resolve connection not established:** installer check returned no external scripting connection. Registration is not proof of an operational editing connection.
- On Studio, Preferences > General > External scripting using must allow Local. Edition is not confirmed. The repository documents restrictions for free 21.1; do not assume its older free-edition bridge will work on this version.
- Current session has no callable Resolve MCP tool loaded yet; registration is for client reconnection/new session. No timeline or project was created.
- Installer's optional release-update check encountered a local certificate verification error; installation and registration completed. TLS verification was not disabled. Update policy is notification-only.

Before editing: establish the live connection, inspect tool capabilities and current project read-only, then create an isolated project/timeline for this ad. Documentation: https://github.com/samuelgursky/davinci-resolve-mcp/blob/main/docs/install.md
