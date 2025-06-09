# pyright: reportUnannotatedClassAttribute=false


from typing import Tuple


Direction = Tuple[
    int, int
]  # have to use Tuple instead of tuple for type hinting as `tuple[int, int]` throws


class DirectionTuple:
    N = (0, -1)  # North
    S = (0, 1)  # South
    E = (1, 0)  # East
    W = (-1, 0)  # West
    NE = (1, -1)  # North-East
    NW = (-1, -1)  # North-West
    SE = (1, 1)  # South-East
    SW = (-1, 1)  # South-West

    @staticmethod
    def to_string(direction: Direction) -> str:
        """Convert a direction tuple to a string representation."""
        if direction == DirectionTuple.N:
            return "N"
        elif direction == DirectionTuple.S:
            return "S"
        elif direction == DirectionTuple.E:
            return "E"
        elif direction == DirectionTuple.W:
            return "W"
        elif direction == DirectionTuple.NE:
            return "NE"
        elif direction == DirectionTuple.NW:
            return "NW"
        elif direction == DirectionTuple.SE:
            return "SE"
        elif direction == DirectionTuple.SW:
            return "SW"
        else:
            raise ValueError("Invalid direction")

    @staticmethod
    def parts(direction: tuple[int, int]) -> list[Direction]:
        """Break a direction into its constituent parts. E.g., NW contains N, W; so contains(NW) would return DirectionTuple.N, DirectionTuple.W."""
        parts = []
        if direction[0] < 0:
            parts.append(DirectionTuple.W)
        elif direction[0] > 0:
            parts.append(DirectionTuple.E)
        if direction[1] < 0:
            parts.append(DirectionTuple.N)
        elif direction[1] > 0:
            parts.append(DirectionTuple.S)
        return parts
