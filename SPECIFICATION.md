# Project specification

- Product / MiniPLM project: Not established
- Specification revision: draft-1
- Status: DRAFT
- Owner: Not assigned
- Development stage and approved scope: Not established
- Current lifecycle stage: Not started
- Approval: None

This bootstrap has no accepted product goal or approved hardware requirements.
Complete this specification for the actual project before product implementation.
It is the product-level objective for engineering work; module specifications
derive their scope and requirements from this baseline. Template maintenance can
continue while this document is a draft.

Follow the [PLM lifecycle](user/docs/plm-lifecycle.md). Project requirements and
sign-off flow down to modules; their evidence and integration results support
project acceptance. Specification approval alone does not sign off later stages.

## Lifecycle and stage sign-off

Record actual stage evidence, reviewed revisions, scope and owner decisions.
Use `NOT_STARTED`, `IN_PROGRESS`, `IN_REVIEW`, `SIGNED_OFF` or an owner-approved
`NOT_APPLICABLE` with rationale. Nothing in this scaffold is signed off.

| Stage | Progress | Signed-off baseline, scope and decision reference |
| --- | --- | --- |
| Conceive | NOT_STARTED | None |
| Specification | NOT_STARTED | None |
| Concept design | NOT_STARTED | None |
| Design | NOT_STARTED | None |
| Detailed design | NOT_STARTED | None |
| Validation and analysis (simulation) | NOT_STARTED | None |
| Tool design | NOT_STARTED | None |
| Realise | NOT_STARTED | None |
| Plan manufacturing | NOT_STARTED | None |
| Manufacture | NOT_STARTED | None |
| Build/assemble | NOT_STARTED | None |
| Test (quality control) | NOT_STARTED | None |

For each sign-off identify reports and exact revisions, reviewer/independence,
decision, actual approver/date, approval source and authorized next scope/actions.
Keep previous decisions and identify those superseded after a baseline change.

## Product goal and completion criteria

State the intended product, who will use it, the outcome it must achieve and the
objective criteria that will show the project is complete. These are the goal
and success criteria for the engineering agent's work.

Not established.

## Scope and boundaries

Define intended use, system responsibilities, exclusions and the development
stage being authorized. Identify external systems, installation constraints and
assumptions that affect the whole product.

Not established.

## Project requirements and acceptance

Use stable project requirement IDs and objective limits, units/tolerances and
operating conditions. Cover product function, performance, failure behavior and
safety as applicable. Identify the verification method for each requirement.

| ID | Requirement | Acceptance limit and conditions | Verification method |
| --- | --- | --- | --- |
| Unassigned | Not established | Not established | Not established |

## Modules, interfaces and allocation

Identify the required modules, their responsibilities, system interfaces and
which project requirement IDs each module specification must address. Add relative
links to actual module-root specifications as those modules are established.
Do not create fictitious modules to populate this section.

Not established.

## Shared constraints and dependencies

Define the operating environment, envelope, loads, power, manufacturing, shared
materials/software, budget, schedule and applicable safety constraints that affect
more than one module. Identify authoritative external inputs and sources.

Not established.

## Integration and verification plan

Define how module evidence combines into system acceptance, which interfaces
need integration tests, and the conditions/resources for those tests. Distinguish
calculation, simulation, inspection and physical measurement. State the
deliverables and evidence needed to meet the project completion criteria.

Not established.

## Repository and deliverables

Identify the target MiniPLM project (the product) and design iteration when known.
The project specification maps to `SPECIFICATION.md` at that iteration's root;
local `user/modules/<module>/` maps to `<module>/` within it. Keep target IDs and
agent records under local `agent/`; the product is not a directory.

No target or project deliverable scope is established. If MiniPLM is unavailable,
retain the documented local structure and report the lack of PLM version control.

## Assumptions and open decisions

Identify unresolved values, owners, impacts and needed decisions. Resolve critical
in-scope decisions before approval. Later-stage exclusions need explicit scope
boundaries and owner acceptance.

Not assessed; this draft is incomplete.

## Review and approval

- Revision and scope reviewed: Not reviewed
- Completeness review and remaining blockers: Not reviewed
- Approver and role: None
- Approval date: None
- Decision and source of approval: None

## Change history

| Revision | Change | Approval impact |
| --- | --- | --- |
| draft-1 | Bootstrap specification scaffold; product goal not established | Unapproved |
