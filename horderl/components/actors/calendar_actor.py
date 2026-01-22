from dataclasses import dataclass

from engine.components import EnergyActor


@dataclass
class Calendar(EnergyActor):
    """
    Actor component that tracks the passage of time.

    The actor system advances days and handles horde transitions.
    """

    day: int = 0
    season: int = 1
    year: int = 1217
    status: str = ""
    energy_cost: int = EnergyActor.DAILY
    round = 1
