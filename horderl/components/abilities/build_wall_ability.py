from dataclasses import dataclass
from typing import Callable

from ..abilities.control_mode_ability import ControlModeAbility
from ..brains.ability_actors.place_stone_wall_actor import PlaceStoneWallActor
from horderl.engine import palettes


@dataclass
class BuildWallAbility(ControlModeAbility):
    ability_title: str = "Build Wall"
    unlock_cost: int = 100
    use_cost: int = 10

    def get_mode(self) -> Callable:
        return PlaceStoneWallActor

    def get_anim(self):
        return "o", palettes.STONE
