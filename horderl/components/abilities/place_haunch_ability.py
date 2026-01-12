from dataclasses import dataclass
from typing import Callable

from horderl.engine import palettes

from ..brains.ability_actors.place_haunch_actor import PlaceHaunchActor
from .control_mode_ability import ControlModeAbility


@dataclass
class PlaceHaunchAbility(ControlModeAbility):
    ability_title: str = "Place Haunch"
    ability_title_key: str = "ability.place_haunch"
    unlock_cost: int = 100
    use_cost: int = 15

    def get_mode(self) -> Callable:
        return PlaceHaunchActor

    def get_anim(self):
        return "α", palettes.MEAT
