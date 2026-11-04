# Deliverables and directory discipline

Read this before preparing a MiniPLM save. Publish files a person needs to read,
open, edit, build, reproduce or use the product. Keep agent operations and their
records local. A file's purpose decides whether it belongs; its extension alone
does not. A readable `.md` agent transcript is still an agent record, while a
required KiCad or software manifest may legitimately contain JSON.

## Folder mapping

The selected MiniPLM project is the product, not a directory. Within its selected
iteration, local `user/modules/<module>/` maps to a named `<module>/` folder.
Keep `user/modules/` locally and omit that wrapper in PLM. For example, inside the
chosen project/iteration:

| Local path | Path within the selected product iteration |
| --- | --- |
| Repository-root `SPECIFICATION.md` | `SPECIFICATION.md` |
| `user/modules/wheel/SPECIFICATION.md` | `wheel/SPECIFICATION.md` |
| `user/modules/wheel/cad/wheel_assembly.FCStd` | `wheel/cad/wheel_assembly.FCStd` |
| `user/modules/wheel/cad/components/hub.FCStd` | `wheel/cad/components/hub.FCStd` |
| `user/modules/wheel/electronics/kicad/controller/` | `wheel/electronics/kicad/controller/` |
| `user/modules/wheel/docs/build.md` | `wheel/docs/build.md` |

`wheel` is illustrative, not a template target. Select the product explicitly;
do not derive its identity from a local folder name. Project-wide human documents
under `user/docs/` map to `docs/` when they belong to that product. Record explicit
destinations when saving several local modules and check for collisions, including
same-named README or documentation files. Preserve discipline and dependency
subfolders below each module folder. Do not create a `product/` directory to
represent the project. For existing
assets, inspect their mappings before writes; template maintenance does not move
remote files.

Validate document navigation against the published paths. Links through local
`user/modules/` wrappers or to project-wide documents may need adjusted links in
the published document or returned MiniPLM links. Preserve usable local originals
and do not publish links that assume agent files are available remotely.

When MiniPLM is unavailable or no usable target is found, use the same hierarchy
under local `user/modules/<module>/` and `user/docs/`. Work continues locally;
report that directory-only storage has no PLM version control or revision history.
The following companion, dependency and file-separation rules still apply.

| Deliverable | Path below local / PLM module folder | Required content and companions |
| --- | --- | --- |
| Module specification | `SPECIFICATION.md` | Human-readable requirements, development scope, acceptance/verification plan and actual approval for the baseline used by development |
| FreeCAD assembly | `cad/<name>_assembly.FCStd` | Corresponding `cad/exports/<name>_assembly.step`, from the same native revision |
| Other native FreeCAD model | `cad/<name>.FCStd` | Corresponding `cad/exports/<name>.step`, from the same native revision |
| Separate FreeCAD parts | `cad/components/<part>.FCStd` | Corresponding `cad/exports/components/<part>.step`; preserve assembly references |
| Non-embedded CAD imports | `cad/components/` | Include actively linked/imported component source files and their external dependencies; apply native/STEP and assembly naming rules |
| Blender source | `cad/blender/<scene>/<scene>.blend` | Pack assets or include required textures, linked scenes and other resources under this scene directory with portable references |
| Non-embedded Blender components | `cad/blender/<scene>/components/` | Include linked component files and their external dependencies, preserving portable relative references |
| Other CAD handoffs | `cad/exports/` with source-relative subfolders | Requested STL/DXF/drawings; these do not replace the native files or required STEP |
| Native tooling/jigs/fixtures | `cad/tooling/` and `cad/exports/tooling/` | Editable tooling sources, matching STEP companions and relevant tolerances/inspection information |
| KiCad board project | `electronics/kicad/<board>/` | `.kicad_pro`, `.kicad_sch`, referenced sheets and `.kicad_pcb`; preserve the project's relative sheet paths |
| Custom KiCad libraries | `electronics/kicad/<board>/libraries/` | `symbols/*.kicad_sym`, `footprints/*.pretty/`, `3dmodels/`, and required `sym-lib-table`/`fp-lib-table` at the project root |
| BOM and fabrication | `electronics/bom/<board>/` and `electronics/fabrication/<board>/{gerbers,drill,assembly}/` | Human-readable BOM and requested manufacturing/assembly handoffs tied to the board source revision |
| Firmware | `firmware/<target>/` | Editable source, headers, build configuration, dependency manifests/locks, relevant tests, readable build/flash instructions and requested release images in `releases/` |
| Product software | `software/<app>/` | Editable source, required resources, build/package files, dependency manifests/locks, relevant tests and readable build/use instructions; requested distributables in `releases/` |
| Simulation study | `sim/<discipline>/<study>/` | Reproducible model/inputs in `inputs/`, human-readable report and its figures in `reports/`, selected useful data in `results/` |
| Final renders | `renders/<purpose>/` | Final images/animations, with source scene/model revision identified in a human-readable index when needed |
| Human documentation | `docs/` and module `README.md` | Requirements, decisions, review summaries, assembly, operating and build guides; `.md`, PDF and other useful readable formats |
| Lifecycle and physical-stage reports | Specification sign-off sections and relevant `docs/manufacturing/` or `docs/quality/` | Readable actual decisions, manufacturing/as-built identities, inspections, deviations and QC results; planned work stays identified as planned |
| External references | `reference/<topic>/` | Required datasheets, reference-only vendor CAD or reference documents, with source/revision identified |

