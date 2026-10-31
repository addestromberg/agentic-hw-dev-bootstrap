---
name: mechanical-engineering
description: Design and review mechanical assemblies, native parametric CAD, materials, tolerances, 3D-printing or fabrication, structural and thermal interfaces, fit and motion. Use for FreeCAD models, mounts, housings, moving stages and manufacturing drawings; not for PCB-only electrical design.
---

# Mechanical engineering

Use $engineering-workflow for cross-discipline requirements and formal handoffs. Read the owning project's native CAD source, assembly context, operating conditions and [mechanical checks](references/design-checklist.md) before editing.

## Design workflow

1. Define function, envelope, masses, loads, motion limits, stiffness and first natural frequency where relevant, alignment, temperature, moisture, materials, surfaces and manufacturing process. Use units and a consistent coordinate frame.
2. Identify critical interfaces: mating faces, datum/fastener/shaft/optical axes, electronics mounts, cable bending and RF clearances. Specify tolerances and a plausible inspection method, not merely nominal dimensions.
3. Prefer **native, editable parametric FreeCAD documents** for Skywatch designed parts: named parameters, constrained sketches and deterministic features. STEP/STL/mesh/renders are exchange/export artifacts, not the master model. Preserve user changes, broken references and feature history.
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
