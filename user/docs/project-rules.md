# Project rules and file layout

`user/` contains files a person needs to understand, edit, simulate, build or use
the hardware. `agent/` contains the automation and working records used to produce
those deliverables. The split applies to every module.

```text
rsim/
├── README.md
├── AGENTS.md
├── user/
│   ├── docs/                         project-wide user documentation
│   └── modules/
│       └── <module>/
│           ├── README.md             purpose, status and links to deliverables
│           ├── cad/                  native editable assemblies and drawings
│           │   ├── components/       separate native part files, when used
│           │   └── exports/          STEP, STL, DXF and other CAD handoffs
│           ├── electronics/
│           │   ├── kicad/            native projects and necessary local libraries
│           │   ├── bom/              readable bill of materials and sourcing
│           │   └── fabrication/
│           │       ├── gerbers/
│           │       ├── drill/
│           │       └── assembly/     placement and assembly handoffs
│           ├── sim/
│           │   ├── fem/
│           │   ├── thermal/
│           │   └── spice/
│           ├── docs/                 reports, build and operating instructions
│           ├── reference/            datasheets, vendor CAD and references
│           └── renders/              final images and animations
└── agent/
    ├── scripts/                      automation and checking tools
    ├── skills/                       engineering/documentation skill packages
    ├── config/modules/<module>/      configuration and manifests
    ├── evidence/<module>/<run>/      checks, logs and provenance
    ├── objects/<module>/<run>/       caches, environments and intermediates
    └── docs/                         agent/toolchain maintenance instructions
```

`wheel` is an example module name, not a committed design scope. Use lowercase
letters, digits and hyphens for module names. Create a module when work on it is
requested. Add `cad/components/` when separate component files are used.

## Artifact placement

Paths below are relative to `user/modules/<module>/` unless they start with `agent/`.

| Artifact | Destination |
| --- | --- |
| Native FreeCAD master, assembly, drawing or editable Blender scene | `cad/` |
| Separate native designed part files | `cad/components/` |
| STEP, STL, DXF and exchange geometry | `cad/exports/` |
| KiCad schematic, board, project and required local libraries | `electronics/kicad/` |
| Human-readable BOM, including CSV | `electronics/bom/` |
| Gerber, drill and assembly files | Matching `electronics/fabrication/` subfolder |
| Reproducible FEM, thermal and SPICE inputs, selected plots and useful datasets | Matching `sim/` subfolder |
| Reports, requirements, decisions and build instructions | `docs/` |
| External datasheets, drawings, vendor CAD and reference documents | `reference/` |
| Final review or presentation render | `renders/` |
| Generation scripts, macros and post-processing code | `agent/scripts/<module>/` |
| Gate config and machine-readable agent manifests | `agent/config/modules/<module>/` |
| Evidence JSON, solver logs, check records and verification screenshots | `agent/evidence/<module>/<run>/` |
| Scratch meshes, solver work files and temporary previews | `agent/objects/<module>/<run>/` |

File encoding does not decide ownership: native KiCad project files and solver
inputs stay with the design even if they use JSON or another text format. Agent
bookkeeping JSON stays under `agent/`.

Keep module-specific documentation with its module; put cockpit-wide user
guidance in `user/docs/`. For shared references, choose an owning module and link
to it from others. Preserve titles, source URLs, revisions and access dates when
available. Keep download/checksum records under `agent/evidence/`.

## Sources and results

Native editable CAD and KiCad files are authoritative. Meshes, fabrication
exports and renders are derived; record source revision and tool versions in the
matching agent evidence. State units and coordinate frames at design interfaces.

Reports should state assumptions, criteria, results and remaining work in readable
form and link to detailed evidence. Distinguish calculated, simulated, reviewed
and physically measured results. A render or a passing software check does not
establish physical fit or readiness.

Use relative links. Link to scripts under `agent/` instead of copying automation
into user folders. Do not place logs, caches, scratch, evidence JSON or `.gitkeep`
placeholders under `user/`.

## Tools and discovery

Use pacman to install and maintain FreeCAD, KiCad and Blender. Prefer headless
FreeCAD execution, `kicad-cli` for exports/ERC/DRC, and Blender background rendering.
GUI-only capabilities require a GUI session. Install optional simulation solvers
when needed; installing FreeCAD does not establish that FEM/thermal solvers work.

MCP integrations and their Python environments belong under `agent/`. Required
`.agents/skills` and `.codex/config.toml` discovery entry points may link into
`agent/`. These, Git metadata and root navigation/instruction files are limited
exceptions to the directory split.
