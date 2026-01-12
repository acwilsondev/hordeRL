from dataclasses import dataclass
from typing import Callable

from horderl.engine import palettes

from ..brains.ability_actors.hire_knight_brain import HireKnightActor
from .control_mode_ability import ControlModeAbility


@dataclass
class HireKnightAbility(ControlModeAbility):
    ability_title: str = "Place Knight"
    ability_title_key: str = "ability.place_knight"
    unlock_cost: int = 250
    use_cost: int = 100

    def get_mode(self) -> Callable:
        return HireKnightActor

    def get_anim(self):
        return "K", palettes.STONE
