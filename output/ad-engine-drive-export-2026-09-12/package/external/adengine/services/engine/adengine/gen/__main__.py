"""python -m adengine.gen            -> stdio MCP
   python -m adengine.gen --http 8771 -> streamable HTTP on 0.0.0.0:8771 (/mcp)"""
import argparse

from adengine.gen.server import serve

ap = argparse.ArgumentParser(prog="python -m adengine.gen")
ap.add_argument("--http", type=int, default=None, help="serve streamable HTTP on this port")
ap.add_argument("--host", default="0.0.0.0")
args = ap.parse_args()
serve(http_port=args.http, host=args.host)
