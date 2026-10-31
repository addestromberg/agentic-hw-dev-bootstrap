#!/usr/bin/env python3
"""Rebuild isolated MCP environments from the pinned upstream source commits."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def run(*args):
    subprocess.run(args, check=True, cwd=ROOT)


def main():
    os.environ["UV_CACHE_DIR"] = str(ROOT / "agent/objects/cache/uv")
    sources = json.loads((ROOT / "agent/config/mcp-sources.json").read_text())
    for name, spec in sources.items():
        source = ROOT / "agent/objects/mcp-sources" / name
        if not source.exists():
            source.mkdir(parents=True)
            run("git", "init", str(source))
            run("git", "-C", str(source), "remote", "add", "origin", spec["repository"])
            run("git", "-C", str(source), "fetch", "--depth", "1", "origin", spec["commit"])
            run("git", "-C", str(source), "checkout", "--detach", "FETCH_HEAD")
        actual = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
        dirty = subprocess.check_output(["git", "-C", str(source), "status", "--porcelain"], text=True).strip()
        if actual != spec["commit"] or dirty:
            raise SystemExit(f"Source differs from pinned clean baseline: {source}; inspect before reinstalling.")
        environment = ROOT / "agent/objects/envs" / f"{name}-mcp"
        if not (environment / "pyvenv.cfg").exists():
            run("uv", "venv", "--python", sys.executable, str(environment))
        run("uv", "pip", "install", "--python", str(environment / "bin/python"), str(source))


if __name__ == "__main__":
    main()
