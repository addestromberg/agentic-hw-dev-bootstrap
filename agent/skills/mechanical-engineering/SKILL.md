---
name: mechanical-engineering
description: Design and review mechanical assemblies, native parametric CAD, materials, tolerances, 3D-printing or fabrication, structural and thermal interfaces, fit and motion. Use for FreeCAD models, mounts, housings, moving stages and manufacturing drawings; not for PCB-only electrical design.
---

# Mechanical engineering

Use $engineering-workflow for cross-discipline requirements and formal handoffs. Read the owning project's native CAD source, assembly context, operating conditions and [mechanical checks](references/design-checklist.md) before editing.

Before module CAD development, follow the
[specification gate](../engineering-workflow/references/module-specification.md)
and read the approved project and module-root `SPECIFICATION.md` baselines. Resolve missing mechanical
requirements/interfaces through specification work before implementation; scoped
feasibility studies remain preliminary. Reapprove affected requirements changes.
Apply the [PLM lifecycle](../../../user/docs/plm-lifecycle.md) at concept, design,
detail and tooling reviews. Tool/fixture sources belong in `cad/tooling/` with
matching STEP exports under `cad/exports/tooling/`. Carry manufacturing and
inspection requirements into readable plans; do not advance physical stages
based on CAD, a render or planned assembly instructions alone.

For MiniPLM-backed work, follow [the repository workflow](../miniplm/SKILL.md).
Resolve the master and separate native part revisions together; preserve their
relative references in local `cad/` and `cad/components/` working copies. Save
editable sources with their dependency record and derived exports. A converted
preview or automatically imported folder is not a verified assembly baseline.
Every saved `.FCStd` must have a matching `.step` from that source revision under
`cad/exports/`, mirroring native subfolders such as `components/`. Recompute,
export and check the STEP geometry/units; a missing or stale companion makes the
package incomplete. Include editable Blender scenes in `cad/blender/<scene>/`
with packed/portable dependencies and final images in `renders/<purpose>/`.
Name top-level assemblies and subassemblies `<name>_assembly.<extension>`, with
the suffix immediately before the extension. Matching exports retain the stem:
`wheel_assembly.FCStd` pairs with `wheel_assembly.step`. Use the same suffix for
Blender files representing assemblies, such as `wheel_assembly.blend`.
Place non-embedded CAD imports and externally linked components in
`cad/components/`, or the owning Blender scene's `components/` subfolder for linked
Blender files. Include their transitive external dependencies and follow the same
assembly naming, native/STEP and revision rules. Fully embedded components need
no separate file, upload or per-component export; verify the saved parent is
self-contained before omitting external sources. The parent's STEP remains required.

## Design workflow

1. Define function, envelope, masses, loads, motion limits, stiffness and first natural frequency where relevant, alignment, temperature, moisture, materials, surfaces and manufacturing process. Use units and a consistent coordinate frame.
2. Identify critical interfaces: mating faces, datum/fastener/shaft/optical axes, electronics mounts, cable bending and RF clearances. Specify tolerances and a plausible inspection method, not merely nominal dimensions.
3. Prefer **native, editable parametric FreeCAD documents** for designed parts: named parameters, constrained sketches and deterministic features. STEP/STL/mesh/renders are exchange/export artifacts, not the master model. Preserve user changes, broken references and feature history.
4. Choose fit and fabrication strategy deliberately (FDM/resin printing, sheet metal, composites, casting or machining). Account for anisotropy, creep, shrinkage, support/access and achievable tolerances.
5. Calculate likely failure modes: section stress, deflection, fastener preload, fatigue, vibration, thermal expansion, weather sealing, centre of mass and mechanical stops. Seek $simulation-engineering when the model is justified; validate critical dimensions and loads physically.
6. Recompute/check the native model, geometry validity, interference and access, assembly travel, export units/orientation, drawing dimensions and fabrication constraints. Record limitations honestly.
7. Request $design-review for design/prototype gate decisions, and a multidisciplinary review when mounting stiffness, vibration, motion, optical alignment, motor effort or thermal performance affects other subsystems.

## CAD inspection and release evidence

When FreeCAD Python bindings are available, run the read-only model inspector:

```sh
python SKILLS/mechanical-engineering/scripts/inspect_freecad.py path/to/model.FCStd --output path/to/new-cad-report.json
```

Use its source SHA, geometry/recompute metrics and report artifact in the
shared [gate checker](../engineering-workflow/references/gate-engine.md).
The helper does not inspect all tolerances, collision pairs or FEM physics.
Do not fabricate metrics when FreeCAD is unavailable. For an adopted project
gate config, run the shared engine for the requested stage and report blockers.

## Handoff

Provide authoritative CAD path and revision, parameter list with units, assumptions, materials, mass properties, load cases, tolerance stack, manufacturing method, drawing/export provenance, applicable analysis and inspection/test plan. Distinguish CAD recompute success, FEM results and measured physical fit.

A valid mesh or attractive render is not proof of machinability, fit, strength or accuracy. If tools, source files, material data or physical measurements are unavailable, mark the relevant checks blocked or not run. Do not order parts or assert that a prototype was built.
