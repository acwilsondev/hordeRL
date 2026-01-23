import numpy as np
import tcod

from engine.components.coordinates import Coordinates
from engine.game_scene import GameScene
from horderl.components.material import Material
from horderl.components.senses import Senses
from horderl.constants import PLAYER_ID


def run(scene: GameScene) -> None:
    player = scene.cm.get_one(Coordinates, entity=PLAYER_ID)
    senses = scene.cm.get_one(Senses, entity=PLAYER_ID)
    if not player or not senses:
        raise ValueError("Player or Senses component not found in scene.")

    if not senses.dirty:
        return

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
            (player.x, player.y),
            light_walls=True,
            radius=scene.config.torch_radius,
        )
