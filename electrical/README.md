# Electrical design

Put the KiCad project in `kicad/`, the physical harness definition in
`wiring/harness.yml`, and generated reports in `reports/`. Read
`docs/domains/electrical.md` before creating symbols or connections.

Recommended progression:

1. Block and power-path diagram in `docs/system-design.md`.
2. Interface proposals in `docs/interfaces.md`.
3. KiCad module symbols and schematic.
4. ERC and manual rating/pin-sharing review.
5. WireViz harness generated from the reviewed net list.
6. Unpowered continuity check and current-limited first power.

Name the primary schematic `electrical/kicad/project.kicad_sch` so the default Make
target works, or override it: `make kicad-erc KICAD_SCH=path/to/file.kicad_sch`.
