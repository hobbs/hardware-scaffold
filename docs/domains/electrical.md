# Electrical-design playbook

## Responsibilities

- KiCad schematic: electrical intent, pins, named nets, ratings annotations, ERC.
- `electrical/breadboard-wiring.md`: temporary stack, jumper, and bench-power build
  plan for a solderless-breadboard prototype.
- WireViz: the actual detachable harness and connector/contact construction.
- `docs/interfaces.md`: the reviewed contract with mechanical and firmware work.
- Datasheets and measurements: authority for ratings and behavior.

## Schematic tool and topology gate

Before allocating pins or creating files:

1. Classify the requested artifact. A KiCad schematic owns logical connectivity;
   `electrical/breadboard-wiring.md` owns how a temporary module-stack or
   solderless-breadboard prototype is assembled; WireViz owns only a physical
   harness whose connector positions and viewing conventions are known. “Wiring
   schematic” may require both the KiCad source and a build plan, but they are not
   interchangeable.
2. Record the physical module topology before counting free pins: direct stack,
   carrier/expansion board, cable, or independent breadboard placement. A direct
   stack mates every header position even when the upper module consumes only a
   subset electrically.
3. Fix the prototype power-injection point and source-coexistence rule before signal
   wiring. `VBUS`, regulated-rail injection, USB, programmer, and battery paths are
   different designs.
4. From the workspace root, run `make kicad-toolcheck` before promising an actual
   `.kicad_sch` deliverable.

If `kicad-cli` and a compatible schematic editor are unavailable, complete all
reachable interface, net-name, evidence, and signal-name wiring work, but report
the actual schematic and ERC as blocked by that missing prerequisite. Do not
hand-author `.kicad_sch` S-expressions or add an ad hoc generator dependency merely
to compensate for a missing KiCad installation. Schematic-as-code is acceptable
only when the project deliberately selects it as its maintained workflow, pins the
generator, and validates the generated file with native KiCad.

Generate review PDFs locally from native schematic source with
`kicad-cli sch export pdf`, normally through the project's `make kicad-pdf`
target. A successful PDF export does not replace native ERC or visual inspection
in KiCad.

### Breadboard module rules

- For a direct stack, show the module as a stack in the build plan and reserve every
  electrically consumed signal before allocating pass-through header GPIO.
- Derive consumed, internally pulled, shared, and no-connect positions from the
  module schematic—not from the fact that a pad is physically present.
- Do not create a pin-numbered WireViz harness for a connector whose contact order
  or mating-face/wire-side convention is unverified. A logical signal-name mapping
  may proceed with an explicit receiving-inspection gate.
- Bench-supply instructions must name voltage, injection contact, return, initial
  current limit or resolution method, and every source that must remain
  disconnected.

## Module-based prototype workflow

1. Draw a block-level power path and budget before signal wiring.
2. Create a KiCad symbol for every module with only real exposed contacts. Include
   exact part/revision, source ID, power limits, logic level, and internally
   consumed/shared pins in fields or visible notes.
3. Use stable, descriptive net names from `electrical/net-names.md`; avoid relying
   on auto-generated labels.
4. Draw power, reset/boot, buses, interrupts, chip selects, enables, and unused-pin
   intent. Mark deliberate no-connects.
5. Run ERC, export a local review PDF with `make kicad-pdf`, explain intentional
   exceptions, and keep the report for release review.
6. For a temporary direct-stack or solderless-breadboard build, adapt
   `templates/project/electrical/breadboard-wiring.md` into
   `electrical/breadboard-wiring.md`.
7. Create a WireViz harness only for detachable, contact-numbered wiring. State
   connector view, contact numbering, wire gauge, color, length, and termination.
8. Cross-check every physical connection against `docs/interfaces.md`. Verify
   continuity before mating or first power.
9. Write a current-limited bring-up plan with expected resistance and rail values.

## Electrical review checklist

- Absolute maximum versus recommended operating values are not confused.
- Regulator and connector limits cover peak demand plus margin.
- All grounds and source-return paths are intentional.
- IO voltage, 5 V tolerance, pull-ups, level shifting, and power-off backfeeding
  have been checked.
- MCU boot-strap, flash, USB, onboard display/SD/RGB, and debug pins are not
  accidentally reused.
- Inductive loads have drivers and transient suppression; motors do not run from
  GPIO pins.
- Decoupling and bulk capacitance follow the component/module guidance.
- Connector polarity is keyed or made difficult to reverse; labels match the
  mating-face/wire-side view.
- USB, external supply, battery, and programmer power cannot fight each other.
- A schematic/ERC pass is not treated as proof of safe power design.

## When to move to a custom PCB

Wait until the module prototype has proven the use case and measured power,
interfaces, thermal behavior, and physical layout. A custom PCB is justified by
size, cost at quantity, reliability, assembly effort, signal integrity, or features
that modules cannot provide—not by tidiness alone.
