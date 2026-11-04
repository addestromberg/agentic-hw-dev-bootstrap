---
name: electronics-development
description: Develop or review electronic circuits, PCB layouts, component choices, hardware-facing firmware, electrical simulations and board releases using change-specific checks and evidence-based release gates. Use for electronics development and bring-up; exclude unrelated software, presentation-only edits and mechanical CAD work.
---

# Electronics development

Use this workflow throughout electronics work, across projects. For module work
in this bootstrap, the [specification gate](../engineering-workflow/references/module-specification.md)
requires complete, approved project and module-root `SPECIFICATION.md` baselines before circuit/PCB or
firmware/software implementation. Requirements discovery and explicitly scoped
feasibility work can prepare that baseline. Qualification and release checks
remain later gates; they do not replace specification approval.
Align work with the [PLM lifecycle](../../../user/docs/plm-lifecycle.md), keeping
concept/design/detail reviews and actual owner sign-off separate from checker
results. Use the existing `prototype` gate for fabrication release planning,
`bench` for the applicable assembled-board test entry, and `qualified` for claims
requiring completed physical evidence. Lifecycle names do not change those enums
or waive their mandatory checks.

This skill is the electrical domain authority for the owning project's boards. For tasks
spanning disciplines, use [engineering-workflow](../engineering-workflow/SKILL.md)
to coordinate requirements and handoffs; use [simulation-engineering](../simulation-engineering/SKILL.md)
for reproducible simulation and [design-review](../design-review/SKILL.md)
for an independent review. **Do not replace** this skill's existing
`prototype`, `bench` or `qualified` checker with the generic workflow gate.

## Before a change

For MiniPLM-backed work, follow [the repository workflow](../miniplm/SKILL.md).
Resolve the native KiCad project, schematic sheets, PCB and required local library
revisions as one baseline. Keep relative library references intact locally and
pin saved source revisions for BOM/fabrication exports. Remote IDs supplement
local input hashes; they do not replace the release checker's file evidence.
Group each board under `electronics/kicad/<board>/`, with the PCB, all schematic
sheets, project files and portable library tables. Put required custom symbols,
footprints and 3D models under its `libraries/`; preserve necessary shared-library
references. Keep BOM/fabrication outputs grouped by board in their owning folders.
Product firmware belongs in `firmware/<target>/` and software in `software/<app>/`,
including source, build configuration, dependency manifests/locks and readable
build/use instructions. Agent scripts, raw check logs, temporary JSON and local
KiCad state stay local and are excluded from PLM.

Read project instructions and existing evidence. Identify the board/revision, operating envelope, affected circuitry and failure modes. Distinguish requirements, proposals and measurements. If no release configuration exists, establish one in the owning project's config directory when relevant to the requested work; do not initialize unrelated projects.

For circuit, component, layout or hardware-facing firmware changes, read [engineering checks](references/engineering-checks.md). Choose checks from the actual change and its electrical consequences. Obtain current primary datasheets for affected parts; verify package and variant. Preserve manual native-design edits and unrelated work.

## During development

Run applicable ERC/DRC, connectivity, calculations, simulations or firmware checks after relevant edits. Record exact inputs, tool versions, criteria and outcomes under the owning project. Documentation/presentation-only edits need link/content checks, not a full electrical simulation rerun, unless they change requirements or invalidate evidence.

Use conservative, justified component tolerances and operating conditions. Do not treat typical values, ideal SPICE sources, IC protection features, or a clean DRC as proof of safe operation. Keep calculated, simulated, reviewed and physically measured results distinct. Missing equipment, models or measurements remain outstanding; never invent results.

Before a fabrication or readiness claim, read [release gates](references/release-gates.md) and run `python <this-skill>/scripts/check_release.py <board-config> --stage prototype|bench|qualified`. This checker reads records only; execute engineering checks separately. Never change requirements or mark unperformed checks passed merely to obtain a green result. Refresh evidence only after the affected checks actually run or the documented review is performed.

## Release and task completion

The prototype gate precedes ordering; the bench gate precedes powered functional/load testing after low-energy logic bring-up; qualification follows physical testing. Use [bring-up guidance](references/bring-up.md) when preparing or performing bench work. A passing gate verifies record completeness/freshness, not engineering truth or formal certification. It does not authorize purchases, fabrication submission, physical test actions or equipment access.

For every electronics task, report what changed, checks actually performed, unresolved findings and readiness for the requested stage. Run the gate for the stage being claimed; otherwise report draft status unless a current gate result establishes more. Stale/missing/failed/skipped required evidence blocks readiness, not unrelated draft progress. Keep evidence with the project; retain raw results and source identities. No commit hooks or CI changes are implied.
