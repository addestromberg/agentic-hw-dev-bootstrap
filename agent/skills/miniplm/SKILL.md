---
name: miniplm
description: Organize hardware, firmware/software and human-facing deliverables in MiniPLM with traceable native revisions, or matching local directories when PLM is unavailable. Apply to product file handoffs; keep agent records local. Bootstrap maintenance does not create projects or upload files.
---

# MiniPLM repository workflow

MiniPLM stores the project's saved hardware deliverables and revision history.
Native editable files remain the design authority; local `user/` files are working
copies and upload sources. Git maintains this bootstrap's skills, automation and
rules; a Git commit does not identify a MiniPLM design revision.

Follow the workspace's project rules for local paths. Use the discipline skills
for engineering checks and readiness decisions. Read
[tool semantics and handoff records](references/repository-contract.md) when
resolving targets, saving files or preparing a package. Before any save, read
[deliverables and directory discipline](references/publish-policy.md) for the
publishable file set, required companions and destination structure.

## Bootstrap versus an active hardware project

This repository is a reusable starting point. Updating its skills, scripts or
templates must not create a MiniPLM product, iteration, folder or file. Do not
embed account details, credentials, project IDs, module names or accepted design
requirements in reusable instructions.

In a downstream project, resolve the intended MiniPLM project and iteration from
the task and existing mapping before writing remotely. Projects are products in
the upstream API. Keep `user/modules/<module>/` locally. Within the explicitly
selected product's iteration, map that local module root to `<module>/`, with
`SPECIFICATION.md` at that folder's root and `cad/`, `electronics/`, `firmware/`,
`software/`, `sim/`, `docs/`, `reference/` and `renders/` below it as needed.
The project is the product, not a `product/` directory. Omit only the local
`user/modules/` wrapper in PLM; retain the module name, such as `wheel/cad/`.
Publish repository-root project `SPECIFICATION.md` at the iteration root, alongside
module folders. It defines the product goal; each module spec refines its allocation.
Follow the [PLM lifecycle](../../../user/docs/plm-lifecycle.md) and save readable
stage reviews/actual sign-offs with the specifications. Keep lifecycle stages
distinct from MiniPLM iterations, folders and file revisions. Discover existing
server stages if relevant; the exposed tools do not provide a general stage
transition/approval operation. Do not create twelve iterations or stage folders,
or claim a server transition, simply to represent the lifecycle.
Use native MiniPLM folders for discipline,
board, study and other deliverable grouping. Record explicit destinations for
multi-module work and resolve collisions before writing.
Folders are organization, not pinned assembly configurations or release states.
Store downstream mappings under `agent/config/`, with module-specific mappings
under `agent/config/modules/<module>/`. Create mappings only for actual work.

## Establish the working baseline

1. Discover the available MiniPLM tools and their current schemas. Check session
   status when needed, then inspect the selected project, iterations, folders and
   files. Do not choose the first visible project or assume “latest” means the
   intended baseline. If MiniPLM or a usable target is unavailable, use the local
   fallback below. Clarify an ambiguous target before dependent remote writes;
   local work can continue without guessing a destination.
2. Resolve each input to a file ID and exact revision, including referenced CAD
   parts, KiCad libraries, simulation inputs and relevant documents. Record the
   remote identity and local SHA-256 before editing. Preserve local changes;
   reconcile divergent local/remote work rather than overwriting either copy.
3. Materialize the chosen revision in the owning local folder using an available,
   verified retrieval route. `plm_get_file` returns metadata, not binary contents;
   `plm_get_documentation` reads supported text. If no binary retrieval route is
   available, report the missing source and continue only independent work.
   Do not substitute a preview or mesh for native CAD.

## Local-only fallback

If no MiniPLM integration, reachable session or usable repository target is found,
continue in local-only mode using `user/modules/<module>/` and the same discipline,
board, scene, study and source subfolders defined in the publish policy. Keep
agent files separately under local `agent/`. Do not make PLM setup a prerequisite
for useful local design work, invent remote IDs, or create a guessed product.

Report that the deliverables are saved locally and have no PLM version control
or revision history. These directories alone do not provide file version control;
bootstrap Git commits and local hash records do not substitute for it. Use a
separate version-control system only when explicitly established by the project.
Native/STEP companions, dependencies and readable reports are still required.

If unavailable remote source files are needed, report those inputs as missing;
local-only mode cannot recover them. When PLM becomes available, inspect its
current state and reconcile the local files before saving. Do not treat local
work as already synchronized or retry an uncertain write blindly.

## Edit, check and save

Before module implementation, follow the
[specification gate](../engineering-workflow/references/module-specification.md).
Read the approved project and module-root `SPECIFICATION.md` at their intended revisions. Draft
specification work and its save are allowed before approval; module CAD, circuit,
firmware/software and design-validation work wait for the approved baseline.

Work locally with the native applications. Keep exports tied to the exact native
inputs, run the checks warranted by the change, and retain provenance in
`agent/evidence/<module>/<run>/`. Existing engineering gates still consume local
paths and byte hashes; a remote revision ID cannot replace these inputs.

When the requested hardware work includes saving deliverables to MiniPLM and the
target is resolved, carry out that save within the authorized scope. Do not add a
confirmation step for every file. Respect local-only draft requests and do not
expand a scoped save into a workspace-wide migration.

- Before a write, inspect the destination and compare the remote baseline with
  the revision used for the edit. Reconcile changes if it has advanced.
- Upload new assets with an explicit container and folder. For an existing
  standalone asset, prefer `plm_create_revision` with its file ID and a meaningful
  change description. Same-name uploads can create revisions; inspect collisions
  before uploading. Do not infer global uniqueness from a filename.
- Select an explicit set of human-facing deliverables and required native/build
  dependencies using the publish policy. Each `.FCStd` needs a matching STEP;
  include `.blend` sources/assets, final renders, readable simulation reports,
  complete KiCad projects/libraries and product firmware/software when in scope.
  Preserve relative references and resolve each destination folder before upload.
  Assembly and subassembly filenames use `<name>_assembly.<extension>`; matching
  exports retain the same stem, including the suffix immediately before the extension.
  Put non-embedded imports and externally linked component files in the owning
  `components/` folder and include their dependencies under the same file rules.
  Fully embedded components need no separate assets; verify they are self-contained.
  Keep all agent records local, including logs, evidence/temporary JSON, upload
  receipts, internal Markdown and machine manifests. Do not upload them singly
  or inside an archive. Required native/build JSON files are a different category.
- Record each successful write's returned identity, then inspect metadata/history
  to confirm the intended revision and destination. Record whether verification
  checked metadata or actual remote bytes; do not claim an unperformed round trip.
- After a timeout or uncertain response, inspect state before retrying. If the
  outcome remains unknown, record it as unresolved and stop dependent writes.
  Do not create duplicate revisions or products to make the task appear complete.

## Handoff

State lifecycle stage, actual sign-off status and repository mode: MiniPLM or local-only. Provide saved file/revision
identities when available, local source paths, checks performed,
unsaved or uncertain items and the location of the revision/dependency record.
Distinguish repository save status from engineering gate status. Multi-file saves
may be partial; no complete package claim until its required members and pinned
dependencies and companion files have been verified at their mapped destinations.
A MiniPLM iteration, revision, conversion or
preview does not establish engineering approval or manufacturing readiness.
