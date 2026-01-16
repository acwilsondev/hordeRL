from dataclasses import dataclass
from typing import Callable

from horderl import palettes

from ..brains.fast_forward_actor import FastForwardBrain
from .control_mode_ability import ControlModeAbility


@dataclass
class FastForwardAbility(ControlModeAbility):
    """
    Describe the fast-forward ability configuration.
    """

    ability_title: str = "Fast Forward"
    ability_title_key: str = "ability.fast_forward"
    unlock_cost: int = 0
    use_cost: int = 0
    mode_factory: Callable = FastForwardBrain
    anim_symbol: str = ">"
    anim_color: tuple = palettes.LIGHT_WATER
