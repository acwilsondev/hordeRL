from dataclasses import dataclass

from engine.components import EnergyActor
from horderl.components.brains.brain import Brain


@dataclass
class DigHoleActor(Brain):
    """
    Brain for digging holes and removing diggable entities.

    Logic is delegated to the brain system.
    """

    energy_cost: int = EnergyActor.INSTANT
