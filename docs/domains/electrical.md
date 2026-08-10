# Electrical-design playbook

## Responsibilities

- KiCad schematic: electrical intent, pins, named nets, ratings annotations, ERC.
- WireViz: the actual harness and connector/contact construction.
- `docs/interfaces.md`: the reviewed contract with mechanical and firmware work.
- Datasheets and measurements: authority for ratings and behavior.

## Module-based prototype workflow

1. Draw a block-level power path and budget before signal wiring.
2. Create a KiCad symbol for every module with only real exposed contacts. Include
   exact part/revision, source ID, power limits, logic level, and internally
   consumed/shared pins in fields or visible notes.
3. Use stable, descriptive net names from `electrical/net-names.md`; avoid relying
   on auto-generated labels.
4. Draw power, reset/boot, buses, interrupts, chip selects, enables, and unused-pin
   intent. Mark deliberate no-connects.
5. Run ERC, explain intentional exceptions, and keep the report for release review.
6. Create a WireViz harness from the reviewed schematic. State connector view,
   contact numbering, wire gauge, color, length, and termination.
7. Cross-check every detachable connector end-to-end against
   `docs/interfaces.md`. Verify continuity on the physical harness before mating.
8. Write a current-limited bring-up plan with expected resistance and rail values.

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
