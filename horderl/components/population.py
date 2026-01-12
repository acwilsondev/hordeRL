from dataclasses import dataclass

from ..components.events.peasant_events import (
    PeasantAddedListener,
    PeasantDiedListener,
)
from ..i18n import t


@dataclass
class Population(PeasantAddedListener, PeasantDiedListener):
    population: int = 0

    def on_peasant_added(self, scene):
        self._log_info("population increased")
        self.population += 1

    def on_peasant_died(self, scene):
        self._log_info("population decreased")
        self.population -= 1
        if self.population <= 0:
            scene.popup_message(
                t("message.peasants_dead")
            )
            scene.pop()
