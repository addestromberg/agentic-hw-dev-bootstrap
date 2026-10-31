#!/usr/bin/env python3
"""Check MCP startup/tool discovery and optionally call a tool with JSON arguments.

Run with agent/objects/envs/kicad-mcp/bin/python (the MCP client SDK is installed there).
"""
import argparse
import asyncio
from datetime import timedelta
import json
import os
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[2]


async def check(args):
    destination = ROOT / "agent/evidence/setup"
    destination.mkdir(parents=True, exist_ok=True)
    parameters = StdioServerParameters(command=sys.executable,
        args=[str(ROOT / "agent/scripts/run_mcp.py"), args.server], env=dict(os.environ))
    with (destination / f"{args.server}-mcp-stderr.log").open("a") as errors:
        async with stdio_client(parameters, errlog=errors) as (reader, writer):
            async with ClientSession(reader, writer, read_timeout_seconds=timedelta(seconds=120)) as session:
                initialized = await session.initialize()
                tools = await session.list_tools()
                record = {"server": initialized.serverInfo.model_dump(mode="json"),
                          "protocol_version": initialized.protocolVersion,
                          "tools": [tool.model_dump(mode="json") for tool in tools.tools]}
                if args.tool:
                    result = await session.call_tool(args.tool, json.loads(args.arguments))
                    record["call"] = {"tool": args.tool, "arguments": json.loads(args.arguments),
                                      "result": result.model_dump(mode="json")}
                    failed = bool(result.isError)
                    for item in result.content:
                        if getattr(item, "type", None) != "text":
                            continue
                        failed = failed or item.text.lstrip("# \n").startswith("❌")
                        try:
                            payload = json.loads(item.text)
                        except (ValueError, TypeError):
                            continue
                        if isinstance(payload, dict):
                            failed = failed or bool(payload.get("error")) or payload.get("success") is False
                    record["call"]["failed"] = failed
                output = destination / (args.output or f"{args.server}-mcp-check.json")
                output.write_text(json.dumps(record, indent=2) + "\n")
                print(json.dumps({"server": args.server, "tools": len(tools.tools),
                                  "output": str(output),
                                  "call_failed": record.get("call", {}).get("failed")}))
                if record.get("call", {}).get("failed"):
                    raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("server", choices=("freecad", "kicad", "blender"))
    parser.add_argument("--tool")
    parser.add_argument("--arguments", default="{}")
    parser.add_argument("--output", help="Filename below agent/evidence/setup/")
    args = parser.parse_args()
    if args.output and Path(args.output).name != args.output:
        parser.error("--output must be a filename, not a path")
    awaitable = check(args)
    asyncio.run(asyncio.wait_for(awaitable, timeout=150))


if __name__ == "__main__":
    main()
