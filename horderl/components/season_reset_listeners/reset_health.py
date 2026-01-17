from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class ResetHealth(SeasonResetListener):
    """Data-only marker for resetting health on season reset."""
