# Harness

`harness.yml` is a valid minimal WireViz starter. Replace the example connector
names and pins from the reviewed KiCad schematic and `docs/interfaces.md`.

WireViz connector pin numbers describe physical contact positions, not MCU GPIO
numbers unless those happen to be identical. State whether diagrams show mating
face or wire side and verify the physical harness with continuity tests.

Run `make wiring-setup` once, then `make wiring-check` for a dependency-light parse
and BOM generation. `make wiring` renders HTML/PNG/SVG/TSV and also requires the
Graphviz `dot` executable. Generated files go to `out/`.
