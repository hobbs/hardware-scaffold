import pytest

from project.components.reference_board import make_board
from project.enclosure import make_base, make_lid
from project.parameters import BOARD, ENCLOSURE


def test_base_matches_named_outer_envelope() -> None:
    bounds = make_base(ENCLOSURE).val().BoundingBox()
    assert bounds.xlen == pytest.approx(ENCLOSURE.outer_length)
    assert bounds.ylen == pytest.approx(ENCLOSURE.outer_width)
    assert bounds.zlen == pytest.approx(ENCLOSURE.base_height)


def test_board_proxy_matches_drawing_envelope() -> None:
    bounds = make_board(BOARD).val().BoundingBox()
    assert bounds.xlen == pytest.approx(BOARD.length + BOARD.connector_length / 2)
    assert bounds.ylen == pytest.approx(BOARD.width)
    assert bounds.zmin == pytest.approx(0.0)
    assert bounds.zmax == pytest.approx(BOARD.thickness + BOARD.component_height)


def test_enclosure_has_declared_board_clearance() -> None:
    base = make_base(ENCLOSURE).val()
    board = make_board(BOARD).translate((0, 0, ENCLOSURE.board_z)).val()
    lid = make_lid(ENCLOSURE).translate((0, 0, ENCLOSURE.base_height)).val()
    # Board/standoff contact is intentional; penetration through a wall,
    # standoff, port edge, or lid is not. Work in assembled coordinates.
    volume_tolerance_mm3 = 1e-6
    assert board.intersect(base).Volume() < volume_tolerance_mm3
    assert board.intersect(lid).Volume() < volume_tolerance_mm3


def test_lid_lip_is_smaller_than_cavity() -> None:
    base = make_base(ENCLOSURE).val()
    lid = make_lid(ENCLOSURE)
    # Exercise the available lateral fit, not just the outer plate's bounds.
    # Moving by the declared fit clearance may touch, but must not penetrate.
    volume_tolerance_mm3 = 1e-6
    for dx, dy in (
        (ENCLOSURE.lid_fit_clearance, 0),
        (-ENCLOSURE.lid_fit_clearance, 0),
        (0, ENCLOSURE.lid_fit_clearance),
        (0, -ENCLOSURE.lid_fit_clearance),
    ):
        placed = lid.translate((dx, dy, ENCLOSURE.base_height)).val()
        assert placed.intersect(base).Volume() < volume_tolerance_mm3
