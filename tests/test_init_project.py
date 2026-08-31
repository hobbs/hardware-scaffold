from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
INITIALIZER = ROOT / "scripts/init_project.py"
CHECKER = ROOT / "scripts/check_project.py"


class InitializeProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.projects = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def initialize(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(INITIALIZER),
                *arguments,
                "--projects-dir",
                str(self.projects),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_minimal_project_is_clean_independent_repository(self) -> None:
        result = self.initialize(
            "desk-monitor",
            "--name",
            "Desk Monitor",
            "--goal",
            "Measure and display indoor air quality for people in a shared office.",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        project = self.projects / "desk-monitor"
        self.assertEqual(
            {
                path.relative_to(project).as_posix()
                for path in project.rglob("*")
                if ".git" not in path.parts
            },
            {".gitignore", "docs", "docs/project-brief.md", "project.toml"},
        )
        brief = (project / "docs/project-brief.md").read_text(encoding="utf-8")
        self.assertNotRegex(brief, r"\b(?:TBD|PLACEHOLDER)\b")
        self.assertFalse((project / "docs/open-questions.md").exists())
        branch = subprocess.run(
            ["git", "-C", str(project), "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(branch, "main")

        check = subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(project), "--strict"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_records_only_supplied_framing_artifacts(self) -> None:
        result = self.initialize(
            "bench-supply",
            "--name",
            "Bench Supply",
            "--goal",
            "Provide adjustable low-voltage DC power for electronics prototypes.",
            "--requirement",
            "Output voltage is adjustable from 0 V to 15 V::Measure output with a calibrated DMM",
            "--constraint",
            "Environment::Indoor electronics bench::User requirement",
            "--assumption",
            "A mains-certified external adapter supplies input power::The power architecture must be reviewed::Confirm adapter before part selection",
            "--question",
            "What maximum output current is required?::It sets converter and thermal sizing::Measure representative loads",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        project = self.projects / "bench-supply"
        brief = (project / "docs/project-brief.md").read_text(encoding="utf-8")
        questions = (project / "docs/open-questions.md").read_text(encoding="utf-8")
        self.assertIn("REQ-001", brief)
        self.assertIn("ASM-001", brief)
        self.assertIn("Q-001", questions)
        for absent in ("parts", "references", "electrical", "mechanical", "firmware"):
            self.assertFalse((project / absent).exists())

    def test_rejects_placeholders_invalid_slugs_and_existing_projects(self) -> None:
        placeholder = self.initialize(
            "new-device",
            "--name",
            "Untitled TBD device",
            "--goal",
            "Do something useful.",
        )
        self.assertNotEqual(placeholder.returncode, 0)
        self.assertFalse((self.projects / "new-device").exists())

        invalid = self.initialize(
            "../escape",
            "--name",
            "Escaping Device",
            "--goal",
            "Remain inside the project directory.",
        )
        self.assertNotEqual(invalid.returncode, 0)

        first = self.initialize(
            "existing",
            "--name",
            "Existing Device",
            "--goal",
            "Exercise destination collision handling.",
        )
        second = self.initialize(
            "existing",
            "--name",
            "Existing Device",
            "--goal",
            "Exercise destination collision handling.",
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertNotEqual(second.returncode, 0)


if __name__ == "__main__":
    unittest.main()
