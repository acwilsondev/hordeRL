from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine import constants
from engine.components import EnergyActor
from horderl.components.brains.brain import Brain


@dataclass
class PainterBrain(Brain, ABC):
    """
    Provide a base class for debug object placing controllers.
    """

    energy_cost: int = EnergyActor.INSTANT
    cursor: int = constants.INVALID

    @abstractmethod
    def paint_one(self, scene, position):
        pass
