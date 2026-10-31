# Checks chosen by electrical consequence

| Change | Required review and useful verification |
| --- | --- |
| Component or schematic | Datasheet variant, pin functions, absolute versus recommended limits, startup states, tolerances, derating, footprint/pad mapping and ERC; MCU pin multiplexing needs firmware verification |
| Power or protection | Supply extremes, startup/shutdown, sequencing, load steps, hot-plug, reverse polarity, overcurrent/overvoltage and regenerated energy; check the complete local energy path |
| Power stage or load | Actual load R/L, current and duty limits; conduction/switching losses at temperature; current regulation, sensing, braking/recirculation and fault response |
| Thermal | Worst-case loss budget, PCB copper/vias, enclosure/ambient and neighbouring heat sources; thermal resistance is layout dependent; follow with physical temperature measurements |
| Layout | DRC and schematic-to-PCB connectivity, current loops/returns, reference planes, decoupling, sensitive analog routes, creepage/clearance appropriate to the application, test access and mechanical interfaces |
| Analog or sensors | Input range/protection, filtering, noise/error budget, ADC reference, sampling and settling; tolerances and supply/temperature dependence |
| Control or firmware | Real sample rate, delays/jitter, polarity, saturation, anti-windup where used, watchdog/reset/brownout, communications/sensor loss and disabled-output behaviour; simulation must describe omitted device physics |
| Fabrication | Board stackup, copper, manufacturer rules, footprints, polarity, BOM substitutions, placement/paste, exposed-pad treatment, connector orientation and access |

Choose bounded, repeatable analyses that answer a design question. Record expected behaviour and pass/fail limits before declaring success. A model with assumed coils/suspension is exploratory evidence, not qualification of a power stage or real closed loop. Never apply motor-specific constants to unrelated designs.

Do not rerun everything for every small change. Identify dependencies, rerun affected checks and carry forward other evidence only through a documented review of its still-applicable inputs. A full-design hash change deliberately invalidates release records until that assessment is recorded.
