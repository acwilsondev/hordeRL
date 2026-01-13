from dataclasses import dataclass

from horderl.components.actors.hordeling_spawner import HordelingSpawner
from horderl.components.events.attack_started_events import AttackStarted
from horderl.components.events.new_day_event import DayBegan
from horderl.components.season_reset_listeners.reset_season import ResetSeason
from horderl.components.tags.hordeling_tag import HordelingTag
from horderl.components.world_beauty import WorldBeauty
from horderl.content.spawners.hordeling_spawner_spawner import (
    hordeling_spawner,
)
from horderl.engine import core
from horderl.components.actors.energy_actor import EnergyActor
from horderl.i18n import t

MAX_HOUR = 23
MAX_DAY = 30
MAX_SEASON = 4


@dataclass
class Calendar(EnergyActor):
    day: int = 0
    season: int = 1
    year: int = 1217
    status: str = "Peacetime"
    energy_cost: int = EnergyActor.DAILY
    round = 1

    def __post_init__(self) -> None:
        self.status = t("status.peacetime")

    def increment(self):
        self.day += 1
        if self.day > MAX_DAY:
            self.season += 1
            self.day = 1

        if self.season > MAX_SEASON:
            self.year += 1
            self.season = 1
        self.pass_turn()

    def get_timecode(self):
        season = self.get_season_string()
        return t(
            "timecode.format",
            season=t(f"season.{season.lower()}"),
            day=self.day,
            year=self.year,
        )

    def get_season_string(self):
        return {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}[self.season]

    def act(self, scene):
        if self.day < 25:
            self.status = t("status.peacetime")
            self.increment()
            scene.cm.add(DayBegan(entity=self.entity, day=self.day))
        elif self.day < 30:
            self.status = t("status.horde_approaching")
            self.increment()
            scene.cm.add(DayBegan(entity=self.entity, day=self.day))
        else:
            if self.status != t("status.under_attack"):
                self._start_attack(scene)
            if not still_under_attack(scene):
                self._end_attack(scene)

    def _start_attack(self, scene):
        scene.popup_message(t("message.horde_arrival"))
        spirits_wrath = scene.cm.get_one(
            WorldBeauty, entity=core.get_id("world")
        ).spirits_wrath

        scene.cm.add(*hordeling_spawner(waves=self.round + spirits_wrath)[1])
        scene.cm.add(AttackStarted(entity=scene.player))
        self.is_recharging = False
        self.status = t("status.under_attack")

    def _end_attack(self, scene):
        self.status = t("status.peacetime")
        self.round += 1
        self.is_recharging = True
        self.increment()
        scene.cm.add(DayBegan(entity=self.entity))
        scene.cm.add(
            ResetSeason(entity=self.entity, season=self.get_season_string())
        )


def still_under_attack(scene):
    return (
        scene.cm.get(HordelingSpawner)
        or scene.cm.get(HordelingSpawner)
        or [t for t in scene.cm.get(HordelingTag)]
    )
