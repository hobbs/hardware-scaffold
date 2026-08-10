# Firmware

Select the framework only after the controller and constraints are known. Keep this
README current with exact commands and versions.

## Target

- Controller / board: TBD (`PART-###`)
- Framework / SDK: TBD
- Toolchain version / lock: TBD
- Logic voltage: TBD

## Interface configuration

Keep all board-specific pins and peripheral instances in one obvious configuration
module. Mirror the reviewed names and active levels in `docs/interfaces.md`; do not
scatter raw GPIO numbers through application logic.

## Commands

```text
# Build
TBD

# Flash
TBD

# Serial monitor / logs
TBD

# Host tests
TBD

# Hardware-in-the-loop smoke test
TBD
```

## Bring-up firmware

Start with outputs in safe/off states, report reset reason and firmware revision,
then test one rail/interface at a time. Keep useful peripheral-test programs or
diagnostic modes instead of deleting them after initial bring-up.

See `docs/domains/firmware.md` for simulation, power measurement, and fault behavior
expectations.
