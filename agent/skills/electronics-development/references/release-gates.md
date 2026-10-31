# Release records and checker contract

Run `python <skill>/scripts/check_release.py <board-config> --stage prototype|bench|qualified [--output report.json]`.
Default is read-only stdout. Exit codes: 0 READY, 1 BLOCKED, 2 INVALID. No engineering tools, instruments or shell commands are executed. Rerun when claiming readiness; saved reports are snapshots, not permanent approval. A passed record requires honest engineering judgement; hashes cannot establish that a calculation or measurement is correct.

## Stage requirements (cumulative)

- Prototype: `operating-envelope`, `component-review`, `design-checks`, `protection-review`, `thermal-analysis`, `layout-review`, `manufacturing-review`, `bringup-plan`.
- Bench: prototype plus `assembly-inspection`, `unpowered-checks`, `logic-bringup`, `bench-test-setup`. The first three require physical records. The bench gate precedes powered functional/load testing; initial low-energy, load-disconnected logic bring-up follows the prototype's approved procedure and its shutdown limits.
- Qualified: bench plus `functionality`, `thermal-measurements`, `transient-measurements`, `fault-measurements`. All four require physical measurements across the declared envelope. Functionality includes implemented control-loop behaviour/timing and sensor noise when applicable.

Each project defines numerical criteria appropriate to its actual parts and application. Low-power or inapplicable hazards may be resolved by a reasoned review artifact at the relevant design gate; do not omit the requirement or claim an unperformed measurement. The qualified stage is intentionally a physical-hardware stage, not appropriate to a simulation-only project. No N/A or waiver shortcut exists in v1. Do not use this generic low-voltage prototype workflow as a substitute for application-specific certification or hazardous-energy engineering.

## Minimal JSON interface, schema_version 1

The board config contains `schema_version: 1`, `board`, `revision`, `project_root` (relative to the config's directory), `design_inputs` (a nonempty unique array of paths relative to project_root), and `evidence_file` (relative to project_root). Include all authoritative design inputs: schematics and referenced sheets, PCB, settings/local libraries, BOM, connector/MCU allocations and applicable operating requirements/firmware. Use individual file paths; hashes are byte-level, not Git commit IDs. Library and dependency files outside the project must be represented by a pinned local manifest/artifact, rather than silently omitted. No paths may escape project_root, including through symlinks.

The evidence file has `schema_version: 1`, matching `board` and `revision`, and `checks`, an object keyed by the requirement IDs above. A record starts with `status: blocked` and a truthful `summary`; missing requirements remain blocked. Valid statuses are `passed`, `failed`, `blocked`, `skipped`. Unknown statuses/configurations fail closed.

A passed record additionally requires:

- `kind`: review, calculation, simulation or measurement. Physical requirements accept measurement only.
- `acceptance`: numerical limits or an objective review criterion; `summary`: observed result and interpretation.
- `performed_by` and `performed_at` (ISO-8601 with timezone).
- `design_inputs_sha256`: the complete current path-to-SHA256 map for the config's inputs.
- `artifacts`: nonempty array of `{ "path": "relative/file", "sha256": "..." }` pointing to supporting results/reviews/raw data.
- Measurements also require nonempty `board_serial`, `conditions` and `instruments` strings. Include firmware, setup/probe identities and calibration information in the supporting artifact.

The checker verifies presence, kind, status and hashes. It does not interpret plots, audit the claimed criteria, or prove the operator performed the test. Do not auto-promote legacy summaries to passed release evidence. To retain an unaffected result after a design change, record an actual dependency review, retain the original result and link both artifacts; do not mechanically refresh hashes.

For new projects, bootstrap the configuration and blocked records for the requested board only. Keep criteria with the board and records under project evidence. Preserve existing validator schemas and commands. Never label manufacturing artifacts release-ready until the prototype gate passes, and keep prototype manufacture distinct from qualified operation. Ordering still requires user authorization.
