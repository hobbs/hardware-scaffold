# Mechanical and CadQuery playbook

## Opinionated toolchain

CadQuery source is the mechanical source of truth. Use STEP for assembly exchange,
STL for conventional slicing, and SVG previews for quick diffs. The recommended
interactive loop is VS Code with OCP CAD Viewer and `make cad-view`; the reproducible
noninteractive loop is `make cad-test cad`.

Direct-manipulation CAD is welcome for exploration or vendor-model cleanup, but
final fit-critical dimensions and enclosure geometry should return to named,
versioned parameters whenever practical.

## Coordinate convention

- Global units are millimetres.
- A PCB proxy defaults to its XY center at the bottom copper/board face.
- +Z points toward components. +X points toward the primary user-facing connector
  unless the component wrapper documents another orientation.
- An enclosure part is modeled in its printable/export orientation when that does
  not make the assembly transform confusing. Assembly locations are explicit.
- Every imported model gets a wrapper documenting vendor source, scaling, origin,
  orientation, and the `PART-###` it represents.

## Component proxy workflow

1. Collect the manufacturer dimension drawing and STEP model if available.
2. Model the board/body envelope, mounting points, connector bodies and insertion
   direction, control travel, tallest regions, and relevant cable/antenna/thermal
   keep-outs.
3. Do not model decorative detail or every onboard component unless it affects fit.
4. Put dimensions in a frozen dataclass or similarly obvious parameter object.
5. Add a bounding-box or position test for each critical dimension.
6. Measure the received part and record corrections in `docs/measurements.md`.

## Layout before enclosure

Build `mechanical/src/project/assembly.py` first. Place real objects in a shared
coordinate system, including fasteners and approximate cable volumes. Review:

- connector insertion/removal and cable bend radius;
- finger, tool, screw-head, nut, and driver access;
- button travel, display/viewing angle, microphones/speakers/light paths;
- antenna keep-outs and conductive/ground-plane proximity;
- battery removal/swelling allowance, strain relief, and sharp edges;
- heat paths, ventilation, and hot-surface separation;
- assembly order and whether the final connector/fastener is physically reachable.

Then build enclosure parts around the reviewed assembly.

## Fit and fabrication rules

- Define clearances by fabrication process and calibrate them with a coupon or
  first print. Do not claim universal “3D printer tolerance.”
- Keep wall, floor, fillet, boss, insert, snap, and port allowances named.
- Prefer heat-set inserts or captured nuts for frequently serviced FDM assemblies;
  document insert installation and heat risk.
- Export one printable file per part, plus an assembly STEP. Mesh tolerance should
  be fine enough for the feature and stated at release.
- First print should be a loose-fit functional draft or a small interface coupon.
  Record physical corrections before cosmetic refinement.

## Preview and review loop

```text
make cad-setup       # once; requires a supported Python (see .python-version)
make cad-view        # interactive OCP CAD Viewer session
make cad-test cad    # geometry assertions, STEP/STL exports, SVG previews
```

Open `mechanical/previews/assembly.svg` for a fast static check and inspect the
assembly STEP in a second viewer before fabrication. A clean render does not prove
manifold meshes, slicer suitability, tolerances, or access.

## Mechanical release checklist

- Actual part variants and source drawings match the model.
- All critical dimensions are parameterized and tested or measured.
- No component, cable keep-out, or fastener collides through its use/assembly path.
- Minimum walls and clearances match the chosen process and orientation.
- Printable parts have intentional orientation and do not depend on hidden support
  assumptions.
- Export names include part and revision in the release bundle.
- A real fit check is recorded before declaring the design verified.
