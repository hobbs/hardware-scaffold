from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts/check_project.py"


class FirmwareProjectCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.project = Path(self.temporary.name) / "firmware-check"
        (self.project / ".git").mkdir(parents=True)
        (self.project / "docs").mkdir()
        (self.project / "firmware").mkdir()
        (self.project / "project.toml").write_text(
            """[project]
name = "Firmware Check"
slug = "firmware-check"
status = "prototype"
revision = "0.1"
units = "mm"
""",
            encoding="utf-8",
        )
        (self.project / "docs" / "project-brief.md").write_text(
            "# Project brief\n\nExercise firmware validation.\n", encoding="utf-8"
        )
        (self.project / "docs" / "system-design.md").write_text(
            "# System design\n\nThe controller runs one diagnostic phase.\n",
            encoding="utf-8",
        )
        (self.project / ".gitignore").write_text(".pio/\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def check(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(self.project)],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_accepts_pinned_platformio_project(self) -> None:
        (self.project / "firmware" / "README.md").write_text(
            "# Firmware\n\nBuild with `pio run`.\n", encoding="utf-8"
        )
        (self.project / "firmware" / "platformio.ini").write_text(
            """[env:controller]
platform = https://github.com/vendor/platform.git#0123456789abcdef0123456789abcdef01234567
board = exact-controller
framework = arduino
lib_deps = vendor/parser@2.1.0
""",
            encoding="utf-8",
        )

        result = self.check()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_moving_dependencies_and_machine_port(self) -> None:
        (self.project / "firmware" / "README.md").write_text(
            "# Firmware\n", encoding="utf-8"
        )
        (self.project / "firmware" / "platformio.ini").write_text(
            """[env]
upload_port = /dev/cu.usbmodem1101
lib_deps =
    vendor/unpinned
    https://github.com/vendor/parser.git#main

[env:controller]
platform = https://github.com/vendor/platform.git#main
board = exact-controller
framework = arduino
""",
            encoding="utf-8",
        )

        result = self.check()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("platform is not pinned to a full Git commit", result.stdout)
        self.assertIn("upload_port contains a machine-local port", result.stdout)
        self.assertIn("is not pinned to an exact version", result.stdout)
        self.assertIn("lib_deps entry", result.stdout)

    def test_requires_readme_environment_and_ignored_build_products(self) -> None:
        (self.project / ".gitignore").write_text("build/\n", encoding="utf-8")
        (self.project / "firmware" / "platformio.ini").write_text(
            "[platformio]\ndefault_envs = controller\n", encoding="utf-8"
        )

        result = self.check()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires firmware/README.md", result.stdout)
        self.assertIn("has no [env:...] build environment", result.stdout)
        self.assertIn("requires .pio/ in .gitignore", result.stdout)


if __name__ == "__main__":
    unittest.main()
