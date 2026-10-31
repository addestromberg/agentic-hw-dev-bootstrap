# Mechanical design verification checklist

Apply only checks relevant to the actual change; identify exclusions and their rationale.

| Topic | Engineering checks |
| --- | --- |
| Requirements | Defined loads, environment, duty cycle, envelope, access, assembly/disassembly and inspection features |
| Geometry | Native model recomputes; intended dimensions/units; sketch constraints; no unintended self-intersection or invalid solids |
| Datum and interfaces | Coordinate systems; optical/rotational/electrical axes; mating interfaces and fastener locations; cable/connector clearance |
| Fits | Tolerance stack including print, machining and assembly variability; fastening method, clearances and travel across extremes |
| Structures | Load cases and boundary conditions; static stress, stiffness, buckling where relevant; fatigue for repetitive motion |
| Dynamics | Mass, inertia, centre of gravity, rotational balance, first structural modes relative to actuation/control bandwidth |
| Thermal and environment | Expansion mismatch, temperature-dependent properties, water/UV/chemical exposure, corrosion, sealing |
| Fabrication | Print orientation/supports, min walls, resin post-cure/shrinkage; machining access, casting porosity or composite layup as applicable |
| Assembly and service | Tool access, misassembly prevention, cable strain relief, replacement and calibration points |
| Deliverables | Native CAD, reproducible exports with units, drawings and tolerances, BOM/material specifications, evidence/revision and physical inspection plan |

For a fast-steering optical mirror, explicitly consider mirror+mount inertia, actuator force/torque, mechanical resonance, travel/stop limits, alignment and the thermal effects of actuator losses. Do not assign nominal stiffness, modulus or mirror mass without a source.

For FEM, document geometry simplifications, boundary conditions, material properties, mesh convergence, contact assumptions and independent hand calculations. Solver success alone does not constitute structural verification; see $simulation-engineering.

When source or solver access is missing, propose a test or calculation and identify the blocker instead of implying execution.
