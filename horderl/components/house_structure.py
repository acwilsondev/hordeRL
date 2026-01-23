from dataclasses import dataclass

from engine.components.component import Component
from engine.types import EntityId


@dataclass
class HouseStructure(Component):
    """Track the entity tiles that make up a house structure."""

    house_id: EntityId = 0
    upgrade_level: int = 0
    is_destroyed: bool = False
    upper_left: EntityId = 0
    upper_middle: EntityId = 0
    upper_right: EntityId = 0
    middle_left: EntityId = 0
    middle_right: EntityId = 0
    bottom_left: EntityId = 0
    bottom_middle: EntityId = 0
    bottom_right: EntityId = 0
