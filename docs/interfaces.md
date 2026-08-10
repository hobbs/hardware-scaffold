# Interface control table

This is the reviewed contract between electrical, mechanical, and firmware work.
The schematic remains authoritative for nets, WireViz for physical wires, CadQuery
for location/access, and firmware for executable pin configuration.

## Electrical and data interfaces

| ID | From → to | Signal / rail | End A pin | End B pin | Levels / protocol | Connector / orientation | Firmware name | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INT-001 | TBD → TBD | TBD | TBD | TBD | TBD | TBD | TBD | Proposed | SRC-### |

Status is `Proposed`, `Reviewed`, `Bench verified`, or `Released`.

Explicitly document:

- connector view (mating face, wire side, or PCB top);
- pin 1 mark and polarity;
- IO voltage and whether a pin is 5 V tolerant;
- pull-up location/value, boot-strap behavior, and internally shared pins;
- nominal and worst-case current on power contacts;
- detachable versus permanently wired connections.

## Mechanical interfaces

| ID | Objects | Datum / origin | Mating or clearance requirement | Target (mm) | Tolerance (mm) | Verification |
| --- | --- | --- | --- | ---: | ---: | --- |
| INT-101 | TBD | TBD | TBD | TBD | TBD | TEST-### |

## Thermal, RF, optical, and acoustic interfaces

| ID | Source / receiver | Keep-out or path | Requirement | Verification |
| --- | --- | --- | --- | --- |
| INT-201 | TBD | TBD | TBD | TEST-### |

## Change rule

A changed connector, pin, board revision, origin, envelope, or access requirement
is an interface change. Update this table first, then the affected sources, tests,
and assembly instructions in the same change.
