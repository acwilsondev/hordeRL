from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class Rebuilder(SeasonResetListener):
    """
    Data-only marker for rebuilding houses on season reset.
    """
