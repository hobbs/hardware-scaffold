# Firmware playbook

Firmware is part of the device design, not a substitute for electrical protection
or a reliable mechanical interface.

## Workflow

1. Define one `PROTO-###` firmware phase with a narrow goal, explicit exclusions,
   physical setup, checks, and exit criteria before creating source.
2. Inspect the exact received controller revision. Record markings and, when
   available, USB VID:PID and bootloader identity. Resolve those observations to a
   documented board target; do not select a near-name board definition from memory.
3. Choose the platform/framework only after the controller and constraints are
   known. Pin remote platforms to immutable revisions and pin every added library.
4. Prove the host toolchain on the actual workstation before building application
   structure. Record installer source, CLI version, host architecture, resolved
   compiler/framework packages, and any vendor-supported compatibility layer.
5. Mirror reviewed interface names from `docs/interfaces.md` in a single pin/config
   module. Explain unavoidable board-specific aliases.
6. Materialize only the phase's layout: build configuration, hardware configuration,
   smallest diagnostic application, and `firmware/README.md`.
7. Keep secrets and machine-local port settings outside version control.
8. Bring up one interface at a time with known-good test firmware.
9. Add deterministic host tests for pure logic and hardware-in-the-loop checks for
   behavior dependent on real peripherals, timing, analog values, or power states.
10. Measure active, idle, sleep, boot, radio, display, and fault-mode current on the
    real device.

## Firmware phase entry gate

Before materializing `firmware/`, confirm:

- the BOM distinguishes proposed hardware from the exact received variant;
- `docs/interfaces.md` owns every pin, peripheral instance, active level, reset
  state, and source-coexistence rule used by the phase;
- the physical build plan names the permitted power source and everything that must
  stay disconnected;
- the phase says what remains closed or absent, not only what will be exercised;
- a build identity and structured diagnostic format are defined; and
- the verification artifact has a place for failed attempts, measured values,
  deviations, and raw logs.

If USB enumeration contradicts the proposed BOM or board target, update the BOM,
interface contract, and source evidence before changing firmware configuration.
USB identity is evidence of the selected bootloader/application target; it does not
replace physical marking and revision inspection.

## Toolchain and first-build gate

Use the platform's documented installer without `sudo`, ad hoc package overrides, or
an unrelated IDE bundle. If the selected platform resolves a host-incompatible
compiler, use only a vendor- or OS-supported compatibility layer; otherwise stop and
request a proper prerequisite installation.

For PlatformIO projects:

1. Install PlatformIO Core with its official isolated installer and record the
   observed Core version. Shell links belong in the user's local bin directory.
2. Pin Git platforms and Git libraries to full commit hashes. Keep `upload_port` and
   `monitor_port` out of `platformio.ini`.
3. Run `pio device list` before selecting the board. Record both application and
   bootloader VID:PID values when they differ.
4. Run the smallest target build immediately. This resolves the actual framework,
   compiler, uploader, and bundled-library versions and exposes host-architecture or
   core-linkage failures before application structure grows.
5. Prefer the framework-bundled dependency when vendor documentation requires one;
   make it discoverable to the build explicitly rather than fetching an unpinned
   newer registry library.

An upload command's zero exit status is not proof that the device was programmed.
Retain the raw uploader output, require a protocol-level success indication, then
observe the new build identity over the intended diagnostic interface. Preserve a
failed attempt as separate evidence before retrying. Record manual bootloader entry
and recovery steps when automatic reset does not work.

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
