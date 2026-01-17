from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class GrowGrass(SeasonResetListener):
    """Data-only marker for grass growth on season reset."""
