"""Parametric starter enclosure parts."""

import cadquery as cq

from project.parameters import EnclosureSpec


def make_base(spec: EnclosureSpec) -> cq.Workplane:
    outer = cq.Workplane("XY").box(
        spec.outer_length,
        spec.outer_width,
        spec.base_height,
        centered=(True, True, False),
    )
    cavity = (
        cq.Workplane("XY")
        .workplane(offset=spec.floor)
        .box(
            spec.inner_length,
            spec.inner_width,
            spec.inner_height + 0.1,
            centered=(True, True, False),
        )
    )
    base = outer.cut(cavity)

    standoffs = (
        cq.Workplane("XY")
        .workplane(offset=spec.floor)
        .pushPoints(spec.board.mounting_points)
        .circle(spec.standoff_diameter / 2)
        .extrude(spec.standoff_height)
    )
    base = base.union(standoffs)

    pilot_holes = (
        cq.Workplane("XY")
        .workplane(offset=spec.floor)
        .pushPoints(spec.board.mounting_points)
        .circle(spec.screw_clearance_diameter / 2)
        .extrude(spec.standoff_height + 0.2)
    )
    base = base.cut(pilot_holes)

    port = (
        cq.Workplane("XY")
        .workplane(offset=spec.board_z + spec.board.thickness - spec.port_clearance)
        .box(
            spec.wall + 2.0,
            spec.board.connector_width + 2 * spec.port_clearance,
            spec.board.connector_height + 2 * spec.port_clearance,
            centered=(True, True, False),
        )
        .translate((spec.outer_length / 2 - spec.wall / 2, 0, 0))
    )
    return base.cut(port)


def make_lid(spec: EnclosureSpec) -> cq.Workplane:
    plate = cq.Workplane("XY").box(
        spec.outer_length,
        spec.outer_width,
        spec.lid_thickness,
        centered=(True, True, False),
    )

    lip_length = spec.inner_length - 2 * spec.lid_fit_clearance
    lip_width = spec.inner_width - 2 * spec.lid_fit_clearance
    lip_outer = (
        cq.Workplane("XY")
        .workplane(offset=-spec.lid_lip_depth)
        .box(
            lip_length,
            lip_width,
            spec.lid_lip_depth,
            centered=(True, True, False),
        )
    )
    lip_inner = (
        cq.Workplane("XY")
        .workplane(offset=-spec.lid_lip_depth - 0.05)
        .box(
            lip_length - 2 * spec.lid_lip_wall,
            lip_width - 2 * spec.lid_lip_wall,
            spec.lid_lip_depth + 0.1,
            centered=(True, True, False),
        )
    )
    return plate.union(lip_outer.cut(lip_inner))
