from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class SpawnSaplingInSpring(SeasonResetListener):
    """
    Data-only marker for spawning saplings in spring.
    """
