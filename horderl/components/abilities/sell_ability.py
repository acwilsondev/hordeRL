from dataclasses import dataclass

from horderl import palettes

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
    control_mode_key: str = "sell"
    anim_symbol: str = "$"
    anim_color: tuple = palettes.GOLD
