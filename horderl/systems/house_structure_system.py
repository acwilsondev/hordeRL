from typing import List

from engine.types import EntityId
from horderl.components.house_structure import HouseStructure


def get_house_structure_tiles(
    house_structure: HouseStructure,
) -> List[EntityId]:
    """
    Assemble the ordered list of tile entities for a house structure.

    Args:
        house_structure: HouseStructure component describing the tile entities.

    Returns:
        List[EntityId]: Ordered tile entity identifiers for the structure.
    """
    return [
        house_structure.upper_left,
        house_structure.upper_middle,
        house_structure.upper_right,
        house_structure.middle_left,
        house_structure.middle_right,
        house_structure.bottom_left,
        house_structure.bottom_middle,
        house_structure.bottom_right,
    ]
