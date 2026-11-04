#!/usr/bin/env python3
"""Create the local module layout without overwriting existing deliverables."""
import argparse
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Lowercase module name, for example wheel")
    parser.add_argument("--components", action="store_true", help="Add separate CAD part folder")
    parser.add_argument("--firmware", action="store_true", help="Add product firmware source root")
    parser.add_argument("--software", action="store_true", help="Add product software source root")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", args.name):
        parser.error("Use lowercase letters, digits and single hyphens; start with a letter.")
    root = args.root.resolve()
    module = root / "user/modules" / args.name
    specification = module / "SPECIFICATION.md"
    specification_text = None
    if not specification.exists():
        template = Path(__file__).resolve().parents[1] / "templates/module-specification.md"
        specification_text = template.read_text(encoding="utf-8").replace("{{module_name}}", args.name)
    folders = ["cad/exports", "electronics/kicad", "electronics/bom",
               "electronics/fabrication", "sim/fem", "sim/thermal",
               "sim/spice", "docs", "reference", "renders"]
    if args.components:
        folders.extend(["cad/components", "cad/exports/components"])
    code_rows = []
    if args.firmware:
        folders.append("firmware")
        code_rows.append("| [firmware/](firmware/) | Product source/build inputs by target |\n")
    if args.software:
        folders.append("software")
        code_rows.append("| [software/](software/) | Product source/build inputs by application |\n")
    for folder in folders:
        (module / folder).mkdir(parents=True, exist_ok=True)
    for parent in ("scripts", "config/modules", "evidence", "objects"):
        (root / "agent" / parent / args.name).mkdir(parents=True, exist_ok=True)
    if specification_text is not None:
        with specification.open("x", encoding="utf-8") as handle:
            handle.write(specification_text)
    readme = module / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {args.name.replace('-', ' ').capitalize()}\n\n"
            "Status: specification draft; module development has not been authorized.\n\n"
            "Complete [SPECIFICATION.md](SPECIFICATION.md), trace its requirements to the "
            "approved project specification, and record actual approval before implementation.\n\n"
            "| Directory | Contents |\n| --- | --- |\n"
            "| [cad/](cad/) | Native CAD with matching STEP; Blender scenes/assets |\n"
            "| [electronics/](electronics/) | KiCad projects/libraries, BOM and fabrication by board |\n"
            + "".join(code_rows)
            + "| [sim/](sim/) | Inputs, readable reports and selected results by study |\n"
            "| [docs/](docs/) | Reports, requirements and build instructions |\n"
            "| [reference/](reference/) | Datasheets, vendor CAD and references |\n"
            "| [renders/](renders/) | Final renders |\n\n"
            "Use named board, scene, study, firmware target and software application "
            "subfolders as needed. Keep their native dependencies and relative references intact.\n\n"
            "[Project rules](../../docs/project-rules.md). "
            "These are local working folders; MiniPLM stores the scoped product deliverables. "
            f"Within its selected project/iteration, this module maps to `{args.name}/`, "
            f"including `{args.name}/SPECIFICATION.md` and `{args.name}/cad/`. "
            "Creating this layout does not create a remote project or upload files.\n\n"
            "If MiniPLM or a usable target is unavailable, keep working in this structure "
            "and report local-only storage without PLM version control or revision history. "
            "Reconcile local files before any later repository upload.\n\n"
            "Agent notes, scripts, raw logs, JSON evidence, receipts and scratch remain local "
            f"under the matching `agent/` module folders (`{args.name}`); exclude them from PLM.\n",
            encoding="utf-8",
        )
    print(module)


if __name__ == "__main__":
    main()
