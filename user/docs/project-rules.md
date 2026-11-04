# Project rules and file layout

`user/` contains files a person needs to understand, edit, simulate, build or use
the hardware. `agent/` contains the automation and working records used to produce
those deliverables. The split applies to every module's local working files.
MiniPLM is the repository for saved hardware deliverables and their revisions.
This bootstrap supplies reusable instructions and tooling; it has no assigned
MiniPLM product, iteration or hardware baseline.
Root `SPECIFICATION.md` is the project-wide human deliverable that defines the
product goal and completion criteria. It is an explicit exception to the local
`user/` placement rule, alongside root navigation/instruction files.

If MiniPLM is unavailable or no usable repository target is found, continue with
the same local directory structure. Report that deliverables are local-only and
have no PLM version control or revision history. Directories and local hash
records do not supply version control; bootstrap Git commits do not version
these product files unless a separate project workflow explicitly does so.

```text
$pwd/
├── README.md
├── AGENTS.md
├── SPECIFICATION.md                 overall product goal and approved baseline
├── user/
│   ├── docs/                         project-wide user documentation
│   └── modules/
│       └── <module>/
│           ├── README.md             purpose, status and links to deliverables
│           ├── SPECIFICATION.md      requirements and approved development baseline
│           ├── cad/                  native editable assemblies and drawings
│           │   ├── components/       separate parts and non-embedded CAD imports
│           │   ├── blender/<scene>/  .blend and required scene resources
│           │   └── exports/          matching STEP; mirror native subfolders
│           ├── electronics/
│           │   ├── kicad/<board>/    native project, schematics, PCB and library tables
│           │   │   └── libraries/    symbols/, footprints/, 3dmodels/
│           │   ├── bom/<board>/      readable bill of materials and sourcing
│           │   └── fabrication/<board>/
│           │       ├── gerbers/
│           │       ├── drill/
│           │       └── assembly/     placement and assembly handoffs
│           ├── firmware/<target>/    source, build inputs and build/flash guide
│           ├── software/<app>/       source, build inputs and build/use guide
│           ├── sim/<discipline>/<study>/
│           │   ├── inputs/           reproducible native models and solver inputs
│           │   ├── reports/          human-readable simulation report and figures
│           │   └── results/          selected useful data, not solver scratch/logs
│           ├── docs/                 reports, build and operating instructions
│           ├── reference/            datasheets, vendor CAD and references
│           └── renders/<purpose>/    final images and animations
└── agent/
    ├── scripts/                      automation and checking tools
    ├── templates/                    reusable document scaffolds
    ├── skills/                       engineering/documentation skill packages
    ├── config/modules/<module>/      configuration and manifests
    ├── evidence/<module>/<run>/      checks, logs and provenance
    ├── objects/<module>/<run>/       caches, environments and intermediates
    └── docs/                         agent/toolchain maintenance instructions
```

`wheel` is an example module name, not a committed design scope. Use lowercase
letters, digits and hyphens for module names. Create a module when work on it is
requested. Add `cad/components/` when separate component files are used.
Create board, scene, study, firmware and software subfolders only when needed.
The simulation discipline can be `fem`, `thermal`, `spice` or another relevant
discipline. Keep each board, scene, study, target and application grouped; do not
put unrelated outputs in one root folder. Preserve established native project
layouts and necessary shared-library references when adopting an existing design.

## Specification before development

Use the [PLM lifecycle and stage sign-off](plm-lifecycle.md) for project/module
progress: Conceive, Specification, Concept design, Design, Detailed design,
Validation and analysis (simulation), Tool design, Realise, Plan manufacturing,
Manufacture, Build/assemble, Test (quality control). Maintain stage progress and
real owner decisions in each specification. Approvals flow from the project
requirements into modules; module and integration evidence support project gates.

Complete and approve repository-root `SPECIFICATION.md` for the agreed stage
before product implementation. It defines the overall product goal for the
engineering agent, project requirements, shared constraints, module allocation,
interfaces and objective system completion/verification criteria. The project
baseline directs module work; do not invent the goal from the bootstrap name.

