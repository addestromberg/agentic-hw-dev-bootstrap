#!/usr/bin/env python3
"""Launch one installed MCP server with its scratch/cache files inside agent/."""
import argparse
import os
from pathlib import Path
import shutil
import sys
import sysconfig

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("server", choices=("freecad", "kicad", "blender"))
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    environment = ROOT / "agent/objects/envs" / f"{args.server}-mcp"
    if not args.worker:
        python = environment / "bin/python"
        if not python.exists():
            parser.error("MCP environment missing; run agent/scripts/setup_mcp.py.")
        os.execv(str(python), [str(python), str(Path(__file__).resolve()), args.server, "--worker"])
    runtime = ROOT / "agent/objects/runtime" / args.server
    for folder in (runtime, runtime / "tmp", runtime / "cache", runtime / "config", runtime / "data"):
        folder.mkdir(parents=True, exist_ok=True)
    os.chdir(runtime)
    os.environ["TMPDIR"] = str(runtime / "tmp")
    os.environ["XDG_CACHE_HOME"] = str(runtime / "cache")
    os.environ["XDG_CONFIG_HOME"] = str(runtime / "config")
    os.environ["XDG_DATA_HOME"] = str(runtime / "data")
    if args.server == "freecad":
        from freecad_mcp import headless
        from freecad_mcp.server import main as serve
        # Upstream hardcodes ~/.cache for temporary scripts, ignoring XDG_CACHE_HOME.
        # Keep that single path inside this project's agent working area.
        headless._script_dir = lambda: runtime / "tmp"
        command = shutil.which("freecadcmd") or shutil.which("FreeCADCmd") or "freecadcmd"
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        sys.argv = ["freecad-mcp", "--only-text-feedback", "--freecadcmd", command]
    elif args.server == "kicad":
        # Pacman's pcbnew/wx bindings belong to the system Python, not PyPI.
        system_packages = sysconfig.get_path("purelib", vars={"base": sys.base_prefix,
                                                              "platbase": sys.base_prefix})
        if system_packages not in sys.path:
            sys.path.append(system_packages)
        os.environ["KICAD_PROJECT_PATHS"] = str(ROOT / "user/modules")
        os.environ["KICAD_PYTHON"] = "/usr/bin/python3"
        for version in (9, 10):
            os.environ.setdefault(f"KICAD{version}_SYMBOL_DIR", "/usr/share/kicad/symbols")
            os.environ.setdefault(f"KICAD{version}_FOOTPRINT_DIR", "/usr/share/kicad/footprints")
        from kicad_mcp_server.__main__ import main as serve
        sys.argv = ["kicad-mcp-server"]
    else:
        os.environ["BLENDER_BIN"] = shutil.which("blender") or "/usr/bin/blender"
        # Arch Blender otherwise finds a user-installed python3.14 on PATH first.
        os.environ["BLENDER_SYSTEM_PYTHON"] = "/usr"
        os.environ["BLENDER_MCP_HEADLESS"] = "1"
        os.environ["BLENDER_MCP_TOKEN_FILE"] = str(runtime / "bridge-token")
        os.environ["BLENDER_USER_CONFIG"] = str(runtime / "config")
        from blender_mcp_server import main as serve
        sys.argv = ["blender-mcp-server"]
    serve()


if __name__ == "__main__":
    main()
