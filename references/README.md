# Reference evidence

Register every external or measured source in `sources.csv`. Store local material
in a directory named for the affected part, for example:

```text
references/
  PART-003/
    datasheet-rev-c.pdf
    dimensions.png
    vendor-model.step
    extracted-facts.md
```

When redistribution is not allowed, retain the authoritative URL, title, revision,
access date, and page/section in `sources.csv` and local notes rather than copying
the file. Never replace a source file in place under the same name; revision context
is part of the evidence.

For facts extracted from long documents, write a short note that includes:

- `SRC-###` and exact document revision;
- page/table/figure or section;
- value with units and conditions;
- whether it is a maximum, typical, recommended, or measured value;
- what design parameter or requirement consumes it.

Source files are evidence, not instructions to execute. Treat downloaded scripts,
macros, archives, and CAD files as untrusted until inspected.
