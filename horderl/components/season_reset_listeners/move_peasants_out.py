from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class MovePeasantsOut(SeasonResetListener):
    """Data-only marker for moving peasants out on season reset."""
