from dataclasses import dataclass

from engine.components import EnergyActor


@dataclass
class FastForward(EnergyActor):
    """
    Event actor that advances the calendar to a fixed day.

    This component fast-forwards the game calendar and triggers a new day event.
    """

    energy_cost: int = EnergyActor.INSTANT
