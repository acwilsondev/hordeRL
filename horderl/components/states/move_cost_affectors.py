from dataclasses import dataclass
from enum import Enum

from engine.components.component import Component


class MoveCostAffectorType(Enum):
    """
    Represent categories of movement cost or speed modifiers.
    """

    HINDERED = "hindered"
    DIFFICULT_TERRAIN = "difficult_terrain"
    HASTE = "haste"
    EASY_TERRAIN = "easy_terrain"


@dataclass(kw_only=True)
class MoveCostAffector(Component):
    """
    Store a movement cost modifier for an entity or terrain tile.
    """

    affector_type: MoveCostAffectorType
