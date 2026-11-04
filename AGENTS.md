# HARDWARE project instructions

Read [the project rules](user/docs/project-rules.md) before creating or moving files.
These rules apply to this entire workspace.
Read root [SPECIFICATION.md](SPECIFICATION.md) for the product goal, approved
scope and project acceptance criteria before engineering work. Its initial draft
is a bootstrap scaffold, not an approved hardware assignment.
Follow [the PLM lifecycle](user/docs/plm-lifecycle.md) for ordered stages and actual
owner sign-off. Project requirements/approvals flow down into modules; module
evidence and integration results support project decisions. Preserve stage scope
and revision traceability; an early design approval does not approve manufacture
or physical testing.

- User deliverables belong in `user/`. Each hardware module owns its CAD,
  electronics, firmware/software, simulations, documentation, references and renders under
  `user/modules/<module>/`.
- Product implementation needs an approved repository-root `SPECIFICATION.md`;
  each affected module also needs its own complete, approved root `SPECIFICATION.md`
  tracing its scope to project requirements. Follow the specification gates in
  `agent/skills/engineering-workflow/references/module-specification.md`.
  Requirements discovery and explicitly scoped feasibility work may prepare the
  spec; an empty scaffold or invented approval never authorizes development.
- Agent code, configuration, JSON records, logs, evidence, caches and intermediate
  files belong in `agent/`, grouped by the same module name when applicable.
  Native application formats required to edit or reproduce a design are user
  deliverables even when their underlying encoding is structured text.
- Keep native editable CAD and KiCad sources authoritative. Retain separate CAD
  parts under `cad/components/` when the model uses separate component files.
- Non-embedded CAD imports and externally linked components belong under
  `cad/components/`; linked Blender components belong in the scene's `components/`
  subfolder. Include their external dependencies and apply the same naming,
  companion-file and revision rules. Fully embedded, self-contained components
  need no separate files or uploads; the parent still needs its required exports.
- Name assemblies and subassemblies `<name>_assembly.<extension>`; put `_assembly`
  immediately before the extension and retain the same stem in matching exports
  (for example `wheel_assembly.FCStd` and `wheel_assembly.step`).
- Every saved `.FCStd` needs a corresponding `.step` from the same native revision
  under `cad/exports/`, mirroring source subfolders. Include `.blend` scenes and
  their portable assets, final renders and readable simulation reports in scope.
- Use MiniPLM as the repository for saved hardware deliverables and revisions;
  local `user/` files are working copies. Follow `agent/skills/miniplm/SKILL.md`
  for target selection, retrieval, saves and revision/dependency records. Git
  maintains the bootstrap instructions and automation; it does not identify a
  saved MiniPLM design revision.
- If MiniPLM or a usable target is unavailable, continue in matching local
  directories. Report local-only storage without PLM version control/history;
  directories and bootstrap Git commits do not substitute for product versioning.
  Reconcile files with the repository before a later upload.
- PLM contains human-facing documents and product files, never agent records,
  logs, temporary/evidence JSON, machine manifests, caches or scratch, even inside
  archives. Keep those local under `agent/`. Required native/build files may use
  JSON. Follow `agent/skills/miniplm/references/publish-policy.md` before saving.
- Keep `user/modules/<module>/` locally; map it to `<module>/` inside the selected
  MiniPLM project iteration, for example `wheel/SPECIFICATION.md` and `wheel/cad/`.
  The project is the product, not a directory. Omit the `user/modules/` wrapper
  in PLM while retaining the module name and discipline folders. Group each KiCad board with its
  schematic sheets, PCB, custom symbols, footprints and library tables. Product
  firmware/software source and required build inputs belong under the module's
  `firmware/<target>/` and `software/<app>/`, separately from agent scripts.
- This is a bootstrap, not an active hardware product. Do not create MiniPLM
  projects, iterations or files while maintaining the template. Keep instance
  mappings in downstream `agent/config/`, and credentials out of the repository.
- Put source references under the owning module's `reference/` and final renders
  under its `renders/<purpose>/`. Put reports and build instructions under `docs/`,
  with simulation reports in their study's `sim/<discipline>/<study>/reports/`.
- Use pacman for FreeCAD, KiCad and Blender. Do not substitute Conda, AppImages,
  pip application builds or extracted package overlays without user direction.
  MCP server Python packages may use isolated environments under `agent/objects/`.
- Use `rsim_freecad.execute_code_headless` for FreeCAD. For Blender's MCP Python
  and render tools, explicitly pass `transport="headless"`; their upstream
  default selects an optional GUI bridge. Read `agent/docs/toolchain.md` for setup.
- Root `README.md`, `AGENTS.md`, `.gitignore`, and application-required discovery
  entry points, plus human-facing project `SPECIFICATION.md`, are exceptions to
  the `user/` versus `agent/` split. Keep the
  actual agent skill/configuration content under `agent/` where possible.

## Skills

Load the relevant skill from `agent/skills/` for hardware work:

| Skill | Apply to |
| --- | --- |
| [miniplm](agent/skills/miniplm/SKILL.md) | Repository targets, native file revisions, local working copies and saved hardware handoffs |
| [engineering-workflow](agent/skills/engineering-workflow/SKILL.md) | Requirements, coupled disciplines, hardware baselines and readiness claims |
| [electronics-development](agent/skills/electronics-development/SKILL.md) | Circuits, PCB work, electrical checks and board release |
| [mechanical-engineering](agent/skills/mechanical-engineering/SKILL.md) | Parametric CAD, assemblies, fits, loads and fabrication |
| [simulation-engineering](agent/skills/simulation-engineering/SKILL.md) | FEM, thermal, SPICE and other engineering analyses |
| [design-review](agent/skills/design-review/SKILL.md) | Evidence-based design assessment |
| [hardware-documentation](agent/skills/hardware-documentation/SKILL.md) | Reports, assembly/build instructions and module documentation |

The five imported engineering skills originated in SKYwatch and are adapted for
this bootstrap's file layout and MiniPLM workflow. In their example
commands, resolve `SKILLS/` to this project's `agent/skills/`. Interpret an owning
project's evidence/config/log paths as `agent/evidence/<module>/`,
`agent/config/modules/<module>/`, and `agent/objects/<module>/` here. Their
SKYwatch-specific examples are not requirements for a downstream project. Do not import SKYwatch
station architecture, requirements, or readiness claims into this project.

Follow existing session instructions on delegation. A preference for independent
review does not itself authorize spawning another agent; label self-review honestly.
Keep calculated, simulated and physically measured results distinct.
