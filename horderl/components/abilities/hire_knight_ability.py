from dataclasses import dataclass

from horderl import palettes

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
    control_mode_key: str = "hire_knight"
    anim_symbol: str = "K"
    anim_color: tuple = palettes.STONE
