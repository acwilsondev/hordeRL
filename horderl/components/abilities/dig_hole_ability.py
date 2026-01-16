from dataclasses import dataclass
from typing import Callable

from horderl import palettes

from ..abilities.control_mode_ability import ControlModeAbility
from ..brains.ability_actors.dig_hole_actor import DigHoleActor


@dataclass
class DigHoleAbility(ControlModeAbility):
    """
    Describe the dig hole ability configuration.
    """

    ability_title: str = "Dig Hole"
    ability_title_key: str = "ability.dig_hole"
    unlock_cost: int = 100
    use_cost: int = 2
    mode_factory: Callable = DigHoleActor
    anim_symbol: str = "o"
    anim_color: tuple = palettes.DIRT