Each module owns `user/modules/<module>/SPECIFICATION.md`. Complete it for the
agreed development scope and obtain the user's or designated owner's approval
of that exact revision before starting module CAD, circuit, PCB, firmware/software
implementation or design-validation work. Reference the approved project-spec
revision and the project requirement IDs allocated to that module. Both the
project and affected module baselines must be approved and consistent. Read the
[specification gate](../../agent/skills/engineering-workflow/references/module-specification.md)
for the review criteria and change procedure. A generated file, unchecked template
or `APPROVED` label without an actual decision does not satisfy the gate.

Requirements discovery, source research and explicitly scoped feasibility studies
can help complete the specification. Keep their preliminary assumptions and
outputs identified; they do not establish an approved module design. Approval
already given for the same revision and scope remains valid. Do not invent
requirements or approval to proceed. Later changes to scope or requirements need
impact review and approval of the revised baseline before affected implementation.
The same gate applies in local-only mode; the bootstrap itself has no approved
project/module specifications or development scope.

## Assembly filenames

Name assembly files `<name>_assembly.<extension>`, with the lowercase `_assembly`
suffix immediately before the extension. Apply this to top-level assemblies and
subassemblies, locally and in MiniPLM. Examples: `wheel_assembly.FCStd`,
`wheel_assembly.step` and `wheel_assembly.blend` when the Blender file represents
the assembly. Matching native and exported assembly files keep the same stem,
including `_assembly`. Put any other name qualifiers before the suffix.

Individual parts and Blender scenes used only for presentation keep descriptive
names appropriate to their role. When renaming an existing assembly, update its
linked references, companion exports, documentation and repository mapping
together, preserving revision history through supported repository operations.

## Imported and embedded components

Put non-embedded CAD component imports and externally linked part/assembly files
under `cad/components/`, including vendor geometry actually used as a file
dependency. For Blender, put externally linked component files under the owning
scene's `cad/blender/<scene>/components/`. Preserve portable relative references
and include all transitive external component dependencies in the local package
and MiniPLM save.

These files follow the same rules as other components: `_assembly` for assemblies
and subassemblies, matching STEP companions for separately saved `.FCStd` files,
native Blender files/assets where applicable, directory grouping and revision
traceability. An imported STEP already serves as STEP geometry; no duplicate
native wrapper is required just for packaging. Vendor CAD retained only as a
reference belongs under `reference/`; an active external dependency belongs in
the appropriate `components/` folder.

A component fully embedded in the saved parent document needs no separate
component file, upload or per-component STEP export. Check that it is genuinely
self-contained, with no remaining external file dependency, before omitting its
source file. The parent's STEP and other deliverables remain required. Do not
extract embedded components solely to populate a `components/` folder.

## Artifact placement

Paths below are relative to `user/modules/<module>/` unless they start with `agent/`
or are explicitly identified as repository-root paths.

| Artifact | Destination |
| --- | --- |
| Overall product goal, project requirements and approved baseline | Repository-root `SPECIFICATION.md` |
| Module requirements and approved development baseline | `SPECIFICATION.md` at module root |
| Native FreeCAD master, assembly or drawing | `cad/` |
| Native jigs, fixtures, moulds and tooling; matching exports | `cad/tooling/` and `cad/exports/tooling/` |
| Separate native parts and non-embedded CAD component imports | `cad/components/` |
| Editable Blender scene and packed/portable assets | `cad/blender/<scene>/` |
| Non-embedded Blender component files | `cad/blender/<scene>/components/` |
| STEP companion for every FreeCAD file; other requested CAD exports | `cad/exports/`, mirroring native subfolders |
| KiCad schematic, referenced sheets, PCB, project and library tables | `electronics/kicad/<board>/` |
| Required custom symbols, footprints and 3D models | `electronics/kicad/<board>/libraries/{symbols,footprints,3dmodels}/` |
| Human-readable BOM, including CSV | `electronics/bom/<board>/` |
| Gerber, drill and assembly files | Matching `electronics/fabrication/<board>/` subfolder |
| Product firmware source, build inputs, tests and build/flash instructions | `firmware/<target>/` |
| Product software source, resources, build inputs, tests and build/use instructions | `software/<app>/` |
| Requested firmware/software release binaries or distributables | Matching `firmware/<target>/releases/` or `software/<app>/releases/` |
| Reproducible simulation model and inputs | `sim/<discipline>/<study>/inputs/` |
| Readable simulation report, figures and selected useful data | Matching study's `reports/` and `results/` |
| Reports, requirements, decisions and build instructions | `docs/` |
| Manufacturing plans, readable build/production records and QC reports | Relevant `docs/manufacturing/` or `docs/quality/` subfolder |
| External datasheets, drawings, reference-only vendor CAD and reference documents | `reference/` |
| Final review or presentation render | `renders/<purpose>/` |
| Agent generation scripts, macros and post-processing automation | `agent/scripts/<module>/` |
| Gate config and machine-readable agent manifests | `agent/config/modules/<module>/` |
| Evidence JSON, solver logs, check records and verification screenshots | `agent/evidence/<module>/<run>/` |
| Scratch meshes, solver work files and temporary previews | `agent/objects/<module>/<run>/` |

