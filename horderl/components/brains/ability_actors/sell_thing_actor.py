from dataclasses import dataclass

from engine.components import EnergyActor
from horderl.components.brains.brain import Brain


@dataclass
class SellThingActor(Brain):
    """
    Brain for selling adjacent sellable entities.

    Input handling is delegated to the brain system.
    """

    energy_cost: int = EnergyActor.INSTANT
