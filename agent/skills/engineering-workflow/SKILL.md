---
name: engineering-workflow
description: Coordinate the stage-gate PLM lifecycle, top-down project/module specifications, multidisciplinary design, sign-off and physical verification. Use when starting hardware work, changing a baseline, advancing lifecycle stages or assessing manufacture/test readiness. Use domain skills for detailed checks.
---

# Engineering workflow

Use this skill as the **process owner**, not as a replacement for electrical, mechanical, RF, optical, simulation or test expertise. Follow project instructions and [the shared gate contract](references/gates-and-contract.md). A project-specific, validated gate (for example the electronics-development checker) takes precedence for that domain and must not be silently weakened.

## Lifecycle and sign-off

Follow the [PLM lifecycle](../../../user/docs/plm-lifecycle.md) as the ordered
stage model: Conceive → Specification → Concept design → Design → Detailed design
→ Validation and analysis (simulation) → Tool design → Realise → Plan manufacturing
→ Manufacture → Build/assemble → Test (quality control).

Prepare each applicable stage's evidence and obtain actual owner sign-off for
the next scope before advancing. Project requirements and approvals flow down
into modules; module evidence and integration results support product decisions.
Keep stage progress and sign-off in the project/module specifications, with
readable supporting reports. Reuse existing approval for unchanged scope;
do not infer fabrication or physical-test permission from design approval.
Record justified, owner-approved stage exclusions without weakening domain gates.
The execution loop below operates within this lifecycle, including rework loops.

## Plan and identify the engineering baseline

Start with repository-root `SPECIFICATION.md` as the product goal and system
acceptance baseline, then the affected module's root `SPECIFICATION.md` and the
[specification entry gates](references/module-specification.md). Trace module
requirements to the approved project revision. Complete and
approve the requirements, interfaces, acceptance plan and scope at both levels before module
implementation. While incomplete, work on requirements and explicitly scoped
feasibility questions. Do not treat an empty template or assumed approval as an
accepted baseline. Reuse existing approval for the same revision/scope.

For MiniPLM-backed hardware work, use [the repository workflow](../miniplm/SKILL.md)
to resolve the project/iteration and exact native file revisions before editing.
Keep local working copies in `user/`, mappings under `agent/config/`, and revision
receipts/evidence under `agent/evidence/`. Bootstrap maintenance does not create
remote projects or hardware baselines.
Plan the deliverable folder structure and file set with the
[publish policy](../miniplm/references/publish-policy.md): native/STEP pairs,
Blender sources, complete board projects, firmware/software, renders and readable
reports as applicable. Keep machine evidence and agent records local; check
package completeness and correct folder placement before claiming a saved handoff.

1. Read the owning project's README, decisions, requirements, applicable agent rules, native design sources, and existing evidence. Locate the actual project/subsystem before creating files.
2. Identify the physical goal, operating envelope, interfaces, regulatory/safety constraints, budget, acceptance criteria, and design revision. Mark unknowns as open; do not invent accepted requirements.
3. Choose a proportionate rigor level: exploratory, prototype or qualification. Record the choice and risks in the specification. Development stays within its approved scope; pre-approval exploration is limited to requirements discovery and explicitly scoped feasibility questions. Readiness needs its own evidence and gates.
4. Build a requirements-to-evidence matrix: requirement ID and units, acceptance, verification method, responsible discipline, evidence and current status.
5. Identify coupled risks (electrical load vs mechanism mass, RF/grounding vs mechanical enclosure, optical alignment vs vibration, thermal expansion vs calibration) and request a multidisciplinary integration review for affected interfaces.

## Execute the loop

- **Design:** invoke the relevant discipline skill; keep editable/native files authoritative. Capture alternatives and trade-offs, explicit assumptions and tolerance/uncertainty budgets.
- **Analyze:** use $simulation-engineering where applicable; establish analytical sanity checks, input provenance and model limits before interpreting plots.
- **Review:** use $design-review, ideally in a separate agent/session with fresh context and no author ownership. Close blocking findings with revised evidence, not prose assurances.
- **Prototype release:** assemble fabrication source, BOM/materials, drawings/exports, checks and a bring-up/test plan. Pin the MiniPLM file revisions and dependencies for the handoff; an iteration or folder alone is not a baseline. Run any domain-specific release checker. A reviewer can recommend readiness, but only the user authorizes purchases or fabrication.
- **Physical verification:** distinguish inspection, unpowered checks, controlled bring-up, measured performance and final validation. Compare against requirements; if the as-built design differs, revise the baseline and affected analyses.
- **Iteration:** on a failed gate, return to the affected stage, preserve prior failures, and recheck dependent evidence.

Revise and reapprove affected project/module specifications before implementing a requirements,
interface or scope change. Carry its revision through design decisions, reports
and applicable gate inputs; preserve previous approvals and failed evidence.

Use [gates and handoff contract](references/gates-and-contract.md) for required traceability and records.

### Executable stage gates

Lifecycle stage names and human sign-offs do not change executable checker enums.
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

Never use a green tool exit status alone as acceptance of a physical design.

## Done condition

Report lifecycle stage and sign-off status, specification/design revisions, changed artifacts, MiniPLM save status and exact saved revisions when applicable, known assumptions, checks **actually run**, evidence locations, unresolved findings, requested gate status and next action. A skill instruction alone does not enforce a gate; CI, a project-specific checker, or an orchestrator must enforce it operationally. Do not authorize manufacture, RF transmission, powered equipment, or system changes on behalf of the user.
