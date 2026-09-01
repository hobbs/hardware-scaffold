# Firmware development plan

Materialize this artifact only when the firmware stack decision and first hardware
bring-up phase contain real project facts. Delete this guidance while adapting it;
do not create an empty phase schedule.

## Stack decision — DEC-###

Record:

- selected build system, framework/runtime, language, and execution model;
- exact received controller identity and supporting `SRC-###` records;
- exact board definition and why it matches the received unit;
- options considered and project-specific tradeoffs;
- pinned platform and dependency policy;
- host-test boundary versus hardware-in-the-loop boundary; and
- conditions that would force reconsideration for the final product.

## Cross-phase invariants

Define once:

- permitted power source and sources that must remain disconnected;
- startup-safe pin states and the single authoritative configuration module;
- diagnostic format and rate limits;
- local/private configuration that must remain untracked;
- terminology shared with the UI and interface contract;
- failure behavior that every phase preserves; and
- receiving-inspection or safety gates that block phase advancement.

## Phase — PROTO-###: narrow bring-up goal

### Goal

State one hardware/software fact this phase will prove. Name every peripheral,
behavior, and power path deliberately excluded.

### Build

List only code and configuration required to prove the goal. Include the build
identity, expected diagnostic records, and behavior preserved from prior phases.

### Physical setup

Link the authoritative assembly and interface artifacts. Name the exact modules,
connections, permitted power source, disconnected sources, bootloader method, and
instrument setup.

### Check

Use an ordered procedure from unpowered inspection through build, upload, runtime
observation, measurements, fault checks, and repeatability. Give expected values and
stop conditions before power is applied.

### Exit

Define observable pass criteria for the real hardware. A successful compile is not a
hardware-phase exit. Require raw evidence and identify any result that must update
`docs/interfaces.md` before source changes.

### Evidence

Assign `TEST-###` rows and raw log paths. Preserve failed attempts separately from
successful retries. Record instrument, setup, operator action, measured value,
firmware/build identity, and deviations; never infer an untested power path from a
USB-powered result.
