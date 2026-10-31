#!/usr/bin/env python3
"""Exercise the pacman CAD applications through the installed headless MCP tools."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
CLIENT = ROOT / "agent/objects/envs/kicad-mcp/bin/python"


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    working = ROOT / "agent/objects/toolchain-check" / stamp
    working.mkdir(parents=True)
    evidence = ROOT / "agent/evidence/setup"
    checks = []

    def call(server, tool, arguments):
        filename = f"{stamp}-{server}-{tool}.json"
        command = [str(CLIENT), str(ROOT / "agent/scripts/check_mcp.py"), server,
                   "--tool", tool, "--arguments", json.dumps(arguments), "--output", filename]
        result = subprocess.run(command, text=True, capture_output=True, timeout=160)
        (evidence / f"{stamp}-{server}-{tool}.log").write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(f"{server}/{tool} failed: inspect {filename} and its log")
        checks.append({"server": server, "tool": tool, "evidence": str((evidence / filename).relative_to(ROOT))})
        record = json.loads((evidence / filename).read_text())["call"]["result"]
        # Some upstream KiCad tools encode failure as text with isError=false.
        texts = [item.get("text", "") for item in record.get("content", [])]
        if any(text.lstrip().startswith("❌") for text in texts):
            raise RuntimeError(f"{server}/{tool} reported failure: inspect {filename}")
        print(f"PASS {server}/{tool}", flush=True)
        return record

    native = working / "box.FCStd"
    step = working / "box.step"
    code = (
        "import FreeCAD as App, Part, json\n"
        "doc=App.newDocument('ToolchainCheck')\n"
        "box=doc.addObject('Part::Box','Box')\n"
        "box.Length=10; box.Width=20; box.Height=30\n"
        "doc.recompute()\n"
        "assert box.Shape.isValid() and abs(box.Shape.Volume-6000)<1e-6\n"
        f"doc.saveAs({str(native)!r})\n"
        f"Part.export([box],{str(step)!r})\n"
        "App.closeDocument(doc.Name)\n"
        f"doc=App.openDocument({str(native)!r})\n"
        "assert doc.Box.TypeId=='Part::Box' and abs(doc.Box.Shape.Volume-6000)<1e-6\n"
        "print(json.dumps({'version':App.Version(),'volume_mm3':doc.Box.Shape.Volume,'valid':doc.Box.Shape.isValid()}))\n"
    )
    call("freecad", "execute_code_headless", {"code": code, "timeout": 60})
    assert native.stat().st_size > 0 and step.stat().st_size > 0

    project = working / "kicad"
    call("kicad", "create_kicad_project", {"project_path": str(project), "project_name": "smoke"})
    board = project / "smoke.kicad_pcb"
    schematic = project / "smoke.kicad_sch"
    assert board.is_file() and schematic.is_file()
    call("kicad", "setup_pcb_layout", {"schematic_path": str(schematic), "width": 20, "height": 10})
    call("kicad", "get_pcb_statistics", {"file_path": str(board)})
    call("kicad", "run_drc", {"pcb_path": str(board)})
    call("kicad", "export_gerber", {"pcb_path": str(board), "output_dir": str(working / "gerbers")})
    assert any((working / "gerbers").iterdir())
    # Verify the saved board with the real pacman pcbnew bindings as well.
    inspect = (
        "import pcbnew,json; "
        f"b=pcbnew.LoadBoard({str(board)!r}); "
        "r=b.GetBoardEdgesBoundingBox(); "
        "w=pcbnew.ToMM(r.GetWidth()); h=pcbnew.ToMM(r.GetHeight()); "
        "assert abs(w-20)<0.2 and abs(h-10)<0.2; "
        "print(json.dumps({'width_mm':w,'height_mm':h}))"
    )
    env = dict(os.environ)
    for key, subdir in (("XDG_CACHE_HOME", "cache"), ("XDG_CONFIG_HOME", "config"),
                        ("XDG_DATA_HOME", "data")):
        directory = working / subdir
        directory.mkdir(exist_ok=True)
        env[key] = str(directory)
    result = subprocess.run(["/usr/bin/python3", "-c", inspect], env=env,
                            text=True, capture_output=True, check=True, timeout=30)
    (evidence / f"{stamp}-pcbnew.log").write_text(result.stdout + result.stderr)

    render = working / "blender.png"
    scene_file = working / "render.blend"
    code = (
        "import bpy, pathlib\n"
        "scene=bpy.context.scene\n"
        "scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=1\n"
        "scene.render.resolution_x=64; scene.render.resolution_y=64; scene.render.resolution_percentage=100\n"
        "scene.render.image_settings.file_format='PNG'\n"
        f"scene.render.filepath={str(render)!r}\n"
        f"bpy.ops.wm.save_as_mainfile(filepath={str(scene_file)!r})\n"
        "bpy.ops.render.render(write_still=True)\n"
        f"assert pathlib.Path({str(render)!r}).is_file()\n"
        "__result__={'version':bpy.app.version_string,'objects':len(scene.objects),'rendered':True}\n"
    )
    result = call("blender", "blender_python_exec", {"code": code, "transport": "headless",
                                                   "factory_startup": True, "timeout_seconds": 90})
    assert render.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", render.read_bytes()[16:24]) == (64, 64)
    assert scene_file.stat().st_size > 0

    versions = subprocess.check_output(["pacman", "-Q", "freecad", "kicad", "blender", "kicad-library"], text=True)
    summary = {"status": "PASS", "utc": stamp, "packages": versions.splitlines(),
               "checks": checks, "artifacts": str(working.relative_to(ROOT)),
               "scope": "Software integration smoke checks only; no RSIM hardware design or physical validation."}
    (evidence / "toolchain-verification.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
