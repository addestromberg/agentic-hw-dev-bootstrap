# HARDWARE project instructions

Read [the project rules](user/docs/project-rules.md) before creating or moving files.
These rules apply to this entire workspace.

- User deliverables belong in `user/`. Each hardware module owns its CAD,
  electronics, simulations, documentation, references and renders under
  `user/modules/<module>/`.
- Agent code, configuration, JSON records, logs, evidence, caches and intermediate
  files belong in `agent/`, grouped by the same module name when applicable.
  Native application formats required to edit or reproduce a design are user
  deliverables even when their underlying encoding is structured text.
- Keep native editable CAD and KiCad sources authoritative. Retain separate CAD
  parts under `cad/components/` when the model uses separate component files.
- Put source references under the owning module's `reference/` and final renders
  under its `renders/`. Put reports and build instructions under its `docs/`.
- Use pacman for FreeCAD, KiCad and Blender. Do not substitute Conda, AppImages,
  pip application builds or extracted package overlays without user direction.
  MCP server Python packages may use isolated environments under `agent/objects/`.
- Use `rsim_freecad.execute_code_headless` for FreeCAD. For Blender's MCP Python
  and render tools, explicitly pass `transport="headless"`; their upstream
  default selects an optional GUI bridge. Read `agent/docs/toolchain.md` for setup.
- Root `README.md`, `AGENTS.md`, `.gitignore`, and application-required discovery
  entry points are exceptions to the `user/` versus `agent/` split. Keep the
  actual agent skill/configuration content under `agent/` where possible.

## Skills

Load the relevant skill from `agent/skills/` for hardware work:

| Skill | Apply to |
| --- | --- |
| [engineering-workflow](agent/skills/engineering-workflow/SKILL.md) | Requirements, coupled disciplines, hardware baselines and readiness claims |
| [electronics-development](agent/skills/electronics-development/SKILL.md) | Circuits, PCB work, electrical checks and board release |
| [mechanical-engineering](agent/skills/mechanical-engineering/SKILL.md) | Parametric CAD, assemblies, fits, loads and fabrication |
| [simulation-engineering](agent/skills/simulation-engineering/SKILL.md) | FEM, thermal, SPICE and other engineering analyses |
| [design-review](agent/skills/design-review/SKILL.md) | Evidence-based design assessment |
| [hardware-documentation](agent/skills/hardware-documentation/SKILL.md) | Reports, assembly/build instructions and module documentation |

The five imported engineering skills are copied from SKYwatch. In their example
commands, resolve `SKILLS/` to this project's `agent/skills/`. Interpret an owning
project's evidence/config/log paths as `agent/evidence/<module>/`,
`agent/config/modules/<module>/`, and `agent/objects/<module>/` here. Their
SKYwatch-specific examples are not RSIM design requirements. Do not import SKYwatch
station architecture, requirements, or readiness claims into this project.

Follow existing session instructions on delegation. A preference for independent
review does not itself authorize spawning another agent; label self-review honestly.
Keep calculated, simulated and physically measured results distinct.
