# KiCad project

Create the main schematic as `project.kicad_sch` and keep custom module symbols in
the project-local library. Use exact `PART-###` values in symbol fields and include
source/revision notes for custom pin maps.

## Tool gate

From the workspace root, run `make kicad-toolcheck` before creating the schematic.
Use a native KiCad-compatible editor for `.kicad_sch` source and native
`kicad-cli sch erc` for ERC. If KiCad is unavailable, keep progressing the reviewed
interface contract, net registry, and signal-name wiring plan, but do not fabricate
the schematic through hand-written S-expressions or a one-off generator.

KiCanvas can open an existing `project.kicad_sch` with **Open from local** for
read-only visual review. Loading successfully in KiCanvas is not ERC.

Schematic-as-code is a project-level workflow decision, not an automatic fallback.
If selected, pin the generator dependency, commit the maintained generator source,
and validate its output with native KiCad.

Before the first schematic:

- Set project text variables for title and hardware revision.
- Add page-level notes for supply ranges and connector-view conventions.
- Decide whether a module's internal peripherals are shown as hidden/reserved pins
  or explicit notes; do not imply those pins are free.
- Configure ERC intentionally. Waivers need a visible reason, not blanket excludes.

When the schematic first exists, adapt the relevant `kicad-toolcheck` and
`kicad-erc` targets from `templates/project/Makefile` into the project's own build
command; do not copy unrelated stage targets. Run `make kicad-erc` after edits.
Inspect both the report and the schematic visually; ERC does not validate ratings,
power-path behavior, connector orientation, or physical stack alignment.
