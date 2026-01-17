from dataclasses import dataclass

from engine.components import EnergyActor

from ..events.attack_started_events import AttackStartListener
from ..season_reset_listeners.seasonal_actor import SeasonResetListener


@dataclass
class FreezeWater(EnergyActor, AttackStartListener, SeasonResetListener):
    """
    Data-only marker for freezing/thawing water based on weather state.

    This component stores timing configuration and is interpreted by
    ``horderl.systems.weather_system``.
    """

    energy_cost: int = EnergyActor.HALF_HOUR
