# Firmware playbook

Firmware is part of the device design, not a substitute for electrical protection
or a reliable mechanical interface.

## Workflow

1. Choose the platform/framework after the controller and constraints are known.
2. Mirror reviewed interface names from `docs/interfaces.md` in a single pin/config
   module. Explain unavoidable board-specific aliases.
3. Keep secrets and machine-local port settings outside version control.
4. Make build, flash, serial-monitor, and test commands discoverable in
   `firmware/README.md`.
5. Bring up one interface at a time with known-good test firmware.
6. Add deterministic host tests for pure logic and hardware-in-the-loop checks for
   behavior dependent on real peripherals, timing, analog values, or power states.
7. Measure active, idle, sleep, boot, radio, display, and fault-mode current on the
   real device.

## Simulation

Wokwi is preferred for early tests of supported MCU/peripheral logic because its
circuit description is text and lintable. Treat unsupported development-board
features, analog/power behavior, exact display integration, and timing as real-
hardware tests. Never infer battery runtime or regulator thermals from digital
simulation.

## Required behavior to define

- Power-on and reset state; outputs must not briefly drive dangerous loads.
- Missing/disconnected sensor and bus-lock behavior.
- Watchdog and brownout behavior.
- Configuration/update recovery and version reporting.
- Safe shutdown and storage state.
- Logging/diagnostics needed for prototype measurements.
- Which behaviors are fail-safe in hardware versus best-effort in software.
