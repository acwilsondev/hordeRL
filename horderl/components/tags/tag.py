from dataclasses import dataclass
from enum import Enum

from engine.components.component import Component


class TagType(str, Enum):
    """Enumerate identity tags that categorize entities."""

    NONE = "none"
    HORDELING = "hordeling"
    PEASANT = "peasant"
    TREE = "tree"
    FARM = "farm"
    CORPSE = "corpse"
    WATER = "water"
    ICE = "ice"


@dataclass
class Tag(Component):
    """Represent a categorical tag assigned to an entity."""

    tag_type: TagType = TagType.NONE
