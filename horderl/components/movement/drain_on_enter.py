from dataclasses import dataclass

from ..events.step_event import EnterListener


@dataclass
class DrainOnEnter(EnterListener):
    """
    Data-only configuration for dealing damage when stepped on.
    """

    damage: int = 0
