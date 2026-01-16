from dataclasses import dataclass

from horderl import palettes

from ..abilities.control_mode_ability import ControlModeAbility


@dataclass
class BuildWallAbility(ControlModeAbility):
    """
    Describe the build wall ability configuration.
    """

    ability_title: str = "Build Wall"
    ability_title_key: str = "ability.build_wall"
    unlock_cost: int = 100
    use_cost: int = 10
    control_mode_key: str = "place_stone_wall"
    anim_symbol: str = "o"
    anim_color: tuple = palettes.STONE
