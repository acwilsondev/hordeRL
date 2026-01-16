import numpy as np
import tcod

from engine.components import Coordinates

from ..events.attack_started_events import AttackStartListener
from ..events.start_game_events import GameStartListener
from ..events.step_event import StepListener
from ..events.terrain_changed_event import TerrainChangedListener
from ..material import Material


class UpdateSenses(
    GameStartListener,
    TerrainChangedListener,
    AttackStartListener,
):
    def on_attack_start(self, scene):
        self.refresh_fov(scene)

    def on_game_start(self, scene):
        self.refresh_fov(scene)

    def on_terrain_changed(self, scene):
        self.refresh_fov(scene)
