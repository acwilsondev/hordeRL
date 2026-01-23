from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class CollectTaxesForKing(SeasonResetListener):
    """
    Data-only marker for collecting taxes for the king.
    """

    value: int = 25
