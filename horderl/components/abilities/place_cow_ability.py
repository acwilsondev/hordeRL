from dataclasses import dataclass

from horderl import palettes

from .control_mode_ability import ControlModeAbility


@dataclass
class PlaceCowAbility(ControlModeAbility):
    """
    Describe the place cow ability configuration.
    """

    ability_title: str = "Place Cow"
    ability_title_key: str = "ability.place_cow"
    unlock_cost: int = 100
    use_cost: int = 100
    control_mode_key: str = "place_cow"
    anim_symbol: str = "C"
    anim_color: tuple = palettes.WHITE
