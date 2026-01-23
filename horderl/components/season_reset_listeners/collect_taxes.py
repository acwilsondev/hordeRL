from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class CollectTaxes(SeasonResetListener):
    """Data-only marker for collecting taxes on season reset."""
