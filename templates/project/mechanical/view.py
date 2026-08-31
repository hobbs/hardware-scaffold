#!/usr/bin/env python3
"""Send named project geometry to the VS Code OCP CAD Viewer."""

from pathlib import Path
import sys

MECHANICAL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(MECHANICAL_DIR / "src"))

from ocp_vscode import show  # noqa: E402

from project.components.reference_board import (  # noqa: E402
    make_board,
    make_connector_keepout,
)
from project.enclosure import make_base, make_lid  # noqa: E402
from project.parameters import BOARD, ENCLOSURE  # noqa: E402


def main() -> None:
    board = make_board(BOARD).translate((0, 0, ENCLOSURE.board_z))
    keepout = make_connector_keepout(BOARD).translate((0, 0, ENCLOSURE.board_z))
    lid = make_lid(ENCLOSURE).translate((0, 0, ENCLOSURE.base_height))
    show(
        make_base(ENCLOSURE),
        lid,
        board,
        keepout,
        names=["base", "lid", "PART-001 board", "connector keep-out"],
        colors=["lightgray", "silver", "green", "orange"],
        alphas=[0.75, 0.35, 1.0, 0.25],
        reset_camera=True,
    )


if __name__ == "__main__":
    main()
