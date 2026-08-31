---
name: init-project
description: Initialize a new hardware project as a clean, independent Git repository under this workspace's ignored projects directory. Use when the user asks to start, create, bootstrap, or initialize a device project.
---

# Initialize a hardware project

Create one project under `projects/<slug>/`. The project must contain only the
completed framing work; never copy `templates/project/` or create files for future
design stages.

## Ground the project

1. Work from the hardware workspace root containing `scripts/init_project.py` and
   `templates/project/`.
2. Read `docs/domains/system-design.md` before framing the project.
3. Extract a concrete project name and one-sentence goal from the request. Derive a
   lowercase, hyphenated slug. Do not use an “untitled” or placeholder name.
4. Identify architecture-changing unknowns: power source, environment, physical
   scale, critical inputs and outputs, fabrication method, and budget.
5. Ask only about unknowns whose plausible answers lead to materially different
   architectures or safety controls. Make conservative, reversible assumptions for
   ordinary gaps. Never infer a hazardous power source, environment, or mechanism.
6. Express only observable, already-agreed behavior as requirements. Do not turn a
   preferred implementation into a requirement.

## Initialize atomically

Run `scripts/init_project.py` once. Pass each known fact with a structured option:

```text
python3 scripts/init_project.py <slug> \
  --name "<project name>" \
  --goal "<one-sentence goal>" \
  --owner "<owner, only if known>" \
  --requirement "<observable criterion>::<verification method>" \
  --constraint "<dimension>::<target or limit>::<source>" \
  --assumption "<assumption>::<consequence if false>::<resolution>" \
  --question "<question>::<why it changes the design>::<resolution method>"
```

Options other than `--name` and `--goal` are repeatable and optional. Omit an
unknown optional field instead of writing `TBD`, “unknown”, an empty table, or a
placeholder. Record a question only when it is concrete and has a resolution
method. Quote every structured argument so shell punctuation remains data.

The initializer must:

- refuse an invalid slug or existing destination;
- create `projects/<slug>/.git/` with `main` as the initial branch;
- create populated `project.toml` and `docs/project-brief.md` files;
- create `docs/open-questions.md` only when at least one real question is passed;
- copy only the functional project `.gitignore` from the templates;
- leave the repository uncommitted so the user controls commit history.

Do not add `AGENTS.md`, `README.md`, a Makefile, build configuration, BOM, source
register, schematic, harness, firmware, CAD, verification plan, empty directory, or
`.gitkeep` during initialization. The workspace's parent instructions govern the
nested project while it remains here.

## Verify

From the workspace root, run:

```text
make check-project PROJECT=projects/<slug>
git -C projects/<slug> status --short --branch
```

Then inspect the project directory. It must contain no artifact unrelated to the
framing work and no `TBD` or generic placeholder. Report the path, the one-sentence
goal, recorded assumptions or open questions, and verification commands. Do not
make an initial commit unless the user explicitly asks for one.
