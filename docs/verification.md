# Verification matrix

Plan tests while writing requirements. Test the assembled device, not only isolated
code or CAD.

| Test | Requirement / risk | Method | Equipment / setup | Acceptance | Result | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-001 | REQ-001 | Inspection / analysis / bench / field | TBD | TBD | — | TBD | Planned |

Status is `Planned`, `Ready`, `Pass`, `Fail`, `Blocked`, or `Waived`. A pass needs
dated evidence: a measurement row, log, image, report, or reproducible command.

## Standard prototype checks

- Visual inspection: polarity, shorts, connector orientation, strain relief.
- Unpowered continuity and resistance-to-ground checks.
- Current-limited first power with expected rail voltages written down beforehand.
- Peak, idle, sleep, and shutdown current measured at the source.
- Touch/control/connector access with the enclosure assembled.
- Thermal observation in worst expected operating mode and environment.
- Fault behavior: disconnected sensor, low supply, reset, interrupted update.
- Fit check using the actual purchased part/revision, not only a vendor STEP model.

## Release summary

- Revision tested: TBD
- Hardware serial / prototype ID: TBD
- Firmware revision: TBD
- Test date and operator: TBD
- Known deviations: TBD
