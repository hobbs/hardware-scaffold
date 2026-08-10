#!/usr/bin/env python3
"""Dependency-free structural checks for the hardware project.

The ordinary mode allows template placeholders while checking coherence. Strict
mode is a release gate and rejects placeholders in project-owned living artifacts.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
import re
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = (
    "AGENTS.md",
    "CLAUDE.md",
    "project.toml",
    "docs/project-brief.md",
    "docs/system-design.md",
    "docs/interfaces.md",
    "docs/risks.md",
    "docs/verification.md",
    "parts/bom.csv",
    "references/sources.csv",
    "electrical/wiring/harness.yml",
    "mechanical/build.py",
    "mechanical/src/project/assembly.py",
    "firmware/README.md",
)

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
    },
}

LIVING_ARTIFACTS = (
    "docs/project-brief.md",
    "docs/system-design.md",
    "docs/interfaces.md",
    "docs/risks.md",
    "docs/verification.md",
    "firmware/README.md",
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
IDENTIFIERS = {
    "part_id": re.compile(r"^PART-\d{3}$"),
    "source_id": re.compile(r"^SRC-\d{3}$"),
}


@dataclass
class Finding:
    severity: str
    message: str


class Checks:
    def __init__(self, strict: bool) -> None:
        self.strict = strict
        self.findings: list[Finding] = []

    def error(self, message: str) -> None:
        self.findings.append(Finding("ERROR", message))

    def warn(self, message: str) -> None:
        self.findings.append(Finding("WARN", message))

    def required_paths(self) -> None:
        for relative in REQUIRED_PATHS:
            if not (ROOT / relative).exists():
                self.error(f"missing required path: {relative}")

    def metadata(self) -> None:
        path = ROOT / "project.toml"
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
        if self.strict and str(project.get("name", "")).startswith("Untitled"):
            self.error("strict: replace the default project name in project.toml")
        if self.strict and project.get("slug") == "untitled-hardware":
            self.error("strict: replace the default project slug in project.toml")

    def csv_files(self) -> tuple[dict[str, list[dict[str, str]]], set[str]]:
        loaded: dict[str, list[dict[str, str]]] = {}
        source_ids: set[str] = set()

        for relative, required_columns in CSV_SCHEMAS.items():
            path = ROOT / relative
            if not path.exists():
                self.error(f"missing table: {relative}")
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
                joined = " ".join(row.values()).upper()
                if "TBD" in joined or "PLACEHOLDER" in joined:
                    self.error(
                        f"strict: parts/bom.csv:{line} contains a placeholder"
                    )
                if row.get("status") not in {"Selected", "Ordered", "Received", "Verified"}:
                    self.error(
                        f"strict: parts/bom.csv:{line} status is not selected or later"
                    )
            for line, row in enumerate(
                loaded.get("references/sources.csv", []), start=2
            ):
                joined = " ".join(row.values()).upper()
                if "TBD" in joined or "UNVERIFIED" in joined or "PLACEHOLDER" in joined:
                    self.error(
                        f"strict: references/sources.csv:{line} is unfinished"
                    )

    def markdown_links(self) -> None:
        for path in ROOT.rglob("*.md"):
            if any(part.startswith(".") and part != "." for part in path.relative_to(ROOT).parts):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                self.error(f"cannot read {path.relative_to(ROOT)}: {exc}")
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
                target_path = target.split("#", 1)[0]
                resolved = (path.parent / target_path).resolve()
                if not resolved.exists():
                    self.error(
                        f"{path.relative_to(ROOT)} has broken local link: {target}"
                    )

    def python_syntax(self) -> None:
        for path in (ROOT / "mechanical").rglob("*.py"):
            try:
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
            except (OSError, SyntaxError) as exc:
                self.error(f"invalid Python in {path.relative_to(ROOT)}: {exc}")
        try:
            tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            self.error(f"pyproject.toml is invalid: {exc}")

    def strict_placeholders(self) -> None:
        if not self.strict:
            return
        marker = re.compile(r"\b(TBD|TO BE DETERMINED)\b", re.IGNORECASE)
        for relative in LIVING_ARTIFACTS:
            path = ROOT / relative
            if path.exists() and marker.search(path.read_text(encoding="utf-8")):
                self.error(f"strict: {relative} still contains TBD")

    def run(self) -> int:
        self.required_paths()
        self.metadata()
        loaded, source_ids = self.csv_files()
        self.table_references(loaded, source_ids)
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
    parser.add_argument(
        "--strict",
        action="store_true",
        help="reject placeholders and incomplete release-critical records",
    )
    args = parser.parse_args()
    return Checks(strict=args.strict).run()


if __name__ == "__main__":
    sys.exit(main())
