# KiCad project

Create the main schematic as `project.kicad_sch` and keep custom module symbols in
the project-local library. Use exact `PART-###` values in symbol fields and include
source/revision notes for custom pin maps.

Before the first schematic:

- Set project text variables for title and hardware revision.
- Add page-level notes for supply ranges and connector-view conventions.
- Decide whether a module's internal peripherals are shown as hidden/reserved pins
  or explicit notes; do not imply those pins are free.
- Configure ERC intentionally. Waivers need a visible reason, not blanket excludes.

Run `make kicad-erc` after edits. Inspect both the report and the schematic
visually; ERC does not validate ratings, power-path behavior, or connector
orientation.
