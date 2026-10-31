---
name: design-review
description: Perform an evidence-based, ideally independent engineering design review for electrical, mechanical, RF, optical, simulation, integration and fabrication changes. Use when assessing risk, readiness or compliance with requirements, not to rubber-stamp an author's work.
---

# Design review

Review the **design evidence**, not the author's confidence. Follow [review report contract](references/review-report.md) and $engineering-workflow. For board release, apply the existing $electronics-development release checker as well; a generic design review cannot replace it.

## Review steps

1. Establish scope, requested gate, revision, interfaces and baseline requirements with explicit acceptance limits. Read applicable owner instructions, decisions, native sources, prior findings and evidence.
2. Prefer a **separate reviewer agent/session** with no participation in the original design. State reviewer independence honestly. If the author performs the review, classify it as `SELF_REVIEW`, not independent approval.
3. Reproduce critical calculations and rerun available static checks/simulations where practical. Do not assume a log, plot or solver exit proves correctness. Inspect claimed measured evidence and calibration/provenance.
4. Review boundaries: load/voltage extremes, mechanical tolerances and interferences, RF assumptions, optics alignment, thermal paths, manufacturing/assembly, control-loop coupling, safety and testability as applicable.
5. Write actionable findings with severity, requirement, affected artifact/line or feature, evidence, consequence and a concrete corrective action/test. Differentiate a demonstrated failure from a risk or unknown.
6. Re-review changes and close findings only with cited evidence. Preserve historical failed/blocked findings and mark exclusions with rationale.
7. Return `PASS`, `BLOCKED` or `NEEDS_REVIEW` **for a named gate and scope**. Unknown, stale, failed or skipped mandatory checks block that gate. Pass cannot authorize manufacturing, purchasing or powered operations.

## Output

Produce a project-local review record with revision, reviewer and independence, design inputs, checks actually performed, findings, dispositions, gate status, residual risks and required next tests. If no native source or evidence was available, report a document-only assessment or `NEEDS_REVIEW`; do not present it as a verified design review.

A reviewer's approval is engineering advice. A physical prototype, measured performance, regulatory compliance or production release still requires the corresponding domain gates and user decisions.
