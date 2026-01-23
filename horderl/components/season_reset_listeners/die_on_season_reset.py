from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class DieOnSeasonReset(SeasonResetListener):
    """Data-only marker for death triggered on season reset."""
