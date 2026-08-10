# System-design playbook

## Goal

Turn a conversational idea into reviewable requirements and a block architecture
without prematurely locking parts or geometry.

## Workflow

1. Write the smallest concrete use scenario in `docs/project-brief.md`.
2. Convert needs into measurable `REQ-###` statements. Separate `Must` from
   attractive extras.
3. Declare non-goals and constraints: environment, size, power, fabrication,
   maintenance, budget, and schedule.
4. Draw system blocks by responsibility, not by favorite part number.
5. Draw the complete power path, including charging, protection, switching,
   conversion, source coexistence, and off-state loads.
6. Draft cross-domain `INT-###` contracts and a first power budget.
7. Record risks, open questions, and costly-to-reverse choices.
8. Only then evaluate purchasable parts.

## Quality bar

- Requirements describe observable behavior and include acceptance criteria.
- The architecture shows every energy source and load.
- Peak demand, typical duty cycle, losses, and margin are distinct values.
- Unknowns say how they will be resolved.
- The first prototype is intentionally smaller than the eventual product where
  possible: USB power before batteries, bench wiring before custom PCB, loose-fit
  enclosure before cosmetic finish.

## Common traps

- Treating a development board as a single magical block without its internal pin
  sharing, regulator limits, antenna, storage, or display connections.
- Estimating runtime from battery label capacity and average MCU current alone.
- Choosing display, battery, and enclosure independently, then discovering their
  physical or power constraints conflict.
- Writing “works reliably” instead of a testable failure/recovery requirement.
