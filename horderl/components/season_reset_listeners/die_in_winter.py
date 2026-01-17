from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class CropsDieInWinter(SeasonResetListener):
    """Data-only marker for crops that die in winter."""
