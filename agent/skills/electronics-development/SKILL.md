---
name: electronics-development
description: Develop or review electronic circuits, PCB layouts, component choices, hardware-facing firmware, electrical simulations and board releases using change-specific checks and evidence-based release gates. Use for electronics development and bring-up; exclude unrelated software, presentation-only edits and mechanical CAD work.
---

# Electronics development

Use this workflow throughout electronics work, across projects. Continue useful draft work while recording unresolved requirements; do not make every edit wait for complete qualification.

This skill is the electrical domain authority for Skywatch boards. For tasks
spanning disciplines, use [engineering-workflow](../engineering-workflow/SKILL.md)
to coordinate requirements and handoffs; use [simulation-engineering](../simulation-engineering/SKILL.md)
for reproducible simulation and [design-review](../design-review/SKILL.md)
for an independent review. **Do not replace** this skill's existing
`prototype`, `bench` or `qualified` checker with the generic workflow gate.

## Before a change

Read project instructions and existing evidence. Identify the board/revision, operating envelope, affected circuitry and failure modes. Distinguish requirements, proposals and measurements. If no release configuration exists, establish one in the owning project's config directory when relevant to the requested work; do not initialize unrelated projects.

For circuit, component, layout or hardware-facing firmware changes, read [engineering checks](references/engineering-checks.md). Choose checks from the actual change and its electrical consequences. Obtain current primary datasheets for affected parts; verify package and variant. Preserve manual native-design edits and unrelated work.

## During development

Run applicable ERC/DRC, connectivity, calculations, simulations or firmware checks after relevant edits. Record exact inputs, tool versions, criteria and outcomes under the owning project. Documentation/presentation-only edits need link/content checks, not a full electrical simulation rerun, unless they change requirements or invalidate evidence.

Use conservative, justified component tolerances and operating conditions. Do not treat typical values, ideal SPICE sources, IC protection features, or a clean DRC as proof of safe operation. Keep calculated, simulated, reviewed and physically measured results distinct. Missing equipment, models or measurements remain outstanding; never invent results.

Before a fabrication or readiness claim, read [release gates](references/release-gates.md) and run `python <this-skill>/scripts/check_release.py <board-config> --stage prototype|bench|qualified`. This checker reads records only; execute engineering checks separately. Never change requirements or mark unperformed checks passed merely to obtain a green result. Refresh evidence only after the affected checks actually run or the documented review is performed.

## Release and task completion

The prototype gate precedes ordering; the bench gate precedes powered functional/load testing after low-energy logic bring-up; qualification follows physical testing. Use [bring-up guidance](references/bring-up.md) when preparing or performing bench work. A passing gate verifies record completeness/freshness, not engineering truth or formal certification. It does not authorize purchases, fabrication submission, physical test actions or equipment access.

For every electronics task, report what changed, checks actually performed, unresolved findings and readiness for the requested stage. Run the gate for the stage being claimed; otherwise report draft status unless a current gate result establishes more. Stale/missing/failed/skipped required evidence blocks readiness, not unrelated draft progress. Keep evidence with the project; retain raw results and source identities. No commit hooks or CI changes are implied.
