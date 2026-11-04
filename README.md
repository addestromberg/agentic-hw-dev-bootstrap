# Agentic hardware development bootstrap

A reusable starting point for hardware projects, with engineering skills, native
design tools, project/module specifications and a stage-gate PLM lifecycle.
The template has no accepted product goal, approved requirements, hardware modules
or assigned MiniPLM project. Copying or maintaining it does not create remote
projects or upload files.

## Start a project

1. Read the [project rules](user/docs/project-rules.md) and
   [toolchain setup](agent/docs/toolchain.md). FreeCAD, KiCad and Blender use
   pacman. Adapt local MCP paths/connections for the downstream workspace; the
   existing setup records describe this workspace, not a portable installation.
2. Define the product goal, scope, measurable requirements, module responsibilities
   and system acceptance in root [SPECIFICATION.md](SPECIFICATION.md). Follow the
   [PLM lifecycle](user/docs/plm-lifecycle.md) for Conceive and Specification
   reviews and actual owner decisions.
3. Create only the modules needed by the project. For example:

   ```sh
   python3 agent/scripts/new_module.py wheel --components --firmware --software
   ```

   `wheel` is illustrative. Omit optional flags when those folders are unnecessary.
   The command creates local folders, a readable index and a draft module-root
   `SPECIFICATION.md`; existing specifications and files are preserved.
4. Complete the affected module specification, tracing its requirements and
   interfaces to the project baseline. Approve both specifications for the agreed
   scope before Concept design or implementation. A scaffold is not approval.
5. Develop, check, review and sign off the applicable lifecycle stages. Produce
   native sources, required companions and readable reports. Select repository
   operation below and save the scoped handoff with its actual status.

Project/module specs retain lifecycle progress and sign-offs through Conceive,
Specification, Concept design, Design, Detailed design, Validation and analysis
(simulation), Tool design, Realise, Plan manufacturing, Manufacture,
Build/assemble and Test (quality control). Record actual decisions and revisions;
earlier approval does not silently authorize later physical actions.

## With MiniPLM or local-only

| Situation | Operation |
| --- | --- |
| MiniPLM is connected and the intended target is resolved | Select the project/iteration explicitly, retrieve exact native revisions/dependencies, edit and check locally, then save deliverables to their mapped folders and verify the resulting revisions. |
| No MiniPLM tools, unavailable service/session, no usable target, or a local-only task | Continue in the same local file structure with the same specification, companion-file, review and sign-off rules. Report local-only storage without PLM revision history. Plain directories do not provide version control. |
| Connection is lost during a save | Preserve local work and record the uncertain/partial save locally. Inspect server state before retrying; do not report missing or uncertain revisions as saved. |
| MiniPLM becomes available later | Inspect current remote revisions and reconcile them with the local work before uploading. Preserve local changes and existing remote history. |

Unavailable remote native inputs remain missing. Continue work that has the
necessary inputs; metadata or previews cannot replace native sources. A separate
design-file version-control workflow must be explicitly established if needed in
local-only mode. Git on this bootstrap maintains its skills, tooling and documents;
it does not supply MiniPLM history or automatic file synchronization.

The MiniPLM **project is the product**. Within its selected iteration:

| Local path | MiniPLM path within that project/iteration |
| --- | --- |
| Root `SPECIFICATION.md` | `SPECIFICATION.md` |
| `user/docs/` | `docs/` for product-wide human documents |
| `user/modules/wheel/SPECIFICATION.md` | `wheel/SPECIFICATION.md` |
| `user/modules/wheel/cad/` | `wheel/cad/` |
| `user/modules/wheel/electronics/` | `wheel/electronics/` |

Keep the local `user/modules/` wrapper on disk; retain the module name in PLM.
The product is not a directory. Record downstream target mappings under
`agent/config/`; keep credentials outside the repository. MiniPLM saves and
sign-off are separate: the current connector does not automate lifecycle approval
transitions. See the [MiniPLM skill](agent/skills/miniplm/SKILL.md) for recovery,
revision handling and transfer limitations.

## Deliverables and local working records

User deliverables live under `user/`, except the root project specification.
Agent scripts, configuration, evidence, logs and scratch stay under `agent/`.
MiniPLM packages include only the scoped human documents and product files:

- Native FreeCAD files with matching STEP companions. Assemblies/subassemblies
  use `<name>_assembly.<extension>` with matching export stems.
- Non-embedded imported/linked components under the owning `components/` folder,
  with dependencies. Fully embedded components need no separate component files.
- Editable Blender scenes/assets and final renders.
- Complete KiCad projects, PCB/schematic sheets and required custom libraries,
  grouped by board; requested BOM/fabrication outputs in their owning folders.
- Firmware/software source, build inputs and instructions, grouped by target/app.
- Reproducible simulation inputs, readable reports, figures and useful result data,
  grouped by study; readable manufacturing, assembly and quality records as needed.

Agent notes (including internal Markdown), logs, temporary/evidence JSON, machine
manifests, upload receipts, caches, backups and scratch never go into PLM. Required
native/build files can contain JSON; purpose determines ownership. Apply the
[publish policy](agent/skills/miniplm/references/publish-policy.md) before every
save, including archive contents and document links.

## Reference

- [Project rules and complete directory structure](user/docs/project-rules.md)
- [Project specification](SPECIFICATION.md)
- [PLM lifecycle and stage sign-off](user/docs/plm-lifecycle.md)
- [Module setup](user/modules/README.md)
- [Agent instructions and skill index](AGENTS.md)
- [Toolchain setup, connection limits and verification](agent/docs/toolchain.md)
