from dataclasses import dataclass

from engine import constants
from engine.components.component import Component


@dataclass
class ScheduleRebuild(Component):
    """
    When this wall dies, set a delayed trigger to attempt to rebuild at the season
    reset.
    """

    root: int = constants.INVALID
