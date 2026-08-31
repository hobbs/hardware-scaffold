---
name: capture-datasheets
description: Archive authoritative raw hardware documents and extract cited pinouts and design-relevant specifications for project parts. Use when adding or refreshing datasheets, schematics, pin maps, protocol references, or source-backed part notes.
---

# Capture datasheet evidence

Create or update evidence for real `PART-###` records under one hardware project.
This skill handles source preservation and extraction; it does not select a part by
familiarity or turn an unreviewed candidate into `Selected`.

## Ground the part

1. Read the project's `project.toml`, brief, system design, BOM or alternates, and
   existing source register. Read `docs/domains/parts-and-sourcing.md` from the
   workspace root.
2. Establish the exact manufacturer, manufacturer part number, suffix, module or
   board revision, and connector variant. If markings on the received unit have not
   been checked, keep the identity or affected claims `UNVERIFIED` and state the
   inspection needed.
3. Use datasheets and drawings from the manufacturer first. A module also needs its
   module schematic or hardware manual when the underlying IC datasheet does not
   describe board pins, regulators, translators, connectors, or shared signals.
4. Treat distributor tables and product-page prose as secondary. When no formal
   datasheet exists, use the manufacturer's product page without calling it a
   datasheet.

## Preserve raw evidence

Use this layout only after real evidence exists:

```text
references/PART-###/
  raw/
    manufacturer-document-id-revision.pdf
  pinout-and-specs.md
```

For each source:

- register a stable `SRC-###` row in `references/sources.csv` with title,
  organization, document revision or publication date, canonical URL, access date,
  authority, and notes;
- inspect document copyright, license, and access terms before copying it into the
  project. If copying is not permitted, keep only the URL and extracted citations;
- preserve downloaded bytes unchanged. Use a descriptive revision-bearing filename
  and never replace a different revision at the same path;
- compute SHA-256 for every local raw file and record it in `file_sha256`; leave
  both `local_path` and `file_sha256` empty for URL-only sources;
- reject login interstitials, HTML error pages, zero-byte responses, and files whose
  type does not match the expected document before treating a download as evidence.

One source row represents one document or versioned web page, not an entire vendor.
Keep older revisions when they still explain hardware already received.

## Extract the quick reference

Write `pinout-and-specs.md` for the exact `PART-###`. Use these sections when they
contain real information:

1. **Identity and applicability** — purchasable variant, board/panel revision,
   observed markings, and whether applicability is verified.
2. **Source map** — `SRC-###`, title/revision, local raw link when present, and the
   scope each source establishes.
3. **Pinout** — connector or package viewing convention followed by a table with
   pin/contact, signal, direction relative to the part, active level, voltage
   domain, function, constraints, and source locator.
4. **Design specifications** — parameter, value and units, minimum/typical/maximum
   or recommended status, operating conditions, source locator, and the consuming
   `REQ-###`, `INT-###`, budget, risk, firmware behavior, or mechanical parameter.
5. **Protocol and sequencing** — only startup, shutdown, timing, bus mode, message,
   or state details the design consumes.
6. **Unverified items and conflicts** — each missing or contradictory fact plus a
   concrete resolution method.

Citations use `SRC-###, p. N, Table X`, `SRC-###, Figure X`, or an exact web section
name. Never cite a PDF generally when a page or table exists. Preserve source units
in the extracted value; add an SI conversion only as a clearly labeled derived
value. Never collapse absolute maximum ratings into recommended operating values.

The extracted note is a review aid, not a new independent source. Downstream
artifacts cite its `SRC-###` evidence instead of copying uncited values.

## Propagate and verify

- If extraction changes a cross-domain pin, rail, level, connector, timing, or
  physical contract, update `docs/interfaces.md` first, then every consuming
  schematic, harness, firmware pin map, budget, and mechanical model.
- Keep part state honest: downloaded evidence does not prove compatibility,
  receipt, measurement, or verification.
- From the workspace root run:

```text
make check-project PROJECT=projects/<slug>
```

Inspect every local raw path and SHA-256 result reported by the checker. Report
URL-only sources, license-limited documents, remaining `UNVERIFIED` claims, and the
exact verification command.
