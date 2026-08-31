#!/usr/bin/env python3
"""Validate the reusable workspace without treating it as a device project."""

from __future__ import annotations

from pathlib import Path
import re
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
    ".agents/skills/init-project/SKILL.md",
    ".claude/skills/init-project/SKILL.md",
    ".agents/skills/capture-datasheets/SKILL.md",
    ".claude/skills/capture-datasheets/SKILL.md",
    "AGENTS.md",
    "CLAUDE.md",
    "Makefile",
    "README.md",
    "docs/domains/electrical.md",
    "docs/domains/system-design.md",
    "scripts/check_project.py",
    "scripts/init_project.py",
    "templates/project/.gitignore",
    "templates/project/Makefile",
    "templates/project/project.toml",
    "templates/project/docs/project-brief.md",
    "templates/project/electrical/breadboard-wiring.md",
    "templates/project/electrical/kicad/README.md",
    "templates/project/electrical/wiring/harness.yml",
    "templates/project/mechanical/src/project/assembly.py",
)
REQUIRED_TEXT = {
    "Makefile": ("kicad-toolcheck:",),
    "docs/domains/electrical.md": (
        "## Schematic tool and topology gate",
        "make kicad-toolcheck",
    ),
    "templates/project/Makefile": (
        "kicad-toolcheck:",
        "kicad-erc: kicad-toolcheck",
    ),
    "templates/project/electrical/kicad/README.md": (
        "## Tool gate",
        "KiCanvas",
    ),
    "templates/project/electrical/breadboard-wiring.md": (
        "## Physical module topology",
        "## Bench power connection",
    ),
}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")


def visible_markdown() -> list[Path]:
    paths: list[Path] = []
    for path in ROOT.rglob("*.md"):
        relative = path.relative_to(ROOT)
        if relative.parts[0] == "projects":
            continue
        if any(part.startswith(".") for part in relative.parts):
            continue
        paths.append(path)
    return paths


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_PATHS:
        if not (ROOT / relative).exists():
            errors.append(f"missing workspace path: {relative}")

    for relative, required_fragments in REQUIRED_TEXT.items():
        path = ROOT / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in text:
                errors.append(f"{relative} is missing required workflow text: {fragment}")

    if (ROOT / "project.toml").exists():
        errors.append("workspace root must not be a device project")
    ignore_lines = {
        line.strip() for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    }
    if "projects/" not in ignore_lines:
        errors.append(".gitignore must ignore projects/")

    for skill_name in ("init-project", "capture-datasheets"):
        skill = ROOT / f".agents/skills/{skill_name}/SKILL.md"
        if not skill.exists():
            continue
        skill_text = skill.read_text(encoding="utf-8")
        if not skill_text.startswith(f"---\nname: {skill_name}\n"):
            errors.append(f"{skill_name} skill has invalid frontmatter")
        if "description:" not in skill_text.split("---", 2)[1]:
            errors.append(f"{skill_name} skill is missing a description")

    for path in visible_markdown():
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if (
                not target
                or target.startswith("#")
                or "://" in target
                or target.startswith("mailto:")
            ):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                errors.append(
                    f"{path.relative_to(ROOT)} has broken local link: {target}"
                )

    python_roots = (ROOT / "scripts", ROOT / "templates/project/mechanical")
    for python_root in python_roots:
        for path in python_root.rglob("*.py"):
            try:
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
            except (OSError, SyntaxError) as exc:
                errors.append(f"invalid Python in {path.relative_to(ROOT)}: {exc}")

    for relative in ("templates/project/project.toml", "templates/project/pyproject.toml"):
        path = ROOT / relative
        if not path.exists():
            continue
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            errors.append(f"invalid TOML in {relative}: {exc}")

    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"Workspace check failed: {len(errors)} error(s).")
        return 1
    print("Workspace check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
