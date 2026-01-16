from dataclasses import dataclass

from horderl import palettes

from .control_mode_ability import ControlModeAbility


@dataclass
class PlaceHaunchAbility(ControlModeAbility):
    """
    Describe the place haunch ability configuration.
    """

    ability_title: str = "Place Haunch"
    ability_title_key: str = "ability.place_haunch"
    unlock_cost: int = 100
    use_cost: int = 15
    control_mode_key: str = "place_haunch"
    anim_symbol: str = "α"
    anim_color: tuple = palettes.MEAT
