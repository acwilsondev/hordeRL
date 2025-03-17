from dataclasses import dataclass

from ..components.events.tree_cut_event import TreeCutListener
from ..components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)
from ..components.world_building.world_parameters import WorldParameters
from ..engine import core, palettes


@dataclass
class WorldBeauty(TreeCutListener, SeasonResetListener):
    trees_cut: int = 0
    spirits_wrath: int = 0
    spirits_attitude: int = 10

    def on_tree_cut(self, scene):
        self._log_info(f"detected tree cut")
        self.trees_cut += 1
        if not self.trees_cut % self.spirits_attitude:
            scene.message(
                "The spirits grow angrier with your cutting.",
                color=palettes.BLOOD,
            )
            world_params = scene.cm.get_one(
                WorldParameters, entity=core.get_id("world")
            )
            self.spirits_wrath += 1
            self.spirits_attitude = max(
                1, self.spirits_attitude - world_params.tree_cut_anger
            )
            self._log_info(
                f"decreased wrath {self.spirits_wrath} and attitude"
                f" {self.spirits_attitude}"
            )

    def on_season_reset(self, scene, season):
        if season == "Spring":
            self._log_info(f"relationship with the spirits improved")
            self.spirits_attitude += 1
            self.spirits_wrath -= 1
            self._log_info(
                f"improved wrath {self.spirits_wrath} and attitude"
                f" {self.spirits_attitude}"
            )
