#!/usr/bin/env python3
"""Dependency-free checks for a progressively materialized hardware project."""

from __future__ import annotations

import argparse
import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
import re
import sys
import tomllib


CORE_PATHS = (".git", "project.toml", "docs/project-brief.md")
CSV_SCHEMAS = {
    "parts/bom.csv": {
        "part_id",
        "description",
        "manufacturer_part_number",
        "quantity",
        "source_ids",
        "status",
    },
    "parts/alternates.csv": {
        "part_id",
        "candidate_part_number",
        "evaluation_status",
        "compatibility_or_changes",
        "source_ids",
    },
    "references/sources.csv": {
        "source_id",
        "part_id",
        "title",
        "document_revision",
        "source_url",
        "local_path",
        "accessed_date",
        "authority",
        "file_sha256",
    },
}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
PLACEHOLDER = re.compile(r"\b(?:TBD|TO BE DETERMINED|PLACEHOLDER)\b", re.IGNORECASE)
IDENTIFIERS = {
    "part_id": re.compile(r"^PART-\d{3}$"),
    "source_id": re.compile(r"^SRC-\d{3}$"),
}
LATER_STAGE_ROOTS = ("parts", "references", "electrical", "mechanical", "firmware")


@dataclass
class Finding:
    severity: str
    message: str


