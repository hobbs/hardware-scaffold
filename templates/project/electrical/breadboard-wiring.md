# Breadboard wiring plan

Use this artifact only for a temporary solderless-breadboard or module-stack build.
Materialize it in a project when the physical prototype layout is being designed;
do not copy it during project initialization.

`docs/interfaces.md` remains authoritative for logical pin assignments, directions,
voltage domains, and active levels. This plan owns temporary module placement,
direct-stack orientation, jumper endpoints, jumper construction, bench-power
attachment, and the unpowered inspection sequence. A detachable, contact-numbered
harness belongs in WireViz instead.

## Build scope and revision

Record the project revision, reviewed interface revision, exact received module
variants, and the prototype behavior this assembly is intended to exercise. List
requirements and risks by stable ID rather than copying their text.

## Physical module topology

| Assembly ID | Lower/carrier module | Upper/attached module | Connection method | Alignment and viewing convention | Electrically consumed positions | Pass-through or internally unused positions |
| --- | --- | --- | --- | --- | --- | --- |

For a direct stack, identify both board ends and at least three independently
checkable contacts such as supply, return, and a distinctive signal. Do not infer
internal use from physical pad presence; cite the module schematic or pinout source.

## Jumper schedule

| Wire ID | Net | From module and silkscreen signal | To module and silkscreen signal | Color | Construction | Contact order verified? |
| --- | --- | --- | --- | --- | --- | --- |

Use signal names until the received connector's contact numbering and
mating-face/wire-side convention are verified. A jumper schedule is not authority
for a new pin assignment; discrepancies go back to `docs/interfaces.md` before the
plan changes.

## Bench power connection

| Supply setting | Initial current limit or resolution method | Injection contact | Return contact | Sources that must remain disconnected | Expected rail checks |
| --- | --- | --- | --- | --- | --- |

Name the exact input path: for example, module `VBUS`, a regulated rail, or a
connector contact. Do not write “power from bench supply” without an injection
point and source-coexistence rule.

## Unpowered inspection

Record the ordered checks for stack rotation/offset, connector signal-name matching,
ground continuity, supply-to-ground resistance behavior after capacitance settles,
and accessible rail test points. State stop conditions for unexpected continuity,
heating, odor, damage, unstable voltage, or current limiting.

## First-power sequence

Add loads incrementally. For each step, name the connected modules, current-limit
setting, expected rails, expected source current or resolution method, observations
to capture, and the power-off condition before changing wiring. Link measurements
to `docs/verification.md` when that artifact exists.
