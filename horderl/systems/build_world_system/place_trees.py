import random

from engine import core
from engine.components import Coordinates
from engine.utilities import get_3_by_3_box
from horderl.components.world_building.world_parameters import WorldParameters

from ...content.terrain.trees import make_tree


def place_trees(scene):
    """Place copse of trees in the world according to WorldParameters."""
    logger = core.get_logger(__name__)
    logger.info(f"placing copse of trees in town...")
    world_settings = scene.cm.get_one(
        WorldParameters, entity=core.get_id("world")
    )

    for _ in range(world_settings.copse):
        x = random.randint(0, scene.config.map_width - 1)
        y = random.randint(0, scene.config.map_height - 1)
        coords = {(coord.x, coord.y) for coord in scene.cm.get(Coordinates)}
        if (x, y) not in coords:
            _spawn_copse(scene, x, y)
    logger.info(f"copse of trees placed.")


def _spawn_copse(scene, x: int, y: int) -> None:
    world_settings = scene.cm.get_one(
        WorldParameters, entity=core.get_id("world")
    )
    working_set = [(x, y)]
    maximum = 10
    while working_set and maximum > 0:
        working_x, working_y = working_set.pop(0)
        _add_tree(scene, working_x, working_y)
        maximum -= 1
        working_set += [
            (_x, _y)
            for _x, _y in get_3_by_3_box(working_x, working_y)
            if (
                random.random() <= world_settings.copse_proliferation
                and 0 < _x < scene.config.map_width - 1
                and 0 < _y < scene.config.map_height - 1
            )
        ]


def _add_tree(scene, x: int, y: int) -> None:
    coords = {(coord.x, coord.y) for coord in scene.cm.get(Coordinates)}
    if (x, y) not in coords:
        tree = make_tree(x, y)
        scene.cm.add(*tree[1])
