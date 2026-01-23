from dataclasses import dataclass

from horderl import palettes

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
    control_mode_key: str = "fast_forward"
    anim_symbol: str = ">"
    anim_color: tuple = palettes.LIGHT_WATER
