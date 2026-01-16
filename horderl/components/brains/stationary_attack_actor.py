from dataclasses import dataclass

from engine import constants
from horderl.components.brains.brain import Brain
from horderl.components.events.attack_started_events import AttackStartListener
from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)


@dataclass
class StationaryAttackActor(Brain, SeasonResetListener, AttackStartListener):
    """
    Stand in place and attack any enemy in range.
    """

    target: int = constants.INVALID
    cost_map = None
    root_x: int = constants.INVALID
    root_y: int = constants.INVALID

    def on_season_reset(self, scene, season):
        from horderl.systems.brain_system import on_stationary_season_reset

        on_stationary_season_reset(scene, self, season)

    def on_attack_start(self, scene):
        from horderl.systems.brain_system import on_stationary_attack_start

        on_stationary_attack_start(scene, self)
