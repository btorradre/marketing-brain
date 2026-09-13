"""python -m adengine.dr [--http [PORT]] [--bind HOST]

Default: stdio. --http serves streamable HTTP at /mcp on ADENGINE_BIND
(default 0.0.0.0) and the given port (default 8770).
"""
from __future__ import annotations

import argparse
import os


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="adengine.dr")
    ap.add_argument("--http", nargs="?", const=8770, type=int, default=None, metavar="PORT")
    ap.add_argument("--bind", default=os.environ.get("ADENGINE_BIND") or "0.0.0.0")
    args = ap.parse_args(argv)

    from .server import run_http, run_stdio
    if args.http is not None:
        run_http(port=args.http, bind=args.bind)
    else:
        run_stdio()


if __name__ == "__main__":
    main()
