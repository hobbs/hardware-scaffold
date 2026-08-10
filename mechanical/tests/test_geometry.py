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
    assert ENCLOSURE.inner_length - BOARD.length == pytest.approx(
        2 * ENCLOSURE.clearance_xy
    )
    assert ENCLOSURE.inner_width - BOARD.width == pytest.approx(
        2 * ENCLOSURE.clearance_xy
    )


def test_lid_lip_is_smaller_than_cavity() -> None:
    bounds = make_lid(ENCLOSURE).val().BoundingBox()
    assert bounds.xlen == pytest.approx(ENCLOSURE.outer_length)
    assert bounds.ylen == pytest.approx(ENCLOSURE.outer_width)
    assert bounds.zmin == pytest.approx(-ENCLOSURE.lid_lip_depth)
    assert bounds.zmax == pytest.approx(ENCLOSURE.lid_thickness)
    assert 2 * ENCLOSURE.lid_fit_clearance > 0
