from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class ExtractContractFees(SeasonResetListener):
    """Data-only marker for contract fee extraction on season reset."""
