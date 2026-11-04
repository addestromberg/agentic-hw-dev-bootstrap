# PLM lifecycle and stage sign-off

Use this ordered stage-gate lifecycle for the product and each affected module.
The MiniPLM project is the product. Project requirements and approved interfaces
flow down into module specifications; module evidence and integration results
flow back into product acceptance. Sign-off applies to identified revisions and
scope, not every future change to a named folder.

The bootstrap defines this workflow without approving a product, creating remote
stages or performing physical work. Use the same gates with local-only storage;
report the absence of PLM version control.

## Stages and exit evidence

Each stage ends with a reviewable package and an owner decision before the next
applicable stage begins. Prepare proportionate evidence for the approved scope.

| Stage | Work and evidence required for sign-off |
| --- | --- |
| Conceive | Product need, intended users/use, desired outcome, boundaries, feasibility questions, owner and proposed module responsibilities. Sign-off authorizes specification work. |
| Specification | Complete project and affected module specifications: measurable requirements, interfaces, allocation, constraints and verification/acceptance plan. Actual approval of both baselines precedes concept design. |
| Concept design | Alternatives, feasibility evidence, selected architecture/principle, key interfaces and justified trade-offs. Sign-off selects the concept to develop. |
| Design | Coherent module/system design, native CAD/circuit/software architecture as applicable, interface definitions, preliminary BOM/materials, calculations and risk disposition. Sign-off accepts the design direction for detailing. |
| Detailed design | Complete editable sources and dependencies, dimensions/tolerances, electrical connectivity/layout, firmware/software/build inputs, BOM and checked native/export pairs. Sign-off establishes the candidate baseline for formal analysis. |
| Validation and analysis (simulation) | Traceable analytical/simulation reports against approved requirements, model limits, convergence/sensitivity checks, margins and review findings. Sign-off records what analysis supports and what still needs physical verification; it does not establish a tested product. |
| Tool design | Required jigs, fixtures, moulds, tooling or test fixtures with native designs, tolerances/interfaces, analyses and inspection plan. If no custom tooling is needed, record the reason and owner-approved applicability decision. |
| Realise | Review the design/analysis/tooling baseline, make/buy choices, resources, responsibilities and open risks; approve the scope entering realization planning. This is a transition decision, not a claim that parts exist or permission for unspecified physical actions. |
| Plan manufacturing | Reviewed process/routing, material/supplier choices, fabrication package, tooling/setup, assembly sequence, inspection/test plan and acceptance criteria. Run applicable domain prototype/manufacturing gates; obtain explicit authorization before purchasing or fabrication. |
| Manufacture | Actual authorized fabrication/procurement with batch/part/material identities, inspection records, deviations and disposition against the released baseline. Sign-off accepts identified parts for assembly; planned orders or generated files are not manufacturing evidence. |
| Build/assemble | Actual assembly/as-built identity, parts/firmware revisions, wiring/alignment/fastening records, inspections and deviation disposition. Run applicable bench gates before powered functional/load testing and obtain authorization for the physical action. |
| Test (quality control) | Actual inspections and tests against approved criteria, calibrated setup where relevant, results/failures, serial/batch traceability and nonconformance disposition. Include module and product integration evidence; use qualified gates where applicable before claiming qualified performance. |

Calculations, exploratory simulations and DFM feedback may inform earlier stages
within their approved scope; the named analysis stage is the consolidated review
of the detailed baseline. Do not defer all engineering checks until that stage.
Failures return affected work to the relevant earlier stage. Retain prior
results and decisions, revise sources, then repeat affected reviews/checks.

## Top-down approval and product integration

1. Establish the product goal and lifecycle scope in root `SPECIFICATION.md`.
   Conceive sign-off permits specification work, not design implementation.
2. Approve the project specification and its requirement/interface allocation.
   Complete and approve an affected module's root `SPECIFICATION.md` consistently
   with that baseline before concept design or implementation for that module.
3. Review module stage evidence and coupled interfaces. A product-level gate
   aggregates the necessary module decisions and integration evidence; a module
   pass alone does not establish a product pass. Modules may progress separately
   where their approved interfaces and dependencies permit it.
4. At physical stages, compare the actual built revision and measured behavior
   with the approved requirements. Preserve discrepancies, corrective actions
   and the exact scope of acceptance.

Research, requirement drafting and explicitly scoped feasibility work can help
prepare decisions before specification approval. Do not use those activities to
bypass an unapproved requirement or begin the module design as if it were signed
off. Approval already given for an unchanged baseline and scope remains valid.

## Sign-off records

Maintain a human-readable lifecycle/sign-off section in the project and module
specifications. Supporting readable review reports belong in the corresponding
`docs/`; simulation reports remain with their studies. Publish these human
deliverables in PLM with the scoped handoff. Raw logs, check JSON, upload receipts
and agent bookkeeping remain local under `agent/`.

Use stage progress `NOT_STARTED`, `IN_PROGRESS`, `IN_REVIEW`, `SIGNED_OFF` or
`NOT_APPLICABLE`. `SIGNED_OFF` requires an actual user/designated-owner decision.
For each decision record:

- Project/module, stage, exact specification and design revisions, and scope.
- Evidence/report references and requirement coverage, checks actually performed,
  unresolved findings and applicability decisions.
- Reviewer identity and honest independence (`SELF_REVIEW` when applicable).
- Decision, approver, date and source of the approval; next stage/actions covered.
- Any superseded decision and the reason for reopening it after a change.

The agent prepares and reviews evidence; it must not invent owner sign-off. The
owner may authorize several clearly scoped stages in one decision, but an early
approval does not silently extend to fabrication, purchases or powered tests.
Do not request approval again for each file or an already authorized action.
Present a concrete reviewable package at a gate before asking for a missing
decision. Report exactly what prevents sign-off when evidence is incomplete.

An inapplicable stage needs a reason and an owner-approved disposition; retain
the stage in the record. Applicability cannot waive mandatory domain checks or
turn missing simulation/physical results into a pass. Existing electronics
`prototype`, `bench`, `qualified` gates retain their stricter requirements.
Specification approval authorizes entry to concept design; later stages have
their own sign-off. These records are reviewed workflow decisions, not a new
automatically enforced state machine.

## Changes and MiniPLM state

After a requirement, interface, design or process change, identify affected gates
and mark their previous sign-offs superseded/pending re-review for the revised
scope. Reapprove changed requirements top-down, then rerun affected checks and
reviews. Unaffected work can continue under its existing approved scope.

Keep lifecycle stage distinct from a MiniPLM design iteration, file revision or
folder. An iteration groups a design cycle; file revisions identify saved assets.
Inspect the target project's actual stages and map the workflow explicitly when
the connected tools support it. Available MiniPLM tools do not expose a general
stage-transition or approval operation: record sign-off in the readable documents
and do not claim a server-enforced transition occurred. Saving a file, creating
an iteration or generating a preview never constitutes sign-off. This template
does not create twelve remote stages or duplicate the deliverable tree per stage.

Retain project `SPECIFICATION.md` at the selected iteration root and module files
under `<module>/`, such as `wheel/SPECIFICATION.md` and `wheel/cad/`. The product
is the selected MiniPLM project, not a `product/` folder.
