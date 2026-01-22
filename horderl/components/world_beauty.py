from dataclasses import dataclass

from ..components.events.tree_cut_event import TreeCutListener
from ..components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class WorldBeauty(TreeCutListener, SeasonResetListener):
    """Track world beauty values affected by tree cutting."""

    trees_cut: int = 0
    spirits_wrath: int = 0
    spirits_attitude: int = 10
