# Mechanical and CadQuery playbook

## Opinionated toolchain

CadQuery source is the mechanical source of truth. Use STEP for assembly exchange,
STL for conventional slicing, and SVG previews for quick diffs. The reproducible
noninteractive loop is `make cad-test cad`; VS Code with OCP CAD Viewer or its
standalone browser viewer is an optional interactive aid, not a build prerequisite.

Direct-manipulation CAD is welcome for exploration or vendor-model cleanup, but
final fit-critical dimensions and enclosure geometry should return to named,
versioned parameters whenever practical.

## Start CAD at the current project stage

Use `templates/project/` as a reference, not a tree to copy. When layout work starts:

1. Add the real part parameters/proxies and `mechanical/src/project/assembly.py`;
   add enclosure geometry only around that layout. Replace the generic reference
   board rather than resizing its example enclosure.
2. Adapt `mechanical/build.py`, `view.py` if wanted, and only relevant geometry
   tests to those real objects. Keep generated `exports/` and `previews/` ignored.
3. Merge the template's Python packaging/test configuration and `cad-*` Make
   targets into existing project files; add `.python-version` if absent. Preserve
   unrelated configuration. Keep the existing Python 3.12, CadQuery 2.8.0 and
   optional ocp-vscode 2.9.0 conventions.
4. Link dimension evidence and current readiness in the project's existing
   measurements/verification records. Do not materialize unrelated electrical,
   firmware, or production artifacts just to begin CAD.

A dry-use UX prototype may use hand-soldered carriers, generous adjustable mounts,
and removable covers. Weatherproofing, production tooling, and custom PCBs are
separate scope decisions, not prerequisites for evaluating grip and controls.

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

1. Use manufacturer drawings/models first, checking the exact `PART-###`, board
   revision, and connector/assembly variant. Cite the source and page, figure, or
   drawing locator beside fit-critical values.
2. Distinguish **vendor nominal dimensions**, **received-part measurements**,
   **design allowances**, and **unresolved dimensions**. Name allowances such as
   print clearance, finger access, cable bend space, and battery removal space;
   they are design choices, not measured hardware dimensions.
3. Model the board/body envelope, mounting points, connector bodies and insertion
   direction, control travel, tallest regions, and relevant cable/antenna/thermal
   keep-outs. Skip detail that does not affect fit.
4. Put values in a frozen dataclass or similarly obvious parameter object. For
   an unresolved value, label any working envelope as provisional, state its
   assumption/range, and identify the fit decision it blocks.
5. Request calipers only for dimensions not resolved by applicable manufacturer
   evidence: for example, soldered header height, underside solder protrusion,
   hand-built carrier stack, actual cable exit, or a supplied battery's assembled
   lead/connector envelope. Specify the datum and measurement direction. Do not
   ask the user to remeasure an entire documented board.
6. Record received-part corrections, method, uncertainty, and build/variant in
   `docs/measurements.md`. Escalate a mismatch rather than silently replacing
   the drawing's nominal value.

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

Then build enclosure parts around the reviewed assembly. Classify review objects
as manufactured solids, physical reference parts, or clearance/keep-out volumes.
A keep-out may intentionally overlap its owner or another keep-out; that is not
a physical collision. Check it against the specific forbidden bodies/materials
and motion path it represents. Document intended contact such as a board resting
on a standoff; do not exempt an entire pair from all interference checks.

For socketed module carriers, review the complete retention load path through the
board underside. A tie that appears to retain a stack may clamp solder tails;
model insulating guards, their board-bearing lands, wire exits and buckle space
before tightening it. Check the whole flexible loop and locked head, not just two
anchor holes. Orient a strain-relief loop across its cable, not along it.

Use one coordinate authority for hand-cut carrier outlines and a separate
signal/pad schedule for connectivity. Generate top and explicitly mirrored
underside build views from those inputs, and reject coordinate disagreement.
Sourced socket height, insertion range, soldering suitability and cable bend
requirements can change the layout; resolve those before calling a carrier
buildable. Preserve rejected candidates and their reasons without retaining them
as active build instructions.

## Fit and fabrication rules

- Define clearances by fabrication process and calibrate them with a coupon or
  first print. Do not claim universal “3D printer tolerance.”
- Keep wall, floor, fillet, boss, insert, snap, and port allowances named.
- Choose assembly order and fastening appropriate to the prototype. Inserts or
  captured nuts can help repeated service, but are not mandatory for a UX mockup;
  if used, document installation access and heat risk.
- Choose each part's print orientation before detailed fastening/overhang design.
  State bed face, critical layer direction, and expected supports; distinguish its
  printable coordinates from its assembly transform.
- Print a small coupon for the riskiest interface first (for example a button
  guide, connector aperture, lid joint, or board mount), using the intended
  material, orientation, and slicer settings. Record the fit correction before
  committing to full fabrication; a loose-fit draft can follow for hand feel.
- Export only manufactured parts as printable files, plus an assembly STEP for
  review. Never send reference boards or keep-outs to the slicer as enclosure
  material. State mesh tolerance at release.

## Checks that exercise geometry

Bounding-box checks help catch a wrong proxy scale, but parameter arithmetic alone
does not prove a part fits. The starter tests check envelopes and assembled
board/lid interference; they are examples, not complete enclosure acceptance
evidence. For the real layout, check the generated solids in assembled coordinates:

