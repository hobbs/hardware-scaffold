# Hardware Project Workspace

An opinionated, chat-first workspace for developing small hardware devices. This
repository is installed once. Each device is initialized under `projects/` as an
independent Git repository; the workspace repository ignores that directory.

The workspace separates reusable process from project evidence:

- `docs/domains/` contains engineering playbooks.
- `templates/project/` contains reference artifacts for each design stage.
- `.agents/skills/init-project/` contains the project initialization skill.
- `scripts/` contains initialization and progressive project checks.
- `projects/<slug>/` contains local project repositories and is never tracked here.

## Initialize a project

Open an agent in this repository and ask it to use the
[`init-project` skill](.agents/skills/init-project/SKILL.md). Include the device's
goal and any known constraints:

> Use the init-project skill to start a desk air-quality monitor for a shared
> office. It will use USB-C power and should cost no more than $100.

The skill resolves only choices that materially affect the architecture, records
concrete assumptions and questions, and runs `scripts/init_project.py`. A new
project starts with:

```text
projects/<slug>/
├── .git/
├── .gitignore
├── project.toml
└── docs/
    ├── project-brief.md
    └── open-questions.md   # only when real questions exist
```

No BOM, schematic, harness, firmware tree, CAD model, test plan, or empty
placeholder file is created before that work begins. When a design step is
implemented, use the corresponding file under `templates/project/` as a reference
and add only real project content.

## Commands

```text
make help
make check
make init NAME="Desk Monitor" SLUG=desk-monitor GOAL="Measure and display indoor air quality for office occupants."
make check-project PROJECT=projects/desk-monitor
make check-strict PROJECT=projects/desk-monitor
```

`make check` validates this workspace and exercises project initialization in a
temporary directory. `check-project` accepts partial projects: metadata and the
brief are required, while later-stage artifacts are checked only when present.
`check-strict` additionally rejects placeholders in materialized project
artifacts.

## Design sequence

1. Frame the goal, constraints, assumptions, and acceptance criteria.
2. Architect system blocks, power, interfaces, and failure behavior.
3. Select evidence-backed parts and alternates.
4. Prototype the electrical, firmware, and mechanical slices that are needed.
5. Integrate shared interfaces, physical access, assembly order, and service.
6. Verify requirements and risks with recorded evidence.
7. Release frozen sources, build outputs, instructions, and known limitations.

The project tree grows with this sequence. Do not copy `templates/project/`
wholesale and do not skip directly from an idea to parts or enclosure geometry.

## Source-of-truth map

Within a project:

| Fact | Authoritative artifact when implemented |
| --- | --- |
| User need, constraint, acceptance criterion | `docs/project-brief.md` |
| System blocks and responsibilities | `docs/system-design.md` |
| Cross-domain contracts | `docs/interfaces.md` |
| Selected and alternate purchasable parts | `parts/bom.csv`, `parts/alternates.csv` |
| Ratings and vendor claims | `references/` and `references/sources.csv` |
| Logical electrical connectivity | KiCad source under `electrical/kicad/` |
| Buildable wire harness | `electrical/wiring/harness.yml` |
| Dimensions, placement, and manufactured geometry | CadQuery source under `mechanical/` |
| Firmware behavior and executable pin assignment | `firmware/` and `docs/interfaces.md` |
| Measurements and pass/fail evidence | `docs/measurements.md`, `docs/verification.md` |

The defaults target module-based, low-voltage prototypes. Battery, charging,
mains, high-current, high-temperature, pressure, radio, motion, laser, or
safety-critical work requires the
[safety playbook](docs/domains/safety.md) before release.
