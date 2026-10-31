# Common engineering gates and handoff contract

This document standardizes language and evidence across hardware disciplines. It does not override stronger board-, product-, safety- or regulation-specific procedures.

The [shared executable checker](gate-engine.md) implements configurable
mechanical/simulation/integration evidence checks, with an adapter to the existing
electrical checker. Its `READY/BLOCKED/INVALID` output is intentionally narrower
than formal engineering approval; a recorded reviewer identity cannot prove
independence or physical validity.

## Lifecycle and decisions

| Milestone | Minimum evidence | Permitted claim |
| --- | --- | --- |
| Scope established | Requirement IDs; intended environment; interfaces; hazards; measurable acceptance; open decisions | Scope drafted, not feasibility proved |
| Design prepared | Native sources, revision, design calculations, trade-offs, part/material identities, assumptions | Design candidate |
| Design reviewed | Applicable simulation/analytical reports; domain checks; independent review findings and disposition | Design review completed, with explicit blockers |
| Prototype-ready | Current reviewed sources; DFM/DFA/DFT; BOM/materials; drawings/export checks; test/bring-up plan; applicable domain release gate | Engineering prototype package ready for user authorization |
| Bench-ready | Actual build/revision/serial; assembly inspection; safe low-energy/unpowered test records; approved procedures and shutdown limits | Controlled next physical test may be proposed, not autonomously performed |
| Validated | Measured acceptance results across the declared operating envelope; uncertainties, anomalies, deviations and calibration | Product verified/validated for the tested scope only |

The electronics-development gate names `prototype`, `bench`, and `qualified` remain authoritative for electronics and include their own stricter record requirements. A simulated result cannot satisfy a measurement gate.

## Minimum handoff record

Record these in the owning project's `docs/` or `evidence/` as appropriate. Use machine-readable metadata if an orchestrator will consume it.

- Task and engineering baseline: project/subsystem, revision/commit or file hashes, author/date, gate requested.
- Requirements: stable IDs, units, limits, tolerances and acceptance criteria; unresolved values explicitly marked **proposed**.
- Design: authoritative native files, interfaces, material/part variants, assumptions, failure modes and affected dependencies.
- Verification: methods (inspection, calculation, simulation, review or measurement), exact configurations/solver versions/instrument calibration, conditions, raw artifacts and hashes.
- Results: expected versus actual with uncertainty, pass/fail **per criterion**, coverage and known limitations.
- Review: reviewer identity, findings by severity, resolutions, residual risks and decision status.
- Next step: responsible party, remaining blockers, proposed action and whether user authorization is required.

Label each claim as `proposed`, `analytical`, `simulated`, `synthetic`, `measured` or `confirmed` as applicable. Preserve source data and failures. Do not rename a proposed design target as a proven result.

## Review gates

Use `PASS`, `BLOCKED` or `NEEDS_REVIEW`. A gate is BLOCKED if a required check is absent, failed, stale, skipped without documented disposition, or contradicted by evidence. `PASS` means the declared scope's evidence and reviews met their criteria; it is not certification and never permission to purchase, transmit, operate hazardous equipment or manufacture.

Rerun affected checks after design changes; an unchanged dependency may retain prior evidence only after documented impact review. State which gates were **not** evaluated.

## Rigor scaling

- **Exploratory:** rapid native design and analytical feasibility work; disclose unknowns and prohibit readiness claims.
- **Prototype:** objective acceptance criteria, reviewed interfaces, repeatable analyses, fabrication/test package and applicable release checks.
- **Qualification:** controlled revisions, independent verification and representative calibrated physical measurements; project-specific regulatory/compliance work as required.
