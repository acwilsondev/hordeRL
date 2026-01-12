from dataclasses import dataclass

from horderl.components.events.start_game_events import GameStartListener
from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)
from horderl.components.serialization.save_game import SaveGame


@dataclass
class SaveOnSeasonReset(SeasonResetListener, GameStartListener):
    """
    Save the game each season.
    """

    def on_game_start(self, scene):
        self.autosave(scene)

    def on_season_reset(self, scene, season):
        self.autosave(scene)

    def autosave(self, scene):
        if not scene.config.autosave_enabled:
            self._log_info(f"autosave is disabled")
            return
        scene.cm.add(SaveGame(entity=scene.player))
