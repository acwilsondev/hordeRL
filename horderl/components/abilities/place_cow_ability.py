from dataclasses import dataclass
from typing import Callable

from horderl import palettes

from ..brains.ability_actors.place_cow_actor import PlaceCowActor
from .control_mode_ability import ControlModeAbility


@dataclass
class PlaceCowAbility(ControlModeAbility):
    """
    Describe the place cow ability configuration.
    """

    ability_title: str = "Place Cow"
    ability_title_key: str = "ability.place_cow"
    unlock_cost: int = 100
    use_cost: int = 100
    mode_factory: Callable = PlaceCowActor
    anim_symbol: str = "C"
    anim_color: tuple = palettes.WHITE
