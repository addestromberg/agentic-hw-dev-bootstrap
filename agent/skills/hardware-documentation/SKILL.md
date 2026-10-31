---
name: hardware-documentation
description: Write and maintain RSIM hardware module reports, requirements, build instructions, operating guides and reference indexes. Use for documentation delivered with CAD, electronics or simulations; keep agent logs, scripts and machine-readable evidence outside user deliverables.
---

# Hardware documentation

Read the workspace `AGENTS.md`, `user/docs/project-rules.md`, and the owning
module's documents and native design baseline before writing. Preserve established
terminology, units, revision identifiers and working user links.

## Destination and scope

- Put module reports, requirements, decisions, assembly/build instructions and
  operating guidance in `user/modules/<module>/docs/`. Keep its `README.md` as a
  short entry point. Put cockpit-wide guidance in `user/docs/`.
- Place external datasheets, drawings and source documents in the module's
  `reference/`, with source URL and revision when known. Link to final images in
  `renders/` and authoritative designs in `cad/` or `electronics/`.
- Keep scripts, macros, evidence JSON, transcripts and intermediates under
  `agent/`. Link to evidence without copying raw logs into reports. Native CAD,
  KiCad and solver inputs are user deliverables.

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
