from dataclasses import dataclass

from engine import constants
from engine.components import EnergyActor
from horderl.components.brains.brain import Brain


@dataclass
class LookCursorController(Brain):
    """
    Brain that moves a cursor for look interactions.

    Input handling is implemented by the brain system.
    """

    energy_cost: int = EnergyActor.INSTANT
    cursor: int = constants.INVALID
