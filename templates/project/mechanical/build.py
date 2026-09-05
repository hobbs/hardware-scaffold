#!/usr/bin/env python3
"""Build deterministic mechanical exports from CadQuery source."""

from pathlib import Path
import sys
from xml.etree import ElementTree as ET

MECHANICAL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(MECHANICAL_DIR / "src"))

from cadquery import exporters  # noqa: E402
import cadquery as cq  # noqa: E402

from project.assembly import make_review_assembly  # noqa: E402
from project.components.reference_board import make_board  # noqa: E402
from project.enclosure import make_base, make_lid  # noqa: E402
from project.parameters import BOARD, ENCLOSURE  # noqa: E402


def export_shape(shape, stem: str, *, printable: bool = False) -> None:
    exports = MECHANICAL_DIR / "exports"
    exporters.export(shape, str(exports / f"{stem}.step"))
    if printable:
        exporters.export(
            shape,
            str(exports / f"{stem}.stl"),
            tolerance=0.02,
            angularTolerance=0.1,
        )


def export_svg(shape, stem: str) -> None:
    exporters.export(
        shape,
        str(MECHANICAL_DIR / "previews" / f"{stem}.svg"),
        opt={
            "projectionDir": (1.0, -1.0, 0.75),
            "showAxes": True,
            "width": 900,
            "height": 650,
            "strokeWidth": 0.35,
        },
    )
    # Keep black geometry visible in both light and dark review surfaces.
    # SVG/CSS background styling is not honored by every rasterizer.
    preview_path = MECHANICAL_DIR / "previews" / f"{stem}.svg"
    tree = ET.parse(preview_path)
    namespace = "http://www.w3.org/2000/svg"
    ET.register_namespace("", namespace)
    background = ET.Element(
        f"{{{namespace}}}rect",
        {"width": "100%", "height": "100%", "fill": "white"},
    )
    tree.getroot().insert(0, background)
    tree.write(preview_path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    (MECHANICAL_DIR / "exports").mkdir(parents=True, exist_ok=True)
    (MECHANICAL_DIR / "previews").mkdir(parents=True, exist_ok=True)

    base = make_base(ENCLOSURE)
    lid = make_lid(ENCLOSURE)
    board = make_board(BOARD)
    assembly = make_review_assembly()

    export_shape(base, "enclosure-base", printable=True)
    export_shape(lid, "enclosure-lid", printable=True)
    export_shape(board, "reference-board")
    assembly.export(str(MECHANICAL_DIR / "exports" / "review-assembly.step"))

    export_svg(base, "base")
    export_svg(lid, "lid")
    preview_assembly = cq.Assembly(name="exploded-preview")
    preview_assembly.add(base, name="base")
    preview_assembly.add(
        board.translate((0, 0, ENCLOSURE.board_z)),
        name="PART-001-reference-board",
    )
    preview_assembly.add(
        lid.translate((0, 0, ENCLOSURE.base_height + 10.0)),
        name="exploded-lid",
    )
    export_svg(preview_assembly.toCompound(), "assembly")
    print("Generated mechanical exports and previews.")


if __name__ == "__main__":
    main()
