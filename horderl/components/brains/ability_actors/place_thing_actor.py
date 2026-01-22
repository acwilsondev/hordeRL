from dataclasses import dataclass

from engine import constants
from engine.components import EnergyActor
from horderl.components.brains.brain import Brain


@dataclass
class PlaceThingActor(Brain):
    """
    Brain for placing buildable objects adjacent to the player.

    Input handling is delegated to the brain system.
    """

    energy_cost: int = EnergyActor.INSTANT
    gold_cost: int = constants.INVALID
    spawn_key: str = ""
