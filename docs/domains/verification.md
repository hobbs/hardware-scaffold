# Prototype and verification playbook

## Before assembly

- Freeze the exact prototype BOM and assign a build ID.
- Compare received items with their BOM variants and dimension drawings.
- Review schematic, harness, polarity, connector view, and mechanical access.
- Prepare expected continuity/resistance, rail voltage, and current-limit values.
- Prepare firmware that keeps outputs safe and exposes basic diagnostics.

## Bring-up sequence

1. Inspect mechanically and electrically with power absent.
2. Check shorts/resistance to ground and continuity through the harness.
3. Power individual rails/blocks with current limiting where practical.
4. Confirm rails, reset/boot, and idle current before attaching expensive loads.
5. Add peripherals one at a time; test expected and fault states.
6. Measure peak and steady current, voltage drop, temperatures, radio/display load,
   and sleep/off states under representative conditions.
7. Assemble the enclosure and repeat critical functional, access, RF, thermal, and
   runtime tests. Open-bench success is not integrated-device success.

## Evidence discipline

Record the build ID, source/firmware/CAD revisions, test conditions, instrument,
units, observed value, and raw artifact. Do not overwrite failed tests; link the
change and rerun as another dated result.

## Release bundle

A reproducible hardware revision contains:

- project brief, architecture, interfaces, risks, decisions, and verification;
- exact BOM, alternates policy, source register, and essential datasheets/drawings;
- KiCad sources and an ERC report;
- WireViz source and generated build diagram;
- CadQuery source, tests, assembly STEP, and per-part fabrication exports;
- firmware source, dependency lock/config, build/flash instructions, and version;
- assembly, first-power, calibration, operation, and known-limit instructions.
