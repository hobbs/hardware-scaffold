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
3. Capture source metadata in `references/sources.csv`. For every selected or
   actively evaluated part, use the `capture-datasheets` skill to archive permitted
   raw documents and write a cited `pinout-and-specs.md`.
4. Check the exact suffix/revision, ratings, logic levels, current, connector
   variant, dimensions, temperature range, lifecycle, minimum order, and stock.
5. Select a part into `parts/bom.csv` and record why. Use quantity per finished
   device; keep prototype spares in a separate field or build note.
6. Treat substitutions as design changes when pinout, voltage, firmware behavior,
   thermal behavior, geometry, certification, or connector mating can change.

## Datasheet evidence pattern

Use one evidence directory per stable part ID:

```text
references/PART-003/
  raw/
    manufacturer-document-id-rev-c.pdf
  pinout-and-specs.md
```

- `raw/` contains byte-for-byte downloads, never renamed in place when the vendor
  revises them. Use stable filenames containing a vendor document ID or product
  name and revision. Record each file's SHA-256 digest in `sources.csv`.
- `pinout-and-specs.md` is the quick reference for that exact part or module
  variant. It must identify every source by `SRC-###` and cite a page, table,
  figure, or named web section for each extracted fact.
- Pin tables must state the viewing convention and direction relative to the part.
  Include signal direction, active level, voltage domain, and fixed/shared or
  boot-sensitive behavior when the source establishes them.
- Specification tables must preserve units, conditions, and claim type (`minimum`,
  `typical`, `maximum`, `recommended`, or `measured`). Extract only facts consumed
  by a requirement, budget, interface, safety review, firmware, or mechanical
  model.
- When no downloadable manufacturer document exists, register the authoritative
  product page and extract only its stated claims. Do not fabricate a raw file or
  promote a distributor summary to a datasheet.
- Do not store a document when its license or access terms prohibit copying.
  Retain its stable URL and revision metadata, leave `local_path` and
  `file_sha256` empty, and note the restriction in both `sources.csv` and the
  extracted reference.
- Conflicts, missing variant markings, ambiguous connector views, and values not
  established by the source are explicit `UNVERIFIED` items with a resolution
  method. A downloaded document is not proof that the received unit matches it.

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
