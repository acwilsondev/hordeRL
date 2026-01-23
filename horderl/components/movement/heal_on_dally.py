from dataclasses import dataclass

from ..events.attack_started_events import AttackStartListener
from ..events.dally_event import DallyListener
from ..season_reset_listeners.seasonal_actor import SeasonResetListener


@dataclass
class HealOnDally(DallyListener, AttackStartListener, SeasonResetListener):
    """
    Data-only configuration for healing after repeated dally actions.
    """

    count: int = 0
    heal_count: int = 5
