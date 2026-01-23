from dataclasses import dataclass

from horderl import palettes

from ..abilities.control_mode_ability import ControlModeAbility


@dataclass
class DigHoleAbility(ControlModeAbility):
    """
    Describe the dig hole ability configuration.
    """

    ability_title: str = "Dig Hole"
    ability_title_key: str = "ability.dig_hole"
    unlock_cost: int = 100
    use_cost: int = 2
    control_mode_key: str = "dig_hole"
    anim_symbol: str = "o"
    anim_color: tuple = palettes.DIRT
