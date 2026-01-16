from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

from engine import constants
from engine.components import EnergyActor
from engine.components.component import Component
from horderl.components.brains.brain import Brain


@dataclass
class PlaceThingActor(Brain, ABC):
    """
    Brain for placing buildable objects adjacent to the player.

    Input handling is delegated to the brain system.
    """

    energy_cost: int = EnergyActor.INSTANT
    gold_cost: int = constants.INVALID

    @abstractmethod
    def make_thing(self, x: int, y: int) -> Tuple[int, List[Component]]:
        raise NotImplementedError()
