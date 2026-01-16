from dataclasses import dataclass
from enum import Enum

from engine.components import EnergyActor
from horderl.components.brains.brain import Brain


@dataclass
class PeasantActor(Brain):
    """
    Brain controlling peasant movement and idle behavior.

    Responsible for deciding between farming, wandering, or idling based on
    internal state and available pathing information.
    """

    class State(str, Enum):
        """
        Possible behavior modes for the peasant brain.
        """

        UNKNOWN = "UNKNOWN"
        FARMING = "FARMING"
        HIDING = "HIDING"
        WANDERING = "WANDERING"

    state: State = State.UNKNOWN
    can_animate: bool = True
    energy_cost: int = EnergyActor.HOURLY