Create only the directories needed by the actual deliverables. Use stable,
descriptive file and folder names. A board, study, target or app groups its own
files; do not dump all schematics, code, figures or exports into one root folder.
Keep existing usable native layouts intact, including necessary shared libraries;
if a shared dependency lives outside a board/scene folder, publish its owning
folder too and preserve the relative references.

Assembly filenames use `<name>_assembly.<extension>` for top-level assemblies and
subassemblies. Keep `_assembly` immediately before the extension in both native
files and matching exports: `wheel_assembly.FCStd`, `wheel_assembly.step` and
`wheel_assembly.blend` for a Blender assembly. Put other qualifiers before the
suffix. This convention applies in PLM and local-only mode. Individual parts and
presentation-only scenes use descriptive names for their own roles. Update
references, export paths and mappings together when renaming existing files;
preserve repository revision history through supported operations.

## Required completeness

- Before product/module development, complete and approve the project and affected
  module `SPECIFICATION.md` files for the agreed scope using the
  [specification gates](../../engineering-workflow/references/module-specification.md).
  Include both baselines in the saved handoff and identify their revisions in the design,
  reports and checks. Draft specifications may be saved while requirements are
  being established; saving them does not authorize implementation.
- Follow the [lifecycle sign-off contract](../../../../user/docs/plm-lifecycle.md).
  Save readable stage evidence and actual decisions for the named revisions and
  scope. Retain discipline folders within `<module>/`; lifecycle progression does
  not require duplicating deliverable trees in separate stage directories.
- Include every non-embedded component import or linked component file under the
  appropriate `components/` folder, including transitive external dependencies.
  Apply the same assembly suffix, native/STEP companion and revision rules as for
  other components. An imported STEP needs no duplicate native wrapper. Vendor
  geometry actively referenced by the model is a component dependency; keep
  reference-only copies under `reference/`.
- Fully embedded components need no separate files, uploads or per-component STEP
  exports. Verify the saved parent contains the component without relying on an
  external source file; merely displaying imported geometry is not proof of
  embedding. Retain the parent's required exports and remaining dependencies.
  Do not extract embedded components merely to create separate component assets.
- Every saved `.FCStd` needs a corresponding STEP file. Mirror the native path
  below `cad/` in `cad/exports/`, changing the extension to `.step`, so equal part
  basenames remain distinct. Recompute the source, export and check units,
  orientation and geometry. Record both saved revisions together. A stale STEP
  is not a companion for a changed native file. If export is impossible, report
  the missing companion and an incomplete package; do not claim completion.
- Include the editable `.blend` used for delivered scenes/renders and the assets
  required to reopen it. A final image alone does not replace the Blender source.
- Group each KiCad project with its PCB, schematics and required custom symbols,
  footprints, library tables and 3D models. Check that the saved layout resolves
  without machine-specific absolute library paths. Bundle project-specific
  third-party libraries needed to reopen the design. Standard KiCad libraries
  can be a documented installed dependency with the required version identified.
- Include firmware and product software source, build dependencies and build/use
  instructions. Source required to build or operate the product belongs under
  `user/`, even if an agent wrote it. Native project/build files and lockfiles
  are deliverables; downloaded toolchains, dependency trees and build caches are
  local. Release binaries supplement source and are included when requested.
- Include final renders and readable simulation reports for work performed in
  scope. Reports state inputs, source revisions, assumptions, method, criteria,
  results, warnings, failures and limits; add selected plots/data needed to judge
  the result. A raw solver log or serialized run record is not a report.

## Keep local

Never include `agent/` records in a PLM package: logs, transcripts, prompts,
internal plans, temporary or evidence JSON, gate-checker output, upload receipts,
hash/dependency bookkeeping, caches, tool installations, scratch geometry, solver
work directories, test-run output, autosaves, backups, locks, secrets or temporary
previews. This applies to individual uploads and archive contents as well as
whole-directory uploads. Renaming or moving a raw agent record into `user/` does
not make it a deliverable.

Summarize engineering evidence in a readable report for the builder/reviewer.
Keep raw records in local `agent/evidence/`. Product firmware/software and
reproducible simulation source are different from agent generation scripts and
post-processing automation; publish the former in their owning deliverable
folders and retain the latter under `agent/`.

## Before any upload

In local-only mode, check the local package against the same rules and report its
location and version-control limitation; skip remote folder/write operations.

Prepare an explicit local inventory of the scoped deliverables and destination
folders, with companions and dependencies. Check it against the rules above;
directory location by itself does not make every file eligible. Keep this
machine-readable inventory in `agent/`, not in PLM.

Resolve/create the native MiniPLM folder chain using parent IDs in the selected
iteration, then pass the leaf `folder_id` for each upload. A local path does not
automatically create its directory hierarchy remotely. Inspect collisions within
the intended folder/container. Existing-file revision writes retain the asset's
current folder: verify it matches the mapping before revising. Do not use child
asset metadata or filename prefixes as a substitute for folders.

For a completed save, verify every required member, companion and dependency at
its mapped destination, check assembly suffixes and matching export stems, and
record exact revisions locally. Missing dependencies,
STEP files, Blender sources or reports must appear as incomplete items in the
handoff. Publish a readable package index when useful; raw machine manifests and
receipts remain local.