class Checks:
    def __init__(self, root: Path, strict: bool) -> None:
        self.root = root.resolve()
        self.strict = strict
        self.findings: list[Finding] = []

    def error(self, message: str) -> None:
        self.findings.append(Finding("ERROR", message))

    def warn(self, message: str) -> None:
        self.findings.append(Finding("WARN", message))

    def required_paths(self) -> None:
        for relative in CORE_PATHS:
            if not (self.root / relative).exists():
                self.error(f"missing required path: {relative}")
        if any((self.root / relative).exists() for relative in LATER_STAGE_ROOTS):
            if not (self.root / "docs/system-design.md").is_file():
                self.error(
                    "later-stage artifacts require an implemented docs/system-design.md"
                )

    def metadata(self) -> None:
        path = self.root / "project.toml"
        if not path.exists():
            return
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            self.error(f"project.toml is invalid: {exc}")
            return

        project = data.get("project", {})
        required = {"name", "slug", "status", "revision", "units"}
        missing = sorted(required - project.keys())
        if missing:
            self.error(f"project.toml [project] is missing: {', '.join(missing)}")
        if project.get("units") != "mm":
            self.warn("project.toml units is not 'mm'; mechanical source assumes mm")
        if project.get("status") not in {
            "concept",
            "architecture",
            "prototype",
            "verification",
            "released",
            "paused",
        }:
            self.error("project.toml status is not a recognized lifecycle state")
        slug = project.get("slug")
        if slug and slug != self.root.name:
            self.error(
                f"project.toml slug {slug!r} does not match directory {self.root.name!r}"
            )

    def csv_files(self) -> tuple[dict[str, list[dict[str, str]]], set[str]]:
        loaded: dict[str, list[dict[str, str]]] = {}
        source_ids: set[str] = set()

        for relative, required_columns in CSV_SCHEMAS.items():
            path = self.root / relative
            if not path.exists():
                continue
            try:
                with path.open(newline="", encoding="utf-8") as handle:
                    reader = csv.DictReader(handle)
                    columns = set(reader.fieldnames or [])
                    rows = list(reader)
            except (OSError, csv.Error) as exc:
                self.error(f"cannot read {relative}: {exc}")
                continue

            missing = sorted(required_columns - columns)
            if missing:
                self.error(f"{relative} missing columns: {', '.join(missing)}")
            if not rows:
                self.error(f"{relative} is an empty stub; remove it until it has records")
            loaded[relative] = rows

            id_column = "source_id" if relative == "references/sources.csv" else "part_id"
            seen: set[str] = set()
            for line, row in enumerate(rows, start=2):
                value = (row.get(id_column) or "").strip()
                pattern = IDENTIFIERS[id_column]
                if not pattern.match(value):
                    self.error(f"{relative}:{line} invalid {id_column}: {value!r}")
                elif value in seen and relative != "parts/alternates.csv":
                    self.error(f"{relative}:{line} duplicate {id_column}: {value}")
                seen.add(value)
            if relative == "references/sources.csv":
                source_ids = seen

        return loaded, source_ids

    def source_files(self, loaded: dict[str, list[dict[str, str]]]) -> None:
        for line, row in enumerate(
            loaded.get("references/sources.csv", []), start=2
        ):
            local_path = (row.get("local_path") or "").strip()
            expected_digest = (row.get("file_sha256") or "").strip().lower()
            if not local_path:
                if expected_digest:
                    self.error(
                        f"references/sources.csv:{line} has file_sha256 without local_path"
                    )
                continue

            path = (self.root / local_path).resolve()
            if not path.is_relative_to(self.root):
                self.error(
                    f"references/sources.csv:{line} local_path escapes project: "
                    f"{local_path}"
                )
                continue
            if not path.is_file():
                self.error(
                    f"references/sources.csv:{line} missing local file: {local_path}"
                )
                continue
            if not re.fullmatch(r"[0-9a-f]{64}", expected_digest):
                self.error(
                    f"references/sources.csv:{line} invalid SHA-256 for {local_path}"
                )
                continue

            digest = hashlib.sha256()
            try:
                with path.open("rb") as handle:
                    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                        digest.update(chunk)
            except OSError as exc:
                self.error(
                    f"references/sources.csv:{line} cannot hash {local_path}: {exc}"
                )
                continue
            if digest.hexdigest() != expected_digest:
                self.error(
                    f"references/sources.csv:{line} SHA-256 mismatch: {local_path}"
                )

    def table_references(
        self, loaded: dict[str, list[dict[str, str]]], source_ids: set[str]
    ) -> None:
        for relative in ("parts/bom.csv", "parts/alternates.csv"):
            for line, row in enumerate(loaded.get(relative, []), start=2):
                values = (row.get("source_ids") or "").split(";")
                for value in (item.strip() for item in values if item.strip()):
                    if value not in source_ids:
                        self.error(
                            f"{relative}:{line} references unknown source ID {value}"
                        )

        if self.strict:
            for line, row in enumerate(loaded.get("parts/bom.csv", []), start=2):
                if row.get("status") not in {
                    "Selected",
                    "Ordered",
                    "Received",
                    "Verified",
                }:
                    self.error(
                        f"strict: parts/bom.csv:{line} status is not selected or later"
                    )

    def markdown_links(self) -> None:
        for path in self.root.rglob("*.md"):
            relative = path.relative_to(self.root)
            if any(part.startswith(".") for part in relative.parts):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                self.error(f"cannot read {relative}: {exc}")
                continue
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
                    self.error(f"{relative} has broken local link: {target}")

    def python_syntax(self) -> None:
        for path in self.root.rglob("*.py"):
            relative = path.relative_to(self.root)
            if any(part.startswith(".") for part in relative.parts):
                continue
            try:
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
            except (OSError, SyntaxError) as exc:
                self.error(f"invalid Python in {relative}: {exc}")
        pyproject = self.root / "pyproject.toml"
        if pyproject.exists():
            try:
                tomllib.loads(pyproject.read_text(encoding="utf-8"))
            except (OSError, tomllib.TOMLDecodeError) as exc:
                self.error(f"pyproject.toml is invalid: {exc}")

    def strict_placeholders(self) -> None:
        if not self.strict:
            return
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(self.root)
            if any(part.startswith(".") for part in relative.parts):
                continue
            if path.suffix.lower() not in {".md", ".csv", ".toml", ".yml", ".yaml"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                self.error(f"cannot inspect {relative}: {exc}")
                continue
            if PLACEHOLDER.search(text):
                self.error(f"strict: {relative} contains a placeholder")

    def run(self) -> int:
        if not self.root.is_dir():
            print(f"ERROR: project root does not exist: {self.root}")
            return 1
        self.required_paths()
        self.metadata()
        loaded, source_ids = self.csv_files()
        self.table_references(loaded, source_ids)
        self.source_files(loaded)
        self.markdown_links()
        self.python_syntax()
        self.strict_placeholders()

        for finding in self.findings:
            print(f"{finding.severity}: {finding.message}")
        errors = sum(item.severity == "ERROR" for item in self.findings)
        warnings = sum(item.severity == "WARN" for item in self.findings)
        if errors:
            print(f"Project check failed: {errors} error(s), {warnings} warning(s).")
            return 1
        print(f"Project check passed: {warnings} warning(s).")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--strict",
        action="store_true",
        help="reject placeholders and incomplete release-critical records",
    )
    args = parser.parse_args()
    return Checks(root=args.root, strict=args.strict).run()


if __name__ == "__main__":
    sys.exit(main())