File encoding does not decide ownership: native KiCad project files, solver
inputs and firmware/software build manifests and lockfiles stay with the design
even if they use JSON or another text format. Source required to build or operate
the product belongs under `user/`, even if an agent wrote it. Agent bookkeeping
JSON stays under local `agent/` and is excluded from PLM.

Keep module-specific documentation with its module; put project-wide user
guidance in `user/docs/`. For shared references, choose an owning module and link
to it from others. Preserve titles, source URLs, revisions and access dates when
available. Keep download/checksum records under `agent/evidence/`.

## Sources and results

Native editable CAD and KiCad files are authoritative. Meshes, fabrication
exports and renders are derived; record source revision and tool versions in the
matching agent evidence. State units and coordinate frames at design interfaces.

Every saved FreeCAD `.FCStd` needs a corresponding `.step` exported from that
native revision. Mirror its path below `cad/` in `cad/exports/`: for example,
`cad/components/shaft.FCStd` pairs with `cad/exports/components/shaft.step`.
Recompute and check exported geometry, units and orientation. A missing or stale
STEP makes the handoff incomplete. Include editable `.blend` files for Blender
work, with required resources packed or saved in portable scene subfolders.

Reports should state assumptions, criteria, results and remaining work in readable
form and link to detailed evidence. Distinguish calculated, simulated, reviewed
and physically measured results. A render or a passing software check does not
establish physical fit or readiness.

Use relative links. Link to scripts under `agent/` instead of copying automation
into user folders. Do not place logs, caches, scratch, evidence JSON or `.gitkeep`
placeholders under `user/`.

## MiniPLM repository and local working copies

Use the [MiniPLM workflow](../../agent/skills/miniplm/SKILL.md) for repository work.
Resolve the intended project (upstream product), iteration and exact file
revisions before editing an existing design. Reuse the downstream project's
organization and select the product explicitly. The MiniPLM project is the
product, not a directory. Map local `user/modules/<module>/` to `<module>/`
inside the selected project iteration. For example, local
`user/modules/wheel/cad/` maps to `wheel/cad/`; the module specification maps to
`wheel/SPECIFICATION.md`. Retain the module name and its discipline subfolders;
omit the local `user/modules/` wrapper and do not add a `product/` folder.
The repository-root project `SPECIFICATION.md` maps to `SPECIFICATION.md` at the
selected iteration's root, above module folders such as `wheel/`.
Map `user/docs/` to `docs/` when those project-wide documents belong to the selected
product. Keep relative
references between native assemblies/parts and KiCad projects/libraries intact.
Record explicit destinations for multi-module work so unrelated files or
same-named documents are not merged. Check published document links against the
remote mapping, since links through local wrapper directories may need adjustment.
Each upload must select the correct native MiniPLM folder; local file paths do
not create remote folders automatically. Keep custom symbols, footprints, library
tables and other inputs needed to reopen each KiCad project with that project.

