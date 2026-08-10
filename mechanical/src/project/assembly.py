"""Review assembly with separately colored manufactured and reference objects."""

import cadquery as cq

from project.components.reference_board import make_board, make_connector_keepout
from project.enclosure import make_base, make_lid
from project.parameters import BOARD, ENCLOSURE, BoardSpec, EnclosureSpec


def make_review_assembly(
    board_spec: BoardSpec = BOARD,
    enclosure_spec: EnclosureSpec = ENCLOSURE,
) -> cq.Assembly:
    assembly = cq.Assembly(name="review-assembly")
    assembly.add(
        make_base(enclosure_spec),
        name="enclosure-base",
        color=cq.Color(0.75, 0.75, 0.78),
    )
    assembly.add(
        make_lid(enclosure_spec),
        name="enclosure-lid",
        loc=cq.Location(cq.Vector(0, 0, enclosure_spec.base_height)),
        color=cq.Color(0.55, 0.58, 0.62),
    )
    board_location = cq.Location(cq.Vector(0, 0, enclosure_spec.board_z))
    assembly.add(
        make_board(board_spec),
        name="PART-001-reference-board",
        loc=board_location,
        color=cq.Color(0.08, 0.45, 0.18),
    )
    assembly.add(
        make_connector_keepout(board_spec),
        name="connector-insertion-keepout",
        loc=board_location,
        color=cq.Color(0.9, 0.25, 0.1, 0.35),
    )
    return assembly
