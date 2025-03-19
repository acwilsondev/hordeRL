"""
Crops Module.

This module handles crop entities in the game, which are valuable resources that farmers
grow and players must protect from hordelings. Crops have monetary value and can be
harvested at the end of the season for gold.

Crops are part of the agricultural system and represent one of the main economic
elements that players need to protect to succeed.

"""

from typing import List, Tuple

from horderl.components import (
    Appearance,
    Attributes,
    Coordinates,
    target_value,
)
from horderl.components.death_listeners.npc_corpse import Corpse
from horderl.components.edible import Edible
from horderl.components.faction import Faction
from horderl.components.relationships.farmed_by import FarmedBy
from horderl.components.tags.crop_info import CropInfo
from horderl.components.target_value import TargetValue
from horderl.components.tax_value import TaxValue
from horderl.engine import core, palettes
from horderl.engine.components.component import Component
from horderl.engine.components.entity import Entity
from horderl.engine.constants import PRIORITY_LOW

crops_description = (
    "A valuable crop. They're easy pickens for the hordelings, but they will"
    " sell for 5 gold at the end of the season- if you protect them."
)


def make_crops(
    x, y, farmer, field_id, color=palettes.FIRE
) -> Tuple[int, List[Component]]:
    """
    Creates a crop entity at the specified location.

    Crops are valuable agricultural resources that can be sold for gold at the end of
    the season if protected from hordelings. Each crop has 3 HP and belongs to the
    peasant faction. Crops are edible entities that can be consumed by hordelings.

    Parameters:
        x (int): The x-coordinate where the crop will be placed
        y (int): The y-coordinate where the crop will be placed
        farmer (int): The entity ID of the farmer who owns/tends this crop
        field_id (int): The ID of the field this crop belongs to
        color (tuple, optional): RGB color tuple for the crop's appearance.
                                Default is palettes.FIRE

    Returns:
        Tuple[int, List[Component]]: A tuple containing:
            - The entity ID of the created crop
            - A list of components that make up the crop entity

    """
    entity_id = core.get_id()
    components: List[Component] = [
        Entity(
            id=entity_id,
            entity=entity_id,
            name="crop",
            description=crops_description,
        ),
        Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_LOW),
        Appearance(
            entity=entity_id,
            symbol="δ",
            color=color,
            bg_color=palettes.BACKGROUND,
        ),
        FarmedBy(entity=entity_id, farmer=farmer),
        CropInfo(entity=entity_id, field_id=field_id, farmer_id=farmer),
        TaxValue(entity=entity_id, value=TaxValue.CROPS),
        TargetValue(entity=entity_id, value=target_value.CROPS),
        Faction(entity=entity_id, faction=Faction.Options.PEASANT),
        Attributes(entity=entity_id, hp=3, max_hp=3),
        Edible(entity=entity_id, sleep_for=10),
        Corpse(entity=entity_id, color=color),
    ]
    return entity_id, components
