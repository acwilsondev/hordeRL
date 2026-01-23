from dataclasses import dataclass

from engine.components import EnergyActor


@dataclass
class HordelingSpawner(EnergyActor):
    """
    Hordelings will spawn at this object's location.
    """

    energy_cost: int = EnergyActor.HOURLY
    waves: int = 1
