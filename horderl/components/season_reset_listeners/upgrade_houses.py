from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class UpgradeHouse(SeasonResetListener):
    """Data-only marker for upgrading houses on season reset."""
