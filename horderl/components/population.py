from dataclasses import dataclass

from ..components.events.peasant_events import (
    PeasantAddedListener,
    PeasantDiedListener,
)


@dataclass
class Population(PeasantAddedListener, PeasantDiedListener):
    """Track the current population count."""

    population: int = 0
