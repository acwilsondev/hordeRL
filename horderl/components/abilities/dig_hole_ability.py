from dataclasses import dataclass
from typing import Callable

from ..abilities.control_mode_ability import ControlModeAbility
from ..brains.ability_actors.dig_hole_actor import DigHoleActor
from horderl.engine import palettes


@dataclass
class DigHoleAbility(ControlModeAbility):
    ability_title: str = "Dig Hole"
    unlock_cost: int = 100
    use_cost: int = 2

    def get_mode(self) -> Callable:
        return DigHoleActor

    def get_anim(self):
        return "o", palettes.DIRT
