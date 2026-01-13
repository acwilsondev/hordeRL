import numpy as np
import tcod

from engine.components import Coordinates

from ..events.attack_started_events import AttackStartListener
from ..events.start_game_events import GameStartListener
from ..events.step_event import StepListener
from ..events.terrain_changed_event import TerrainChangedListener
from ..material import Material


class UpdateSenses(
    StepListener,
    GameStartListener,
    TerrainChangedListener,
    AttackStartListener,
):
    def on_attack_start(self, scene):
        self.refresh_fov(scene)

    def on_game_start(self, scene):
        self.refresh_fov(scene)

    def on_step(self, scene, point):
        self.refresh_fov(scene)

    def on_terrain_changed(self, scene):
        self.refresh_fov(scene)

    def refresh_fov(self, scene):
        mob = scene.cm.get_one(Coordinates, entity=self.entity)
        transparency = np.ones(
            (scene.config.map_width, scene.config.map_height),
            order="F",
            dtype=bool,
        )
        materials = scene.cm.get(Material, query=lambda m: m.blocks_sight)
        for material in materials:
            coords = scene.cm.get_one(Coordinates, entity=material.entity)
            transparency[coords.x, coords.y] = False
            scene.visibility_map[:] = tcod.map.compute_fov(
                transparency,
                (mob.x, mob.y),
                light_walls=True,
                radius=scene.config.torch_radius,
            )
