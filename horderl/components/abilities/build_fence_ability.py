from dataclasses import dataclass

from horderl import palettes

from ..abilities.control_mode_ability import ControlModeAbility


@dataclass
class BuildFenceAbility(ControlModeAbility):
    """
    Describe the build fence ability configuration.
    """

    ability_title: str = "Build Fence"
    ability_title_key: str = "ability.build_fence"
    unlock_cost: int = 100
    use_cost: int = 5
    control_mode_key: str = "place_fence"
    anim_symbol: str = "o"
    anim_color: tuple = palettes.WOOD
