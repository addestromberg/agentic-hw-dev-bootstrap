---
name: hardware-documentation
description: Write and maintain hardware module reports, requirements, build instructions, operating guides and reference indexes. Use for documentation delivered with CAD, electronics or simulations; keep agent logs, scripts and machine-readable evidence outside user deliverables.
---

# Hardware documentation

Read the workspace `AGENTS.md`, `user/docs/project-rules.md`, and the owning
module's documents and native design baseline before writing. Preserve established
terminology, units, revision identifiers and working user links.

For MiniPLM-backed work, follow [the repository workflow](../miniplm/SKILL.md).
Read documents at the intended revision and identify the exact native sources
assessed by each report or build guide. Save requested documentation and referenced
deliverables with a readable revision index when needed. Keep local relative links
usable and include returned MiniPLM links/IDs for repository navigation; metadata
alone does not establish that a referenced native file was inspected.

## Destination and scope

- Maintain repository-root `SPECIFICATION.md` as the overall product goal,
  project requirements, module allocation and system completion criteria. This
  human-facing file is a root-placement exception; keep the bootstrap draft until
  actual requirements and owner approval exist.
- Maintain the module's root `SPECIFICATION.md` as the requirements and approved
  scope entry point, using the [specification template](../../templates/module-specification.md)
  and [entry gate](../engineering-workflow/references/module-specification.md).
  Draft it before module implementation; record actual approval rather than
  inventing accepted values or copying a status label. Put supporting analyses
  and detailed requirement documents under `docs/` and link them from the spec.
  Identify the approved parent-project revision and map module requirement IDs
  to project requirement IDs. Propagate approved changes without silently
  redefining the overall goal.
- Maintain the specification's [lifecycle/sign-off record](../../../user/docs/plm-lifecycle.md):
  stage, exact revisions/scope, readable evidence references, review findings and
  actual owner decision/date/source. Keep prior/superseded decisions. Separate
  planned manufacture/assembly/test instructions from records of actual work;
  only recorded physical work can support completed physical-stage claims.
- Put module reports, decisions, assembly/build instructions and
  operating guidance in `user/modules/<module>/docs/`. Keep its `README.md` as a
  short entry point. Simulation reports and figures stay with their study under
  `sim/<discipline>/<study>/reports/`. Put project-wide guidance in `user/docs/`.
- Place external datasheets, drawings and source documents in the module's
  `reference/`, with source URL and revision when known. Link to final images in
  `renders/` and authoritative designs in `cad/` or `electronics/`.
- Publish human-facing `.md`, PDF and other useful documents, not agent notes,
  transcripts, raw logs or JSON records. Keep agent generation scripts, macros,
  evidence and intermediates under local `agent/`. Product firmware/software and
  reproducible simulation source belong in their deliverable folders and are
  included in PLM with required build/native files, even if those contain JSON.
- Summarize methods, results, failures and limits in readable reports. For PLM
  readers, link to saved deliverables and include the facts needed to assess the
  report; a local `agent/` path is not remotely accessible supporting evidence.
  Keep detailed raw-evidence links for local use without uploading those records.

## Write for the builder or reviewer

Use the structure warranted by the document; omit empty template sections.

For build instructions, identify revision, parts/materials, tools, orientation,
datums and units, ordered assembly steps, interface dimensions and checks that
show important steps are complete. State torque, fit, wiring and polarity values
only when supported by the design or a cited source. Label unperformed assembly
steps as proposed instructions; writing a guide does not establish a tested build.

For reports, connect the question and requirements to the source revision,
assumptions, method, criteria, results and limits. Distinguish calculated,
simulated, reviewed and measured results. Label plot axes, units, conditions and
captions. Cite primary datasheets/reference documents for component and material
properties. Missing results stay missing; do not infer a pass from missing evidence.

Explain unresolved decisions and the next check when they affect the user. For
prototype, bench or qualified readiness claims, use the relevant engineering skill
and actual gate checker. Documentation edits do not require rerunning unrelated
simulations.

## Finish

Check relative links, filenames, units, part/revision consistency, captions and
agreement between summaries and evidence. For a PDF export, retain the editable
source and inspect layout, diagrams and tables. Report checks actually performed
and remaining uncertainty.
