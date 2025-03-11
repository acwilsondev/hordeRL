from dataclasses import dataclass
from typing import Callable

from .control_mode_ability import ControlModeAbility
from ..brains.fast_forward_actor import FastForwardBrain
from ...engine import palettes


@dataclass
class FastForwardAbility(ControlModeAbility):
    ability_title: str = "Fast Forward"
    unlock_cost: int = 0
    use_cost: int = 0

    def get_mode(self) -> Callable:
        return FastForwardBrain

    def get_anim(self):
        return ">", palettes.LIGHT_WATER
