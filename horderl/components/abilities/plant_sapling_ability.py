from dataclasses import dataclass
from typing import Callable

from horderl import palettes
from horderl.components.abilities.control_mode_ability import (
    ControlModeAbility,
)
from horderl.components.brains.ability_actors.plant_sapling_actor import (
    PlaceSaplingActor,
)


@dataclass
class PlantSaplingAbility(ControlModeAbility):
    """
    Describe the plant sapling ability configuration.
    """

    ability_title: str = "Plant Saplings"
    ability_title_key: str = "ability.plant_saplings"
    unlock_cost: int = 100
    use_cost: int = 1
    mode_factory: Callable = PlaceSaplingActor
    anim_symbol: str = "+"
    anim_color: tuple = palettes.FOILAGE_C
