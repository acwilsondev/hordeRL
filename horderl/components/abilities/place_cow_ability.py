from dataclasses import dataclass
from typing import Callable

from horderl import palettes

from ..brains.ability_actors.place_cow_actor import PlaceCowActor
from .control_mode_ability import ControlModeAbility


@dataclass
class PlaceCowAbility(ControlModeAbility):
    ability_title: str = "Place Cow"
    ability_title_key: str = "ability.place_cow"
    unlock_cost: int = 100
    use_cost: int = 100

    def get_mode(self) -> Callable:
        return PlaceCowActor

    def get_anim(self):
        return "C", palettes.WHITE
