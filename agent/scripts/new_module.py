#!/usr/bin/env python3
"""Create the agreed module layout without overwriting existing deliverables."""
import argparse
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Lowercase module name, for example wheel")
    parser.add_argument("--components", action="store_true", help="Add separate CAD part folder")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", args.name):
        parser.error("Use lowercase letters, digits and single hyphens; start with a letter.")
    root = args.root.resolve()
    module = root / "user/modules" / args.name
    folders = ["cad/exports", "electronics/kicad", "electronics/bom",
               "electronics/fabrication/gerbers", "electronics/fabrication/drill",
               "electronics/fabrication/assembly", "sim/fem", "sim/thermal",
               "sim/spice", "docs", "reference", "renders"]
    if args.components:
        folders.append("cad/components")
    for folder in folders:
        (module / folder).mkdir(parents=True, exist_ok=True)
    for parent in ("scripts", "config/modules", "evidence", "objects"):
        (root / "agent" / parent / args.name).mkdir(parents=True, exist_ok=True)
    readme = module / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {args.name.replace('-', ' ').capitalize()}\n\n"
            "Status: layout created; requirements and design are not established.\n\n"
            "| Directory | Contents |\n| --- | --- |\n"
            "| [cad/](cad/) | Native CAD, drawings and exchange exports |\n"
            "| [electronics/](electronics/) | KiCad, BOM and fabrication files |\n"
            "| [sim/](sim/) | FEM, thermal, SPICE and useful analysis results |\n"
            "| [docs/](docs/) | Reports, requirements and build instructions |\n"
            "| [reference/](reference/) | Datasheets, vendor CAD and references |\n"
            "| [renders/](renders/) | Final renders |\n\n"
            "[Project rules](../../docs/project-rules.md). Automation and raw evidence "
            f"belong under the matching `agent/` module folders (`{args.name}`).\n",
            encoding="utf-8",
        )
    print(module)


if __name__ == "__main__":
    main()
