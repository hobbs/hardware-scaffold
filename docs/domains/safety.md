# Safety playbook

This scaffold defaults to low-voltage, current-limited module prototypes. Safety is
a design input and a verification obligation, not a disclaimer added at the end.

## Escalate and pause release when

- lithium or other rechargeable-cell chemistry, protection, charging profile,
  thermal sensing, cell provenance, or enclosure suitability is unknown;
- mains voltage or energy can be touched, bridged, overheated, or inadequately
  isolated;
- a source can deliver enough current to cause fire, burns, arcing, or wiring
  damage without coordinated fuse/current limiting;
- motion, pressure, heat, laser/UV, chemicals, RF exposure, or sharp mechanisms can
  harm people or property;
- a single software fault can defeat the only protective function;
- required standards, legal constraints, or competent review are not understood.

Record a `RISK-###`, identify the necessary qualified review or authoritative
guidance, and prevent fabrication/release instructions from presenting the design
as verified.

## Batteries and charging

- Prefer protected, reputable cells/packs and a charger/power-path solution made
  for the exact chemistry, series count, capacity range, and load topology.
- Verify charge voltage/current, temperature requirements, undervoltage/overcurrent
  protection, load sharing, reverse current, USB/external-source coexistence, wire
  and connector ratings, and physical protection.
- Do not solder directly to cells unless the cell and process explicitly support it
  and the builder is equipped/qualified.
- Account for swelling, puncture/abrasion, crush, heat, service, transport, and a
  failure path that does not trap pressure or direct flame toward the user.
- Bench-test charging and discharge temperatures/current with containment and a
  documented stop condition. An AI-created circuit or generic module name is not a
  safety validation.

## Mains and high energy

Use certified enclosed supplies whenever possible. Creepage, clearance, insulation,
earthing, fusing, enclosure flammability, strain relief, and accessible-part rules
depend on voltage, pollution, materials, installation, and jurisdiction; seek a
qualified review. Do not prototype exposed mains on a solderless breadboard.

## Safety evidence

For each hazard, record severity, exposure, preventive controls, protective
controls, test method, residual risk, and who accepted it. Tests should include
credible single faults; “works normally” is insufficient.
