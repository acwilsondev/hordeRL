from dataclasses import dataclass
from typing import Callable

from .control_mode_ability import ControlModeAbility
from ..brains.ability_actors.place_cow_actor import PlaceCowActor
from horderl.engine import palettes


@dataclass
class PlaceCowAbility(ControlModeAbility):
    ability_title: str = "Place Cow"
    unlock_cost: int = 100
    use_cost: int = 100

    def get_mode(self) -> Callable:
        return PlaceCowActor

    def get_anim(self):
        return "C", palettes.WHITE
