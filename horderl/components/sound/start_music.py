from dataclasses import dataclass

from ..events.start_game_events import GameStartListener
from ..season_reset_listeners.seasonal_actor import SeasonResetListener


@dataclass
class StartMusic(GameStartListener, SeasonResetListener):
    def on_season_reset(self, scene, season):
        scene.sound.play("town")

    def on_game_start(self, scene):
        scene.sound.play("town")
