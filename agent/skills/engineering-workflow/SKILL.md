---
name: engineering-workflow
description: Coordinate requirements, architecture, multidisciplinary design, evidence, review gates, prototype handoff and validation for physical engineering work. Use when a task crosses disciplines, changes a hardware baseline, starts a new design, or claims readiness for manufacture, bench testing or release. Delegate detailed checks to applicable domain and review skills.
---

# Engineering workflow

Use this skill as the **process owner**, not as a replacement for electrical, mechanical, RF, optical, simulation or test expertise. Follow project instructions and [the shared gate contract](references/gates-and-contract.md). A project-specific, validated gate (for example the electronics-development checker) takes precedence for that domain and must not be silently weakened.

## Plan and identify the engineering baseline

1. Read the owning project's README, decisions, requirements, applicable agent rules, native design sources, and existing evidence. Locate the actual project/subsystem before creating files.
2. Identify the physical goal, operating envelope, interfaces, regulatory/safety constraints, budget, acceptance criteria, and design revision. Mark unknowns as open; do not invent accepted requirements.
3. Choose a proportionate rigor level: exploratory, prototype or qualification. Record the choice and risks. Exploration is allowed with open blockers; claims of readiness are not.
4. Build a requirements-to-evidence matrix: requirement ID and units, acceptance, verification method, responsible discipline, evidence and current status.
5. Identify coupled risks (electrical load vs mechanism mass, RF/grounding vs mechanical enclosure, optical alignment vs vibration, thermal expansion vs calibration) and request a multidisciplinary integration review for affected interfaces.

## Execute the loop

- **Design:** invoke the relevant discipline skill; keep editable/native files authoritative. Capture alternatives and trade-offs, explicit assumptions and tolerance/uncertainty budgets.
- **Analyze:** use $simulation-engineering where applicable; establish analytical sanity checks, input provenance and model limits before interpreting plots.
- **Review:** use $design-review, ideally in a separate agent/session with fresh context and no author ownership. Close blocking findings with revised evidence, not prose assurances.
- **Prototype release:** assemble fabrication source, BOM/materials, drawings/exports, checks and a bring-up/test plan. Run any domain-specific release checker. A reviewer can recommend readiness, but only the user authorizes purchases or fabrication.
- **Physical verification:** distinguish inspection, unpowered checks, controlled bring-up, measured performance and final validation. Compare against requirements; if the as-built design differs, revise the baseline and affected analyses.
- **Iteration:** on a failed gate, return to the affected stage, preserve prior failures, and recheck dependent evidence.

Use [gates and handoff contract](references/gates-and-contract.md) for required traceability and records.

### Executable stage gates

For any claim of design/prototype/bench/qualified readiness in a configured
mechanical, simulation or integrated project, run the
[shared checker](scripts/check_gates.py) against a project-local configuration:

```sh
python SKILLS/engineering-workflow/scripts/check_gates.py <project-gate-config.json> --stage prototype
```

Read [configuration/evidence contract](references/gate-engine.md) first. A
missing config or evidence is a blocker, not permission to skip the gate.
If the project has not adopted this schema yet, report readiness as
**not evaluated**, even when design work continues. The electrical adapter
calls the original electronics release checker unchanged; never substitute
a generic `READY` for its own release result. The shared checker validates
recorded evidence and numeric criteria, not actual material physics.

Never use a green tool exit status alone as acceptance of a physical design. Never use a green tool exit status alone as acceptance of a physical design.

## Done condition

Report design revision, changed artifacts, known assumptions, checks **actually run**, evidence locations, unresolved findings, requested gate status and next action. A skill instruction alone does not enforce a gate; CI, a project-specific checker, or an orchestrator must enforce it operationally. Do not authorize manufacture, RF transmission, powered equipment, or system changes on behalf of the user.
