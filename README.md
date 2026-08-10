# Hardware Project Scaffold

An opinionated, chat-first starter for small devices built from development boards,
modules, wiring, firmware, and fabricated enclosures. Clone it, open an AI coding
agent, and describe the device you want to make.

The scaffold treats a device as linked but distinct designs:

- **System:** requirements, architecture, interfaces, risks, and verification.
- **Electrical:** authoritative connectivity in KiCad and buildable harnesses in
  WireViz.
- **Mechanical:** parametric component placement and enclosures in CadQuery.
- **Firmware:** behavior, pin assignments, builds, and hardware-in-the-loop tests.
- **Evidence:** part sources, datasheets, calculations, and bench measurements.

## Start a project

1. Clone this repository for the new project.
2. Open Codex or Claude in the repository and say what you want to build. A useful
   first message is:

   > Help me turn this scaffold into a desk air-quality monitor. Start with the
   > project brief. Ask only for decisions that materially change the architecture;
   > record other unknowns as assumptions or open questions.

3. The agent should update [project.toml](project.toml), then work through
   [the project brief](docs/project-brief.md) and
   [the system design](docs/system-design.md) before selecting parts or drawing an
   enclosure.
4. Run `make check` frequently. Run `make check-strict` before calling a design
   revision complete.

`AGENTS.md` is the operating manual for coding agents. `CLAUDE.md` imports it so
both tools follow the same process.

## Source-of-truth map

| Fact | Authoritative artifact |
| --- | --- |
| User need, constraint, acceptance criterion | `docs/project-brief.md` |
| System blocks and responsibilities | `docs/system-design.md` |
| Cross-domain pin, protocol, connector, and mechanical contracts | `docs/interfaces.md` |
| Selected and alternate purchasable parts | `parts/bom.csv`, `parts/alternates.csv` |
| Ratings and vendor claims | `references/` plus `references/sources.csv` |
| Logical electrical connectivity | KiCad schematic under `electrical/kicad/` |
| Actual wires, colors, gauges, lengths, and connector pins | `electrical/wiring/harness.yml` |
| Dimensions, placement, clearances, and enclosure geometry | CadQuery under `mechanical/` |
| Firmware pin assignment and behavior | `firmware/` plus `docs/interfaces.md` |
| Observed behavior | `docs/measurements.md` and `docs/build-log.md` |
| Pass/fail evidence | `docs/verification.md` |

## Commands

```text
make help            Show available commands
make check           Validate structure, links, metadata, and tabular schemas
make check-strict    Also reject unfinished project metadata and placeholder BOM rows
make cad-setup       Create .venv and install CadQuery/test dependencies
make cad             Export STEP/STL models and SVG previews
make cad-test        Run mechanical geometry tests
make cad-view        Open the model in the OCP CAD Viewer workflow
make wiring-setup    Install the pinned WireViz tool
make wiring-check    Parse the harness and generate its tabular BOM
make wiring          Render the WireViz harness
make kicad-erc       Run KiCad electrical-rules checks
```

Generated CAD, wiring, and EDA reports are ignored. Deliberately promote small
review artifacts (for example, a release preview image) when they are useful to
future builders.

## Repository layout

```text
docs/                 Requirements, architecture, decisions, logs, and verification
references/           Datasheets, drawings, source register, and extracted facts
parts/                BOM, alternates, and selection records
electrical/           KiCad project, WireViz harness, net conventions, reports
mechanical/           CadQuery source, tests, exports, and previews
firmware/             Firmware source and hardware-test notes
scripts/              Dependency-light project checks
```

The defaults target module-based, low-voltage prototypes. Battery, charging,
mains, high-current, high-temperature, pressure, radio, or safety-critical work
requires a dedicated risk review; see [the safety playbook](docs/domains/safety.md).
