from dataclasses import dataclass
from typing import Callable

from horderl import palettes

from ..abilities.control_mode_ability import ControlModeAbility
from ..brains.ability_actors.place_fence_actor import PlaceFenceActor


@dataclass
class BuildFenceAbility(ControlModeAbility):
    """
    Describe the build fence ability configuration.
    """

    ability_title: str = "Build Fence"
    ability_title_key: str = "ability.build_fence"
    unlock_cost: int = 100
    use_cost: int = 5
    mode_factory: Callable = PlaceFenceActor
    anim_symbol: str = "o"
    anim_color: tuple = palettes.WOOD
