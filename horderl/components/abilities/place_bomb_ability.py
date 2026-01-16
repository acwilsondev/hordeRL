from dataclasses import dataclass
from typing import Callable

from horderl import palettes

from ..brains.ability_actors.place_bomb_actor import PlaceBombActor
from .control_mode_ability import ControlModeAbility


@dataclass
class PlaceBombAbility(ControlModeAbility):
    """
    Describe the place bomb ability configuration.
    """

    ability_title: str = "Place Bomb"
    ability_title_key: str = "ability.place_bomb"
    unlock_cost: int = 100
    use_cost: int = 10
    mode_factory: Callable = PlaceBombActor
    anim_symbol: str = "δ"
    anim_color: tuple = palettes.STONE
