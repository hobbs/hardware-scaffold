"""Named dimensions for the starter assembly, in millimetres."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BoardSpec:
    """Simplified PART-001 proxy; replace from an authoritative drawing."""

    length: float = 50.0
    width: float = 30.0
    thickness: float = 1.6
    component_height: float = 8.0
    hole_spacing_x: float = 42.0
    hole_spacing_y: float = 22.0
    mounting_hole_diameter: float = 3.0
    connector_length: float = 8.0
    connector_width: float = 9.0
    connector_height: float = 3.2
    connector_insertion: float = 12.0

    @property
    def mounting_points(self) -> tuple[tuple[float, float], ...]:
        x = self.hole_spacing_x / 2
        y = self.hole_spacing_y / 2
        return ((-x, -y), (-x, y), (x, -y), (x, y))


@dataclass(frozen=True)
class EnclosureSpec:
    """Process-dependent starter dimensions; calibrate before fabrication."""

    board: BoardSpec = field(default_factory=BoardSpec)
    clearance_xy: float = 1.0
    headroom: float = 2.0
    wall: float = 2.0
    floor: float = 2.0
    standoff_height: float = 4.0
    standoff_diameter: float = 6.0
    screw_clearance_diameter: float = 2.7
    lid_thickness: float = 2.0
    lid_fit_clearance: float = 0.35
    lid_lip_depth: float = 2.0
    lid_lip_wall: float = 1.2
    port_clearance: float = 0.6

    @property
    def inner_length(self) -> float:
        return self.board.length + 2 * self.clearance_xy

    @property
    def inner_width(self) -> float:
        return self.board.width + 2 * self.clearance_xy

    @property
    def inner_height(self) -> float:
        return (
            self.standoff_height
            + self.board.thickness
            + self.board.component_height
            + self.headroom
        )

    @property
    def outer_length(self) -> float:
        return self.inner_length + 2 * self.wall

    @property
    def outer_width(self) -> float:
        return self.inner_width + 2 * self.wall

    @property
    def base_height(self) -> float:
        return self.floor + self.inner_height

    @property
    def board_z(self) -> float:
        return self.floor + self.standoff_height


BOARD = BoardSpec()
ENCLOSURE = EnclosureSpec(board=BOARD)
