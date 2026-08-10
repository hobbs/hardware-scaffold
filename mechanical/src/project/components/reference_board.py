"""Generic development-board proxy used only to demonstrate the workflow.

Origin: XY center of the PCB at its bottom face. +Z points toward components and
+X points through the primary connector.
"""

import cadquery as cq

from project.parameters import BoardSpec


def make_board(spec: BoardSpec) -> cq.Workplane:
    pcb = cq.Workplane("XY").box(
        spec.length,
        spec.width,
        spec.thickness,
        centered=(True, True, False),
    )
    holes = (
        cq.Workplane("XY")
        .pushPoints(spec.mounting_points)
        .circle(spec.mounting_hole_diameter / 2)
        .extrude(spec.thickness)
    )
    pcb = pcb.cut(holes)

    components = (
        cq.Workplane("XY")
        .workplane(offset=spec.thickness)
        .box(
            spec.length - 8.0,
            spec.width - 6.0,
            spec.component_height,
            centered=(True, True, False),
        )
    )
    connector = (
        cq.Workplane("XY")
        .workplane(offset=spec.thickness)
        .box(
            spec.connector_length,
            spec.connector_width,
            spec.connector_height,
            centered=(True, True, False),
        )
        .translate((spec.length / 2, 0, 0))
    )
    return pcb.union(components).union(connector)


def make_connector_keepout(spec: BoardSpec) -> cq.Workplane:
    """Volume that must remain open for plug insertion and cable handling."""

    return (
        cq.Workplane("XY")
        .workplane(offset=spec.thickness)
        .box(
            spec.connector_insertion + spec.connector_length / 2,
            spec.connector_width + 4.0,
            spec.connector_height + 3.0,
            centered=(False, True, False),
        )
        .translate((spec.length / 2, 0, 0))
    )
