from dataclasses import dataclass

from engine.components import EnergyActor


@dataclass
class SnowFall(EnergyActor):
    """
    Data-only marker for snowfall and grass growth based on weather state.

    This component stores timing configuration and is interpreted by
    ``horderl.systems.weather_system``.
    """

    energy_cost: int = EnergyActor.HALF_HOUR
