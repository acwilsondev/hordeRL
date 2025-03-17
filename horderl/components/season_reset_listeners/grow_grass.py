from dataclasses import dataclass

from horderl.components.season_reset_listeners.seasonal_actor import SeasonResetListener


@dataclass
class GrowGrass(SeasonResetListener):
    def on_season_reset(self, scene, season):
        if season in {"Spring", "Summer"}:
            scene.cm.delete(self.entity)
