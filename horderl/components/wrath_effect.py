from dataclasses import dataclass

from engine.components import EnergyActor


@dataclass
class WrathEffect(EnergyActor):
    """
    Trigger a wrathful purge that removes hordelings and spawners.
    """

    energy_cost: int = EnergyActor.INSTANT
