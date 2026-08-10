# Hardware project agent guide

This repository is a reproducible engineering notebook and build source, not just
a codebase. Help the user move from an idea to a device that can be assembled,
tested, revised, and understood later.

## On the first conversation

1. Read `project.toml`, `docs/project-brief.md`, `docs/open-questions.md`, and the
   current git status.
2. Summarize the proposed device in one sentence and identify the few unknowns
   that could change its architecture: power source, environment, physical scale,
   critical inputs/outputs, fabrication method, and budget.
3. Make conservative, reversible assumptions for ordinary unknowns and record
   them. Ask the user only about decisions whose alternatives materially diverge.
4. Update the brief before producing a shopping list or detailed geometry.
5. Work from requirements to blocks to interfaces to parts. Do not select a part
   merely because it is familiar.

## Read the relevant playbook

| When the task involves… | Read before editing |
| --- | --- |
| Scope, requirements, architecture, tradeoffs | `docs/domains/system-design.md` |
| Part selection, sourcing, cost, or BOMs | `docs/domains/parts-and-sourcing.md` |
| Schematics, power, wiring, connectors, or PCBs | `docs/domains/electrical.md` |
| Enclosures, component layout, CAD, printing, or fasteners | `docs/domains/mechanical.md` |
| Embedded code, simulation, pin maps, or hardware tests | `docs/domains/firmware.md` |
| Batteries, charging, mains, heat, motion, pressure, lasers, or other hazards | `docs/domains/safety.md` |
| Prototype builds, measurements, or release readiness | `docs/domains/verification.md` |

Read multiple playbooks when a change crosses boundaries. Update
`docs/interfaces.md` first when the change affects another domain.

## Engineering rules

- **Never invent a specification.** Record its source ID from
  `references/sources.csv`, or mark it `TBD`/`UNVERIFIED` and explain how it will
  be resolved.
- **Datasheets outrank distributor tables; measurements outrank assumptions** for
  the actual unit under test. Preserve revision/date context.
- **Use stable identifiers:** `REQ-###`, `ASM-###`, `INT-###`, `PART-###`,
  `SRC-###`, `RISK-###`, `TEST-###`, `DEC-###`, `Q-###`, and `PROTO-###`.
  Reference them across artifacts.
- **Keep one owner per fact.** Link to the authoritative artifact instead of
  copying values into multiple files. Derived values should name their inputs.
- **Separate design states:** proposed, selected, ordered, received, measured, and
  verified are not synonyms.
- **Use SI units in calculations.** Mechanical source uses millimetres. State units
  in column names, parameters, diagrams, and measurements.
- **Prefer text, parameters, and generated outputs.** Do not hand-edit generated
  STEP/STL/SVG, WireViz diagrams, KiCad reports, or firmware build products.
- **Keep changes buildable.** When source changes, regenerate or test the relevant
  artifact when the toolchain is available and report what was not run.

## Required design sequence

1. **Frame:** brief, non-goals, constraints, assumptions, and acceptance criteria.
2. **Architect:** block diagram, power path, interfaces, failure concerns, and
   rough budgets.
3. **Select:** evidence-backed components and alternates; capture models, drawings,
   pinouts, ratings, and lifecycle/availability.
4. **Prototype:** schematic plus wiring plan, firmware proof, mechanical proxies,
   and bench measurements.
5. **Integrate:** shared interface table, full mechanical assembly, service and
   cable access, thermal/antenna keep-outs, and assembly order.
6. **Verify:** trace requirements and risks to tests; record results and deviations.
7. **Release:** freeze sources, BOM, fabrication exports, wiring diagram, firmware,
   assembly instructions, and known limitations under a revision tag.

Do not skip directly from idea to enclosure. Component geometry is meaningful only
after the real part/revision and connector access requirements are known.

## Domain boundaries

- CadQuery owns physical envelopes, origins, locations, keep-outs, openings,
  clearances, and manufactured geometry. It does not own net connectivity.
- KiCad owns logical connectivity, component pins, named nets, and ERC. It does
  not specify wire length, color, routing, or prove electrical safety.
- WireViz owns the buildable harness: connector sides, contact positions, wire
  color/gauge/length, and splice/crimp details.
- Firmware owns executable pin configuration. The interface table is the reviewed
  cross-domain contract and must agree with both firmware and the schematic.
- The BOM owns purchasing identity and quantity. CAD and schematics should refer
  to `PART-###`, not duplicate vendor/order facts.

## CadQuery conventions

- Use named parameters; no unexplained dimensions inside feature-building code.
- Put each physical component in `mechanical/src/project/components/` and keep its
  origin documented. Default: PCB XY center at its bottom face; +Z points toward
  components; +X points toward the primary user-facing connector.
- Model fit-critical geometry, not cosmetic board detail: overall envelope,
  mounting holes, connectors, controls, tallest regions, antenna/thermal/cable
  keep-outs, and tool access.
- Imported STEP is reference geometry. Wrap it in a component module that defines
  the same origin and exposes simplified keep-outs.
- Keep parts separate in an assembly. Export printable parts individually and an
  assembly STEP for review.
- Add geometry tests for critical wall thickness, envelope, hole spacing, port
  access, and intentional clearances.
- Use the workflow in `docs/domains/mechanical.md`; commit source and reviewable
  intent, not a pile of generated meshes.

## Review gates

A module-based prototype is ready to build only when:

- Each selected part has a `PART-###`, source evidence, and exact revision/variant.
- Supply rails have voltage tolerances and worst-case/current estimates.
- Logic levels, pull-ups, shared pins, boot straps, and internally consumed pins
  are reviewed.
- KiCad schematic and WireViz pin positions agree with `docs/interfaces.md`.
- Connector polarity and connector-view orientation are explicit.
- CAD includes connector insertion space, cable bend space, controls, fasteners,
  and relevant keep-outs.
- A bring-up plan gives current-limited first-power steps and expected readings.

A design revision is complete only when `make check-strict` passes and every
claimed verification has evidence in `docs/verification.md`.

## Safety stop conditions

Do not normalize or silently fill gaps in hazardous designs. Pause design release
and surface the risk when battery chemistry/protection is unknown, mains isolation
is unclear, a component may exceed a rating, polarity is ambiguous, temperature or
pressure lacks containment, a mechanism can injure, or a safety function depends
only on unverified software. Follow `docs/domains/safety.md`.

## Routine checks

Run `make check` after document/table edits. For mechanical changes, run
`make cad-test cad`; for harness changes, run `make wiring`; for KiCad changes, run
`make kicad-erc`. If a dependency is unavailable, leave the source coherent and
state the exact skipped command.
