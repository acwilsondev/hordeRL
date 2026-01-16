from dataclasses import dataclass

from engine.components import EnergyActor
from horderl.components.brains.brain import Brain


@dataclass
class SleepingBrain(Brain):
    """
    Brain that sleeps for a fixed number of turns.

    Responsible for consuming turns, spawning sleep animation, and transitioning
    back to the previous brain when the sleep counter expires.
    """

    turns: int = 3
    energy_cost: int = EnergyActor.HOURLY