Edit and check local files in the layout above, then save the scoped deliverables
to MiniPLM with revision descriptions and pinned source/dependency identities.
Keep local working copies; an upload is not permission to delete them. Do not
overwrite local edits or newer remote work without reconciling the versions.
Record local byte hashes alongside MiniPLM file/revision IDs so exports, checks,
reports and saved packages can be tied to the sources actually used.

Downstream target mappings belong under `agent/config/`, with module-specific
values under `agent/config/modules/<module>/`. Write receipts and dependency
records belong under `agent/evidence/<module>/<run>/` and remain local. Publish
only scoped human-facing documents and product deliverables: native CAD with STEP
companions, Blender scenes/assets, renders, simulation inputs/readable reports,
complete electrical projects, firmware/software source and required build inputs,
references and requested fabrication/release outputs.

Never upload agent notes (including `.md`), raw logs, temporary/evidence JSON,
gate reports, machine manifests, upload receipts, caches, tool environments,
solver scratch, build caches, backups, autosaves, locks or secrets. This applies
to individual files and archive contents. Produce readable reports from evidence
rather than copying raw records into PLM. Required native/build files that happen
to contain JSON are deliverables, not temporary agent records. Existing local
gate checkers continue to use real files and SHA-256 hashes, not remote IDs.

Before saving, make an explicit local inventory of deliverables, companions,
dependencies and destination folders. Apply the detailed
[publish policy](../../agent/skills/miniplm/references/publish-policy.md).
Keep the machine inventory local; publish a readable package index when useful.
An allowed folder is not permission to upload every file in it.

In local-only mode, apply the same grouping, native/STEP, dependency and report
requirements and report the local paths. Do not invent PLM identities or claim
synchronization. When PLM becomes available, inspect and reconcile its current
revisions before uploading local work. Missing remote sources remain missing;
fallback storage cannot substitute for native inputs that were never retrieved.

### Connected and local-only operation

| Condition | Required behavior |
| --- | --- |
| Available MiniPLM integration/session and resolved target | Use exact native revisions/dependencies, perform local work and checks, then save the explicit deliverable inventory and verify the saved revisions/destinations. |
| Missing tools, unavailable service/session, missing target, or a local-only request | Use local-only mode without guessing a remote target or making setup a prerequisite. Apply the same specifications, lifecycle, file grouping and companion rules; report local paths and lack of PLM version history. |
| Required native inputs are unavailable | Identify the missing inputs and continue only work with sufficient sources; metadata, rendered previews and fallback folders do not recover a missing native file. |
| Interrupted/uncertain write | Keep local work and per-file outcomes. Stop dependent writes, report the uncertain save and inspect server state before retrying; preserve any confirmed saved revisions. |
| Return from local-only mode | Reconcile local hashes/source identities and current remote state before saving. Resolve divergence and collisions; do not overwrite local edits or silently create duplicate revisions. |

Local-only storage does not supply version control by itself. Adopt a separate
design-file version-control workflow only when explicitly established by the
project. Repository availability and lifecycle sign-off are independent: absent
PLM does not waive engineering gates, and a connected repository does not approve
an engineering stage.

Git maintains the bootstrap and its automation. A Git commit, MiniPLM iteration,
folder or preview alone does not pin a complete design package. Record exact
member revisions for a handoff and distinguish a successful repository save from
engineering approval. Do not claim files are saved until their writes are verified;
report partial or uncertain saves explicitly.

Template maintenance does not create remote products, iterations, folders or
files. Keep this bootstrap free of instance-specific IDs, credentials and assumed
hardware requirements. Establish those only for actual downstream project work.

## Tools and discovery

Use pacman to install and maintain FreeCAD, KiCad and Blender. Prefer headless
FreeCAD execution, `kicad-cli` for exports/ERC/DRC, and Blender background rendering.
GUI-only capabilities require a GUI session. Install optional simulation solvers
when needed; installing FreeCAD does not establish that FEM/thermal solvers work.

MCP integrations and their Python environments belong under `agent/`. Required
`.agents/skills` and `.codex/config.toml` discovery entry points may link into
`agent/`. These, Git metadata and root navigation/instruction files are limited
exceptions to the directory split; root `SPECIFICATION.md` is the explicit
project-wide specification exception.
