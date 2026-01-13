from dataclasses import dataclass

from engine.components.events import Event
from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)
from horderl.i18n import t


@dataclass
class ResetSeason(Event):
    # Season we're entering
    season: str = "None"

    def listener_type(self):
        return SeasonResetListener

    def notify(self, scene, listener):
        listener.on_season_reset(scene, self.season)

    def _after_notify(self, scene):
        scene.message(
            t(
                "message.season_begin",
                season=t(f"season.{self.season.lower()}"),
            )
        )
