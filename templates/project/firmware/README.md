# Firmware

Materialize this file only after the controller, framework, first `PROTO-###` phase,
and reviewed interface contract are known. Replace this guidance with concrete
project facts; do not retain empty headings or example values.

## Phase contract

Record the active prototype ID, one-sentence goal, explicit exclusions, permitted
power source, disconnected sources/loads, and exit criteria. Link the detailed phase
in `docs/firmware-plan.md` when that artifact exists.

## Target identity

Record all of the following before selecting a build target:

- `PART-###` and received product/revision markings;
- application USB VID:PID and serial identity, when available;
- bootloader VID:PID and serial identity, when different;
- exact build-system board identifier;
- source IDs that connect the received identity to that board definition; and
- unresolved receiving-inspection limits.

USB enumeration can disprove a proposed target, but it does not replace physical
marking and revision inspection.

## Pinned toolchain

Record the tested host OS/architecture, supported installation method, CLI version,
immutable platform revision, resolved framework/core, compiler, uploader, and every
added library version. State any vendor- or OS-supported host compatibility layer.
Do not solve host incompatibility with an ad hoc compiler override.

For PlatformIO, keep a full Git commit in `platformio.ini`, keep machine-local ports
out of it, and preserve the package versions printed by the first successful build.

## Interface configuration

Keep all board-specific pins and peripheral instances in one obvious configuration
module. Mirror the reviewed names and active levels in `docs/interfaces.md`; do not
scatter raw GPIO numbers through application logic. Set output latches to safe
levels before enabling their drivers, and leave excluded peripherals unopened.

## Layout

Describe the small set of materialized files and the responsibility of each. A first
phase normally needs only:

- one pinned build configuration;
- one hardware configuration module;
- one diagnostic application; and
- this command and recovery record.

Do not create parser, display, state-machine, or test scaffolding before the phase
uses it.

## Commands

Record the exact working directory and exact commands for:

- tool/version check;
- build;
- bootloader entry;
- upload;
- device discovery;
- serial/log monitor;
- host tests, when portable logic exists; and
- hardware-in-the-loop smoke test.

Label each command `verified`, `pending hardware`, or `not applicable`, with the last
execution date. Never commit `/dev/...`, `COM...`, or another machine-local port to
the build configuration; document the observed command here or use an environment
variable.

## Upload and recovery

Document normal and manual bootloader entry, expected application and bootloader
identities, and recovery from an interrupted upload. A zero process exit status is
not enough: require the uploader's protocol-level success indication and then
observe the new firmware build identity. Retain failed and successful upload logs as
separate evidence.

## Expected diagnostics

Define the machine-readable boot record, build identity, reset reason, heartbeat or
progress rate limit, and expected fault records. State which diagnostic interfaces
remain deliberately closed.

## Verification evidence

Link the applicable `TEST-###` rows in `docs/verification.md` and raw logs. Record
actual instruments, power topology, measured values, operator actions, failed
attempts, and deviations. A USB-powered check does not prove a bench-supply or
battery path.
