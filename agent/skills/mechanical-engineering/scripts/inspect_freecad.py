#!/usr/bin/env python3
"""Read-only FreeCAD model check. Run in a Python environment with FreeCAD bindings."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("--object", dest="object_name", help="Specific solid-bearing object")
    parser.add_argument("--output", type=Path, help="New JSON report path")
    args = parser.parse_args()
    model = args.model.resolve()
    if not model.is_file() or model.suffix != ".FCStd":
        parser.error("Expected an existing native .FCStd model")
    if args.output and (args.output.exists() or args.output.is_symlink()
                        or args.output.resolve() == model):
        parser.error("Output must be a new file, never the model")
    try:
        import FreeCAD as App
    except ImportError:
        print("FreeCAD Python bindings unavailable; run in the FreeCAD Python environment.",
              file=sys.stderr)
        return 2

    document, findings, examined = None, [], []
    try:
        document = App.openDocument(str(model))
        document.recompute()
        if args.object_name:
            obj = document.getObject(args.object_name)
            candidates = [obj] if obj is not None else []
            if not candidates:
                findings.append(f"Missing object: {args.object_name}")
        else:
            candidates = [obj for obj in document.Objects
                          if obj.TypeId in ("PartDesign::Body", "Part::Feature")]
        for obj in candidates:
            shape = getattr(obj, "Shape", None)
            if shape is None or shape.isNull():
                findings.append(f"No valid shape on {obj.Name}")
                continue
            valid, count = bool(shape.isValid()), len(shape.Solids)
            examined.append({"name": obj.Name, "type": obj.TypeId,
                             "valid": valid, "solid_count": count})
            if not valid or count < 1:
                findings.append(f"Invalid or non-solid shape: {obj.Name}")
        if not examined:
            findings.append("No solid objects were inspected")
    except Exception as exc:
        findings.append(f"Inspection failed: {type(exc).__name__}: {exc}")
    finally:
        if document is not None:
            App.closeDocument(document.Name)

    valid = not findings
    report = {
        "schema_version": 1, "tool": "FreeCAD shape inspector",
        "freecad_version": ".".join(str(x) for x in App.Version()),
        "source": str(model),
        "source_sha256": hashlib.sha256(model.read_bytes()).hexdigest(),
        "objects": examined, "errors": findings,
        "metrics": {"valid_geometry": {"value": valid}, "recompute_ok": {"value": valid}},
    }
    payload = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
