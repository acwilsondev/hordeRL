from dataclasses import dataclass

from horderl import palettes

from ..abilities.control_mode_ability import ControlModeAbility


@dataclass
class BuildSpikesAbility(ControlModeAbility):
    """
    Describe the build spike trap ability configuration.
    """

    ability_title: str = "Build Spike Trap"
    ability_title_key: str = "ability.build_spikes"
    unlock_cost: int = 100
    use_cost: int = 5
    control_mode_key: str = "place_spikes"
    anim_symbol: str = "╨"
    anim_color: tuple = palettes.STONE
