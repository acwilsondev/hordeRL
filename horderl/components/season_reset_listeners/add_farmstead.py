from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class AddFarmstead(SeasonResetListener):
    """Data-only marker for adding farmsteads on season reset."""
