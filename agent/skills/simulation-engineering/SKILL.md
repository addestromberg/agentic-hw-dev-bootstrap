---
name: simulation-engineering
description: Plan, run and evaluate reproducible engineering simulations and analytical cross-checks across SPICE electronics, controls, mechanics/FEM, RF/EM and optics. Use when modeling performance, uncertainty, convergence or sensitivity; never equate simulation with physical verification.
---

# Simulation engineering

Use this skill when the task needs predictive analysis. Work with the applicable domain skill and the owning project's actual models; use $engineering-workflow for requirements and release handoffs.

## Simulation protocol

1. **Question:** specify requirement ID, measurable output, acceptance threshold, operating envelope, expected failure mode and what the model is capable of answering.
2. **Provenance:** record source revision, geometry/netlist, material/datasheet/model versions, solver and settings, units, reference frames, stimuli, boundary conditions and assumptions.
3. **Sanity baseline:** compare with an independent analytical estimate or simple case. Check energy/current conservation, dimensions and sign conventions where applicable.
4. **Execution:** choose an appropriate available tool (e.g. ngspice for circuits, SciPy/control for control loops, CalculiX/FreeCAD FEM for structures, openEMS for supported full-wave RF, ray tracing for optical models). Never invent a run or claim tools are installed without checking.
5. **Numerical quality:** test timestep/mesh/convergence, solver warnings, parameter sensitivity and relevant extreme tolerances. Explain idealizations and missing coupled physics.
6. **Interpretation:** compare outputs and uncertainty margins against declared acceptance, record failures and alternatives. Flag whether the result is analytical, synthetic or simulated.
7. **Correlation:** propose calibrated physical measurements with comparable stimulus, geometry, load and units; simulation cannot replace bench results. Route blocking results to $design-review.

Use [reproducible run record](references/reproducible-simulation.md) and retain native source/mesh/netlist/config, logs, plots, numerical results and exact invocations in the **owning project**, not inside the shared skills. Keep raw and processed data linked and checksummed.

## Evidence and gate integration

For simulation release claims, follow the
[shared gate schema](../engineering-workflow/references/gate-engine.md):
record the solver/version, model limits, convergence status, source hashes,
required numerical criteria, corners, raw artifacts and independent review.
When a project gate config exists, run
`python SKILLS/engineering-workflow/scripts/check_gates.py <config> --stage prototype`.
Changes to any configured source invalidate downstream evidence until
rechecked; this checker evaluates claims and evidence, not solver physics.
Do not mark `READY` when the simulation has not actually run.

## Tool-specific cautions

- **SPICE:** models may omit nonlinear losses, parasitics, protection, stability limits or actuator mechanics; sweep realistic corners and sources.
- **FEM:** constraint/contact assumptions and mesh convergence can dominate apparent stress and resonances.
- **RF:** a simplified array factor or analytical radiation plot is not coupled full-wave gain, S11 or a measured antenna pattern.
- **Control/optics:** include sampling, latency, noise, saturation, actuator bandwidth and flexible structures where material; ideal plant response is not demonstrated tracking performance.

Do not change model inputs to make a result pass without documenting the revision. If execution is impossible, provide a runnable plan and explicitly mark `NOT_RUN`.
