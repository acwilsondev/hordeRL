from dataclasses import dataclass
from typing import List

from horderl.components import Attributes
from horderl.components.season_reset_listeners.seasonal_actor import SeasonResetListener


@dataclass
class ResetHealth(SeasonResetListener):
    def on_season_reset(self, scene, season):
        scene.message("You rest and your wounds heal.")
        healths: List[Attributes] = scene.cm.get(Attributes)
        for health in healths:
            health.hp = health.max_hp
