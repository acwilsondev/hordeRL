from dataclasses import dataclass
from enum import Enum, auto

from engine.components.component import Component


class CostMapperType(Enum):
    """Define the available pathfinding cost mapping strategies."""

    NORMAL = auto()
    STEALTHY = auto()
    PEASANT = auto()
    ROAD = auto()
    SIMPLEX = auto()
    STRAIGHT_LINE = auto()


@dataclass
class CostMapper(Component):
    """
    Data-only component for pathfinding cost mapping configuration.

    Systems interpret the mapper type to build cost grids.
    """

    mapper_type: CostMapperType = CostMapperType.NORMAL
