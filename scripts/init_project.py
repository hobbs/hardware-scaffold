#!/usr/bin/env python3
"""Create a minimal hardware project as an isolated Git repository."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


SCAFFOLD_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECTS_DIR = SCAFFOLD_ROOT / "projects"
TEMPLATE_GITIGNORE = SCAFFOLD_ROOT / "templates" / "project" / ".gitignore"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACEHOLDER = re.compile(r"\b(?:TBD|TO BE DETERMINED|PLACEHOLDER)\b", re.IGNORECASE)


def clean(value: str, label: str) -> str:
    value = " ".join(value.split())
    if not value:
        raise ValueError(f"{label} must not be empty")
    if PLACEHOLDER.search(value):
        raise ValueError(f"{label} must describe known work, not a placeholder")
    return value


def fields(value: str, count: int, label: str) -> tuple[str, ...]:
    values = tuple(clean(item, label) for item in value.split("::"))
    if len(values) != count:
        raise ValueError(f"{label} must contain {count} fields separated by '::'")
    return values


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|")


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_metadata(name: str, slug: str, owner: str | None) -> str:
    lines = [
        "[project]",
        f"name = {toml_string(name)}",
        f"slug = {toml_string(slug)}",
        'status = "concept"',
        'revision = "0.1"',
        'units = "mm"',
    ]
    if owner:
        lines.extend(["", "[owners]", f"design = {toml_string(owner)}"])
    return "\n".join(lines) + "\n"


def render_brief(
    goal: str,
    owner: str | None,
    requirements: list[tuple[str, str]],
    constraints: list[tuple[str, str, str]],
    assumptions: list[tuple[str, str, str]],
) -> str:
    lines = [
        "# Project brief",
        "",
        "Status: draft",
        f"Last reviewed: {date.today().isoformat()}",
    ]
    if owner:
        lines.append(f"Owner: {owner}")
    lines.extend(["", "## One-sentence goal", "", goal])

    if requirements:
        lines.extend(
            [
                "",
                "## Requirements",
                "",
                "| ID | Requirement / acceptance criterion | Priority | Verification | Status |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for index, (requirement, verification) in enumerate(requirements, start=1):
            lines.append(
                f"| REQ-{index:03d} | {markdown_cell(requirement)} | Must | "
                f"{markdown_cell(verification)} | Proposed |"
            )

    if constraints:
        lines.extend(
            [
                "",
                "## Constraints",
                "",
                "| Dimension | Target or limit | Why / source |",
                "| --- | --- | --- |",
            ]
        )
        for dimension, target, source in constraints:
            lines.append(
                f"| {markdown_cell(dimension)} | {markdown_cell(target)} | "
                f"{markdown_cell(source)} |"
            )

    if assumptions:
        lines.extend(
            [
                "",
                "## Assumptions",
                "",
                "| ID | Assumption | Consequence if false | Resolution |",
                "| --- | --- | --- | --- |",
            ]
        )
        for index, (assumption, consequence, resolution) in enumerate(assumptions, start=1):
            lines.append(
                f"| ASM-{index:03d} | {markdown_cell(assumption)} | "
                f"{markdown_cell(consequence)} | {markdown_cell(resolution)} |"
            )

    return "\n".join(lines) + "\n"


def render_questions(questions: list[tuple[str, str, str]]) -> str:
    lines = [
        "# Open questions",
        "",
        "| ID | Question | Why it matters | Resolution method | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for index, (question, why, resolution) in enumerate(questions, start=1):
        lines.append(
            f"| Q-{index:03d} | {markdown_cell(question)} | {markdown_cell(why)} | "
            f"{markdown_cell(resolution)} | Open |"
        )
    return "\n".join(lines) + "\n"


def initialize(args: argparse.Namespace) -> Path:
    name = clean(args.name, "name")
    goal = clean(args.goal, "goal")
    owner = clean(args.owner, "owner") if args.owner else None
    if not SLUG.fullmatch(args.slug):
        raise ValueError("slug must contain lowercase letters, digits, and single hyphens")

    requirements = [fields(value, 2, "requirement") for value in args.requirement]
    constraints = [fields(value, 3, "constraint") for value in args.constraint]
    assumptions = [fields(value, 3, "assumption") for value in args.assumption]
    questions = [fields(value, 3, "question") for value in args.question]

    projects_dir = args.projects_dir.resolve()
    destination = projects_dir / args.slug
    if destination.exists():
        raise FileExistsError(f"project already exists: {destination}")
    if not TEMPLATE_GITIGNORE.is_file():
        raise FileNotFoundError(f"missing template: {TEMPLATE_GITIGNORE}")

    projects_dir.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{args.slug}-", dir=projects_dir))
    try:
        (temporary / "docs").mkdir()
        shutil.copyfile(TEMPLATE_GITIGNORE, temporary / ".gitignore")
        (temporary / "project.toml").write_text(
            render_metadata(name, args.slug, owner), encoding="utf-8"
        )
        (temporary / "docs" / "project-brief.md").write_text(
            render_brief(goal, owner, requirements, constraints, assumptions),
            encoding="utf-8",
        )
        if questions:
            (temporary / "docs" / "open-questions.md").write_text(
                render_questions(questions), encoding="utf-8"
            )
        subprocess.run(
            ["git", "init", "-q", "-b", "main", str(temporary)], check=True
        )
        temporary.replace(destination)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return destination


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="initialize a clean project under the scaffold's projects directory"
    )
    result.add_argument("slug")
    result.add_argument("--name", required=True)
    result.add_argument("--goal", required=True)
    result.add_argument("--owner")
    result.add_argument(
        "--requirement",
        action="append",
        default=[],
        metavar="CRITERION::VERIFICATION",
    )
    result.add_argument(
        "--constraint",
        action="append",
        default=[],
        metavar="DIMENSION::TARGET::SOURCE",
    )
    result.add_argument(
        "--assumption",
        action="append",
        default=[],
        metavar="ASSUMPTION::CONSEQUENCE::RESOLUTION",
    )
    result.add_argument(
        "--question",
        action="append",
        default=[],
        metavar="QUESTION::WHY::RESOLUTION",
    )
    result.add_argument(
        "--projects-dir",
        type=Path,
        default=DEFAULT_PROJECTS_DIR,
        help=argparse.SUPPRESS,
    )
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        destination = initialize(args)
    except (FileExistsError, FileNotFoundError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"error: {exc}") from exc
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
