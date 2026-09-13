"""trace.jsonl writer: every SDK message and every hook event, one line each."""

from __future__ import annotations

import dataclasses
import json
import time
from pathlib import Path
from typing import Any


def _plain(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        # walk fields by hand so nested dataclasses keep their _type tag
        # (dataclasses.asdict flattens them to plain dicts first)
        return {"_type": type(obj).__name__,
                **{f.name: _plain(getattr(obj, f.name)) for f in dataclasses.fields(obj)}}
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_plain(v) for v in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return repr(obj)


class Trace:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = open(path, "a", encoding="utf-8")
        self.tool_calls = 0
        self.tools_used: dict[str, int] = {}

    def write(self, kind: str, payload: Any) -> None:
        rec = {"ts": round(time.time(), 3), "kind": kind, "payload": _plain(payload)}
        self._fh.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
        self._fh.flush()

    def message(self, msg: Any) -> None:
        name = type(msg).__name__
        self.write(name, msg)
        if name == "AssistantMessage":
            for block in getattr(msg, "content", []) or []:
                if type(block).__name__ == "ToolUseBlock":
                    self.tool_calls += 1
                    tool = getattr(block, "name", "?")
                    self.tools_used[tool] = self.tools_used.get(tool, 0) + 1

    def close(self) -> None:
        self._fh.close()
