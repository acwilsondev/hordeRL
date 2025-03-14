from dataclasses import dataclass
from typing import Callable

from .control_mode_ability import ControlModeAbility
from ..brains.ability_actors.place_haunch_actor import \
    PlaceHaunchActor
from ...engine import palettes


@dataclass
class PlaceHaunchAbility(ControlModeAbility):
    ability_title: str = "Place Haunch"
    unlock_cost: int = 100
    use_cost: int = 15

    def get_mode(self) -> Callable:
        return PlaceHaunchActor

    def get_anim(self):
        return "α", palettes.MEAT
