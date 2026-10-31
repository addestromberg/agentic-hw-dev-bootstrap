# Shared engineering gate engine

Read-only, standard-library Python checker. This evaluates **evidence records**; it does not run SPICE/FEM, prove model correctness, certify a product or authorize fabrication. The existing electronics-development \`prototype\`/\`bench\`/\`qualified\` checker is called unchanged when the electrical domain is selected.

\`\`\`sh
python SKILLS/engineering-workflow/scripts/test_check_gates.py
python SKILLS/engineering-workflow/scripts/check_gates.py path/to/gate.json --stage prototype
\`\`\`

Exit status: 0 \`READY\`, 1 \`BLOCKED\`, 2 \`INVALID\`. JSON is printed to stdout. Optional \`--output new-report.json\` creates a **new** report, refusing to overwrite any existing file.

## Config: schema_version 1

Store the config under the owning subsystem (not in \`SKILLS/\`). \`project_root\` is relative to the config's directory; all design inputs, evidence and electrical config paths are relative to the resolved project root and must not escape it. Include authoritative CAD, electrical, material, solver-model and controls files affected by the requirements.

\`\`\`json
{
  "schema_version": 1,
  "project": "mirror-holder",
  "revision": "prototype-A",
  "author": "design-agent",
  "project_root": "..",
  "domains": ["mechanical", "simulation"],
  "design_inputs": ["cad/mirror-holder.FCStd", "config/loads.json"],
  "evidence_file": "evidence/engineering-gates.json",
  "check_definitions": {
    "simulation.result-assessment": {
      "criteria": [{"metric":"first_resonance","op":"gte","value":500,"unit":"Hz"}]
    },
    "mechanical.manufacturing-review": {
      "depends_on": ["simulation.result-assessment"]
    },
    "mechanical.functional-measurement": {
      "criteria": [{"metric":"measured_deflection","op":"lte","value":0.05,"unit":"mm"}]
    }
  }
}
\`\`\`

The numbers above are **illustrative, not accepted SKYwatch specifications**. When selecting \`"electrical"\` in \`domains\`, also set \`"electrical_config": "config/board-release.json"\` to refer to the existing electronics gate's board config. The shared \`design\` stage does not grant electrical readiness: request \`prototype\` or later.

## Cumulative stage policy

| Domain | Stage | Required check names (prefix with domain) |
| --- | --- | --- |
| mechanical | design | cad-integrity, interface-review, tolerance-review, load-review |
| mechanical | prototype | manufacturing-review, independent-review |
| mechanical | bench | as-built-inspection, dimensional-measurement |
| mechanical | qualified | functional-measurement |
| simulation | design | model-provenance, analytical-baseline |
| simulation | prototype and later | convergence, corner-cases, result-assessment, independent-review |
| integration (when two or more domains selected) | prototype and later | interface-review |

\`mechanical.cad-integrity\` must report boolean \`valid_geometry=true\` and \`recompute_ok=true\`. Use the read-only helper \`SKILLS/mechanical-engineering/scripts/inspect_freecad.py\` (requires FreeCAD Python bindings) to produce an inspection artifact; record the results honestly.

For simulation \`convergence\`, \`corner-cases\` and \`result-assessment\`, records must include \`solver: {"name": "...", "version": "..."}\`, nonempty \`model_limits\`, \`converged: true\`; \`corner-cases\` additionally requires a \`cases_run\` metric >=2. \`simulation.result-assessment\` and \`mechanical.functional-measurement\` must have project-specific numeric criteria.

## Evidence schema

An evidence JSON file contains \`{"schema_version":1,"project":"mirror-holder","revision":"prototype-A","checks":{...}}\`. Each full check ID maps to a record similar to:

\`\`\`json
{
  "status":"passed",
  "kind":"simulation",
  "acceptance":"First mode >= 500 Hz under declared fixture and loads",
  "summary":"Simulated first mode 560 Hz with stated limitations",
  "performed_by":"simulation-agent",
  "performed_at":"2026-10-31T19:00:00+01:00",
  "design_inputs_sha256":{
    "cad/mirror-holder.FCStd":"<actual SHA-256>",
    "config/loads.json":"<actual SHA-256>"
  },
  "artifacts":[{"path":"evidence/fem-run.json","sha256":"<actual SHA-256>"}],
  "solver":{"name":"CalculiX","version":"2.x"},
  "model_limits":"Rigid mount, nominal properties; no actuator nonlinearities",
  "converged":true,
  "metrics":{"first_resonance":{"value":560,"unit":"Hz"}}
}
\`\`\`

Replace placeholders with actual evidence, paths and hashes. All \`passed\` checks require a nonempty acceptance, summary, identity, timezone-aware timestamp, current exact hashes of **every** configured input and at least one existing hashed artifact. Required missing, skipped or failed records block release. Physical measurement checks require \`kind="measurement"\`, \`specimen_id\`, \`conditions\` and \`instruments\`. Independent reviews require \`kind="review"\`, \`independent=true\`, a nonempty \`reviewer\` that differs from the config \`author\`, and \`performed_by\` equal to that reviewer. The declaration is checked; actual independence still needs a human or trusted workflow.

Numeric criteria use \`metric\`, \`op\` (\`eq\`, \`lt\`, \`lte\`, \`gt\`, \`gte\`), numeric/boolean \`value\` and optional \`unit\`; \`record.metrics[metric]\` must have a matching value and **exact** unit (no automatic conversions). Results are comparisons against recorded claims; the reviewer must examine actual solver/test artifacts.

For check dependencies, declare \`depends_on\` in \`check_definitions\`; the dependent evidence record must provide an \`upstream_sha256\` map to the SHA-256 of each upstream check's canonical JSON (sorted keys, compact separators, UTF-8). A changed/failed upstream record blocks downstream, and cycles are rejected. Every record also depends on all configured design inputs, conservatively invalidating both mechanical and simulation evidence when geometry or interface sources change. Do **not** merely update hashes to pass; rerun affected checks or document an actual dependency review.

Selecting domains defines the assessed scope; an omitted domain is **not checked**. A \`READY\` result is insufficient for manufacturing authorization, powered testing, physical performance or regulatory compliance. Integrate this checker into CI/Kaddeban for actual stage enforcement; skills alone cannot enforce execution.
