# Reproducible simulation run record

Use a project-local Markdown or structured record. These fields are mandatory when claiming a result; mark unavailable values explicitly.

| Field | Required content |
| --- | --- |
| Run ID and status | Unique run ID; PLANNED, RUN, FAILED or NOT_RUN |
| Objective | Requirement ID, predicted observable, acceptance and decision supported |
| Baseline | Source revision/commit or input hashes; model/source files and linked dataset identity |
| Execution | Solver and exact version, command/API invocation, environment, runtime settings, seed where relevant |
| Model | Relevant geometry/netlist, units, coordinate frames, physics included/excluded and model limitations |
| Cases | Stimuli, loads, boundary/initial conditions, parameter corners, tolerance or uncertainty ranges |
| Quality | Warnings, convergence criteria, mesh/timestep refinement and analytical cross-check |
| Results | Raw numeric outputs/paths and hashes, plots, uncertainty and per-criterion pass/fail |
| Reproducibility | Instructions to reproduce and expected artifacts; deviations or failures |
| Next measurement | Instrumentation, setup and comparable observable for physical verification |

Suggested outcome language:

- `PASS (SIMULATED)`: simulated results met the declared criteria within model assumptions, **not** physical qualification.
- `FAIL (SIMULATED)`: one or more criteria not met; preserve failed runs.
- `INCONCLUSIVE`: solver convergence, model validity or uncertainty cannot support the claim.
- `NOT_RUN`: instructions or example were produced, but no solver executed.

Never describe screenshots without accessible result data as verified numerical evidence. For multiple parameter sweeps, report all cases, worst-case margins and failed/unstable runs rather than only a nominal plot.
