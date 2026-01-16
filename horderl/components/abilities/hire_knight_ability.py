from dataclasses import dataclass
from typing import Callable

from horderl import palettes

from ..brains.ability_actors.hire_knight_brain import HireKnightActor
from .control_mode_ability import ControlModeAbility


@dataclass
class HireKnightAbility(ControlModeAbility):
    """
    Describe the hire knight ability configuration.
    """

    ability_title: str = "Place Knight"
    ability_title_key: str = "ability.place_knight"
    unlock_cost: int = 250
    use_cost: int = 100
    mode_factory: Callable = HireKnightActor
    anim_symbol: str = "K"
    anim_color: tuple = palettes.STONE
