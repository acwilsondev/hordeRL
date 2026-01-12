from dataclasses import dataclass
from typing import Callable

from horderl.engine import palettes

from ..brains.ability_actors.place_bomb_actor import PlaceBombActor
from .control_mode_ability import ControlModeAbility


@dataclass
class PlaceBombAbility(ControlModeAbility):
    ability_title: str = "Place Bomb"
    ability_title_key: str = "ability.place_bomb"
    unlock_cost: int = 100
    use_cost: int = 10

    def get_mode(self) -> Callable:
        return PlaceBombActor

    def get_anim(self):
        return "δ", palettes.STONE
