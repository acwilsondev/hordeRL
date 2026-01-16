from dataclasses import dataclass
from typing import Callable

from horderl import palettes

from ..brains.ability_actors.sell_thing_actor import SellThingActor
from .control_mode_ability import ControlModeAbility


@dataclass
class SellAbility(ControlModeAbility):
    """
    Describe the sell things ability configuration.
    """

    ability_title: str = "Sell Things"
    ability_title_key: str = "ability.sell"
    unlock_cost: int = 0
    use_cost: int = 0
    mode_factory: Callable = SellThingActor
    anim_symbol: str = "$"
    anim_color: tuple = palettes.GOLD
