# Staged prototype bring-up

Write the board-specific procedure and numerical shutdown limits before powering hardware. Do not assume the user owns instruments or permit destructive tests through this skill.

1. Verify assembly identity/revision, orientation, soldering, connectors and accessible test points. Check unpowered rails for shorts; account for capacitors and parallel paths when interpreting resistance.
2. With loads disconnected and outputs disabled, use a suitable current-limited supply. Establish input polarity, ramp/sequence, current limit and stop conditions from the design. Measure rails, idle current and abnormal heating before programming.
3. Establish SWD/programming, clocks, communications, sensor input plausibility and safe reset/watchdog states. Calibrate monitoring as needed. Record low-energy logic bring-up; this is not a load test.
4. Establish the bench gate: appropriate instruments, suitable dummy loads, wiring/grounding, bounded fault energy, known safe firmware and emergency disable. Progress from reduced limits to real loads only within the written procedure.
5. Measure functionality, temperature through thermal equilibrium, supply/load transients and controlled fault response over the intended envelope. Record raw waveforms, board serial, firmware, instrument/setup identities and conditions. Include actual sampled control and sensor-noise measurements for controllers.

Do not connect an oscilloscope ground clip to a switching node. Select suitable differential/isolated measurement methods where required. Short-circuit, reversed-supply and other fault tests require a separately justified energy-limited setup; they are not casual first-power checks.

Qualification applies only to the tested hardware, firmware and conditions. Formal EMC, electrical safety or environmental compliance requires its own applicable programme.
