from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class SaveOnSeasonReset(SeasonResetListener):
    """
    Data-only marker for autosaving on season reset.
    """
