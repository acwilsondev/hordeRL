from dataclasses import dataclass
from typing import Callable

from horderl import palettes

from ..abilities.control_mode_ability import ControlModeAbility
from ..brains.ability_actors.place_spikes_actor import PlaceSpikesActor


@dataclass
class BuildSpikesAbility(ControlModeAbility):
    """
    Describe the build spike trap ability configuration.
    """

    ability_title: str = "Build Spike Trap"
    ability_title_key: str = "ability.build_spikes"
    unlock_cost: int = 100
    use_cost: int = 5
    mode_factory: Callable = PlaceSpikesActor
    anim_symbol: str = "╨"
    anim_color: tuple = palettes.STONE
