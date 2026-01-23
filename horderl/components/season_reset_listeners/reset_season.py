from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class ResetSeason(Component):
    """
    Event signaling a transition to a new season.
    """

    # Season we're entering
    season: str = "None"
