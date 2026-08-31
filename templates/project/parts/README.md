# Parts and BOM

`bom.csv` is the purchasing source of truth for the selected revision.
`alternates.csv` records evaluated candidates and substitution constraints. Follow
`docs/domains/parts-and-sourcing.md`.

Use semicolon-separated IDs within a CSV cell, such as `SRC-001;SRC-004`. Do not
put line breaks inside cells. Add prototype-only tools and consumables only when
they must travel with the reproducible build; otherwise list them in assembly docs.