- valid solids and unintended physical intersection volume, using a stated
  numerical tolerance and identifying intended contacts;
- residual wall, floor, and boss material at cuts and holes, not just the named
  thickness parameter;
- connector/button/display apertures through the actual wall or cover, including
  alignment, button travel and a clear viewing path;
- positive retention, not just noninterference: complete supported head-bearing
  material, restraint against lift/slide, usable thread engagement, recessed tips
  and nut antirotation where required. A plate resting on ledges is not retained;
- plug, finger, driver, fastener and cable clearance along insertion, operation,
  assembly, and removal paths, not only at the final resting position.

Keep regression assertions for plausible geometry failures, not echoes of the
dataclass. Analytic clearance volumes and sections can support review; they do
not establish cable stiffness, tactile feel, print quality, or physical access.

Give service checks their actual assembly state. A driver path requiring lid
removal may intersect the closed lid, but must still clear every other forbidden
body and cable reservation. Check nut insertion and removal continuously, not only
at their final positions. Use a counterfactual missing ear or blocked pocket to
confirm a retention regression would detect the corresponding design mistake.

## Preview and review loop

From the project root, check the supported interpreter before installing anything:

```sh
python3.12 -c "import sys; assert sys.version_info[:2] == (3, 12), sys.version; print(sys.executable)"
make cad-setup PYTHON=python3.12
make cad-test cad
```

If `python3.12` is missing, install Python 3.12 through the local Python manager,
or use the full path to an existing 3.12 interpreter for both the check and
`PYTHON=...`. Do not substitute the system `python3` blindly: it may be 3.14,
while the template requires `>=3.12,<3.13`. If `.venv` already exists, first run
`.venv/bin/python --version`; if it is not 3.12, preserve anything needed from it
and deliberately recreate it with the supported interpreter. The template
`cad-setup` checks executable availability, not the selected interpreter version.

`make cad-setup` installs the template's viewer extra too, but exports/tests do
not require the VS Code extension or a running viewer. For interactive review,
open the OCP CAD Viewer pane in VS Code, then run `make cad-view`.

Without VS Code, the same installed viewer supports a local browser. In one
terminal, keep this command running (substitute the selected CAD interpreter):

```sh
.venv/bin/python -m ocp_vscode --host 127.0.0.1 --port 3939 --tree_width 280
```

Open `http://127.0.0.1:3939/viewer`, then run `make cad-view` in another terminal.
Open the browser **before** sending geometry; resend after opening or refreshing
the viewer. A project may expose the server command as `make cad-server`.
Port 3939 must not already be occupied by another viewer.

The explicit tree width is required for the tested ocp-vscode 2.9.0 standalone
launch: omitting it generated `JSON.parse("None")` and a blank page. `/` is the
API endpoint, not the viewer page. Use `Camera.RESET` from `ocp_vscode.config`
instead of the deprecated boolean reset argument.

Review assembled and exploded views plus section or orthographic views through
fit-critical areas. Keep physical references and keep-outs separately named and
distinguishable by color/transparency or separate annotated views. Include
orientation/datums so an exploded gap is not mistaken for assembled clearance.
The starter `previews/assembly.svg` is an exploded monochrome overview without
keep-outs, not this complete review set; `exports/review-assembly.step` contains
the assembled named objects and connector keep-out.
Generate an explicit background rectangle for monochrome SVGs; transparent black
edges can disappear on dark review surfaces. Inspect a rasterized preview instead
of assuming a successfully written SVG is legible.

Inspect the assembly STEP in a CAD viewer and manufactured meshes in the slicer
before fabrication. Preserve reproducible exports even if the optional viewer is
unavailable. Record exactly which views/checks were inspected; source-only review
cannot claim fit, printability, electrical/battery safety, or a physical trial.

## Readiness gates

Record the current gate, evidence, and unresolved blockers; do not call every
successful render “verified.”

| Gate | Evidence and limits |
| --- | --- |
| Dry UX concept | Layout and review views support intended grip, controls, display, and access; provisional dimensions are explicit. Claim hand-feel or usability results only after the corresponding physical trial. No fit or environmental claim. |
| Fit-ready for trial fabrication | Exact variants and fit-critical dimensions are resolved; geometry/access checks and print orientation are reviewed; the first interface coupon is specified. This authorizes a trial print, not a claim that received hardware fits. |
| Field-tested | A real assembled build has recorded fit and powered functional checks, then a trial in stated conditions with results and limitations. A dry trial does not establish weatherproofing, durability, or production readiness. |

Battery/charging safety remains a separate electrical verification gate. Correct
connector polarity or a mechanically fitting battery alone cannot approve it.

## Mechanical release checklist

- Actual part variants and source drawings match the model; unresolved dimensions
  and allowances are visible, not disguised as manufacturer facts.
- Critical geometry checks cover collisions, wall/cut integrity, apertures and
  assembly/service paths, with physical references distinguished from keep-outs.
- Minimum walls and clearances match the chosen process and orientation.
- Printable parts have intentional orientation and explicit support assumptions;
  the coupon and subsequent physical fit results are recorded.
- Export names include part and revision in a release bundle.
- The stated readiness gate matches observed evidence. Real fit and use checks,
  not source review or a clean render, support any claim of verification.
