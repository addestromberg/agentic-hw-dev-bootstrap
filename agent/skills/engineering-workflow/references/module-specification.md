# Project and module specifications: development entry gates

Root `SPECIFICATION.md` defines the overall product goal, scope, requirements and
objective completion criteria for the engineering agent. It is a user deliverable
at repository root by project convention. Publish it as `SPECIFICATION.md` at the
selected MiniPLM project iteration's root. The project is the product, not a folder.

Complete and approve the project specification for the agreed stage before
product implementation. Cover intended use and boundaries, measurable project
requirements, shared constraints, module responsibilities and interfaces,
requirement allocation, integration verification and actual owner approval.
An unset product goal or unresolved critical system interface blocks development.
Requirements discovery and explicitly scoped feasibility work can prepare this
baseline; maintaining the bootstrap does not require an invented approved goal.

Specification is the entry gate to Concept design in the
[PLM lifecycle](../../../../user/docs/plm-lifecycle.md). The approved specification
defines requirements and scope; subsequent Concept design, Design, Detailed design
and realization stages require their own recorded sign-offs. Keep the lifecycle
progress/decision section in each spec current without conflating specification
status with stage progress or MiniPLM revision state.

The module's root `SPECIFICATION.md` is the human-readable development baseline.
Local `user/modules/<module>/SPECIFICATION.md` maps to `<module>/SPECIFICATION.md`
within the selected MiniPLM project/iteration. The MiniPLM project is the product;
`<module>/` is a folder. Keep agent check records local.

Use the [specification template](../../../templates/module-specification.md) when
starting a module. Existing equivalent specifications can be reconciled into this
root entry point without discarding accepted requirements or their history.

Each module spec identifies the approved project-spec revision and project
requirement IDs it implements, with module-level acceptance criteria. Check that
its scope and interfaces agree with the project baseline. Both the project spec
and the affected module spec must pass their entry gates before module
implementation. Other modules can remain in specification work if they do not
leave critical dependencies unresolved for the approved work.

## Complete for the agreed scope

Before module implementation, review the specification for:

- Purpose, intended use, boundaries, exclusions, responsible owner and development
  stage/scope. Define what work the baseline authorizes.
- Parent project-spec revision and allocation of project requirement IDs, with
  any derived module requirements identified and consistent with the project goal.
- Stable requirement IDs and objective acceptance limits, including units and
  tolerances where applicable. Define expected behavior and failure responses.
- Interfaces and dependencies: mating geometry/datums, wiring/pin assignments,
  supplies, signals, communications and software contracts as applicable.
- Operating conditions and constraints: loads, duty cycle, environment, power,
  materials/manufacturing, safety, cost or schedule where they affect the design.
- A verification method and pass criterion for every in-scope requirement, with
  physical measurements distinguished from calculations and simulations.
- Deliverables, component/dependency ownership and folder destinations, including
  native/STEP pairs, board libraries, source/build inputs and reports as applicable.
- Resolved assumptions and open decisions for the scope being approved. An
  inapplicable topic needs a reason; a critical unknown must be resolved before
  approval. Later-stage exclusions need explicit boundaries and owner acceptance,
  not a label used to conceal an unresolved in-scope requirement.
- A revision identifier and an actual approval decision for that revision and
  scope, with approver, date and decision provenance. Use the user's or designated
  owner's decision; the authoring agent must not invent approval.

Completeness concerns the requirements and interfaces needed for this stage;
design outputs such as the final feature tree or component selection can be
developed against those requirements. Do not demand a finished design in the spec.

## Entry decision

Use `DRAFT`, `IN_REVIEW`, `APPROVED` or `SUPERSEDED` for specification status.
Only `APPROVED` with the complete content and real decision above permits module
implementation. A file's existence, a status string or a green software check
does not prove completeness or approval. This is a reviewed workflow gate; the
existing fabrication/bench gate checkers do not enforce this entry decision.

Before approval, continue specification writing, source research and requirements
discovery. An explicitly scoped feasibility study can answer an identified open
question; keep its assumptions/results preliminary and distinguish it from module
implementation. Do not start module CAD, circuit/PCB design, product firmware/
software implementation or design-validation runs against an unapproved baseline.
Template maintenance, inspection of existing artifacts and specification review
do not require inventing a module or obtaining approval for the bootstrap.

If the spec is incomplete, report the exact missing decisions and prepare the
reviewable draft before seeking approval. Reuse approval already given in the
session or existing record for the same revision/scope; do not ask again for an
unchanged approved baseline. Engineering review may inform the decision but does
not replace the owner's approval or manufacture/bench authorization.

## Changes after approval

Preserve accepted project/module revisions and their decisions. For a requirements, interface or
scope change, draft a new revision, assess affected design inputs/checks and obtain
approval for the revised scope before affected implementation resumes. Unaffected
work can continue within the existing approved scope. Editorial corrections that
do not change requirements or scope do not need a new engineering approval.
Propagate approved project-level changes into affected module specifications;
resolve conflicting module requirements against the approved project baseline
rather than silently changing the overall goal.

Record both specification revisions in design decisions, reports and gate inputs.
Include actual project and module specification files among applicable local gate `design_inputs`
so byte hashes detect baseline changes; include its saved MiniPLM revision in
handoff traceability when available. Specification approval permits the agreed
development work, not a claim of verified hardware or readiness to manufacture.
Apply this entry gate identically in local-only mode.
