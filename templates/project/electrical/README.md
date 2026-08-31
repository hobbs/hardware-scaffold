# Electrical design

Put the KiCad project in `kicad/`, the physical harness definition in
`wiring/harness.yml`, and generated reports in `reports/`. Read
`docs/domains/electrical.md` before creating symbols or connections.

Recommended progression:

1. Block and power-path diagram in `docs/system-design.md`.
2. Interface proposals in `docs/interfaces.md`.
3. KiCad module symbols and schematic.
4. ERC and manual rating/pin-sharing review.
5. `breadboard-wiring.md` for temporary module stacks and solderless jumpers, or a
   WireViz harness for detachable contact-numbered wiring.
6. Unpowered continuity check and current-limited first power.

Name the primary schematic `electrical/kicad/project.kicad_sch`. Before authoring
it, run `make kicad-toolcheck` from the workspace root. A newly initialized project
does not contain a Makefile; when the schematic becomes real, adapt only the
`kicad-toolcheck` and `kicad-erc` targets from `templates/project/Makefile` into the
project's own build command. Then run `make kicad-erc`, or override
`KICAD_SCH=path/to/file.kicad_sch`.
