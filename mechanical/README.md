# CadQuery mechanical design

This starter models a generic reference board, a base, a lid, connector clearance,
and a review assembly. Replace the proxy with real `PART-###` components; do not
scale the finished enclosure around the example.

## Structure

```text
mechanical/
  src/project/
    parameters.py             Named project dimensions
    components/               One module per real physical object
    assembly.py               Shared-coordinate-system layout
    enclosure.py              Manufactured enclosure parts
  tests/                      Fit- and fabrication-critical assertions
  build.py                    Deterministic STEP/STL/SVG export
  view.py                     OCP CAD Viewer interactive loop
  exports/                    Generated, ignored
  previews/                   Generated, ignored
```

## First use

Install a Python compatible with `.python-version`, then:

```sh
make cad-setup
make cad-test cad
```

For interactive work, install the OCP CAD Viewer extension in VS Code, open its
viewer pane, and run `make cad-view`. The script sends separately named parts and
keep-outs so collisions and access are easier to review than in a single fused
body.

Generated outputs:

- `exports/enclosure-base.step` and `.stl`
- `exports/enclosure-lid.step` and `.stl`
- `exports/reference-board.step`
- `exports/review-assembly.step`
- `previews/assembly.svg`, `base.svg`, and `lid.svg`

## Replacing the starter

1. Give every physical component a `PART-###` and reviewed drawing/source.
2. Replace `reference_board.py` with named proxy modules using the coordinate
   convention in `docs/domains/mechanical.md`.
3. Put fit-affecting values in `parameters.py`; preserve meaningful source comments.
4. Lay out all components, fasteners, and cable/connector keep-outs in
   `assembly.py` before changing enclosure form.
5. Add tests for envelope, hole locations, clearances, wall/boss thickness, and
   port/access alignment.
6. Make a loose-fit print or interface coupon and record corrections under
   `docs/measurements.md`.
