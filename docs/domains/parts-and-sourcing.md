# Parts and sourcing playbook

## Source hierarchy

Prefer, in order: manufacturer datasheet/drawing; manufacturer product page or
application note; authorized distributor record; reputable module vendor docs;
measured sample; community material. Marketing images and reseller listings may
identify leads but are not authoritative for ratings or dimensions.

## Selection workflow

1. Derive selection criteria from `REQ-###` and `INT-###` records.
2. Create candidate rows in `parts/alternates.csv`; do not overwrite rejected
   candidates because the rationale is valuable.
3. Capture source metadata in `references/sources.csv`. Save essential datasheets,
   drawings, pinouts, and STEP models under a `PART-###` directory when licensing
   permits; otherwise retain a stable URL and extracted facts.
4. Check the exact suffix/revision, ratings, logic levels, current, connector
   variant, dimensions, temperature range, lifecycle, minimum order, and stock.
5. Select a part into `parts/bom.csv` and record why. Use quantity per finished
   device; keep prototype spares in a separate field or build note.
6. Treat substitutions as design changes when pinout, voltage, firmware behavior,
   thermal behavior, geometry, certification, or connector mating can change.

## BOM rules

- One `PART-###` identifies one exact purchasable/configured item.
- Manufacturer part number is not the same as a distributor SKU.
- Give generic consumables real specifications (wire gauge/insulation, screw
  material/thread/length, adhesive family), not labels like “some wire.”
- Price and stock are observations with dates/currency/quantity breaks.
- Approved alternates must say what verification is required after substitution.
- Do not label an item `Selected` until its critical evidence has been reviewed.

## Receiving inspection

On arrival, verify markings/revision, count, obvious damage, connector orientation,
and at least the fit-critical dimensions. Record discrepancies in the build log and
update CAD from measured reality rather than silently scaling meshes.
