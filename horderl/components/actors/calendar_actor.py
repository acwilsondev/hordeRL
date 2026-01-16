from dataclasses import dataclass

from engine.components import EnergyActor
from horderl.i18n import t


@dataclass
class Calendar(EnergyActor):
    """
    Actor component that tracks the passage of time.

    The actor system advances days and handles horde transitions.
    """

    day: int = 0
    season: int = 1
    year: int = 1217
    status: str = "Peacetime"
    energy_cost: int = EnergyActor.DAILY
    round = 1

    def __post_init__(self) -> None:
        self.status = t("status.peacetime")
