import random

from engine import core
from engine.components import Coordinates
from engine.utilities import get_3_by_3_box
from horderl.components.world_building.world_parameters import WorldParameters

from ...content.terrain.rocks import make_rock


def place_rocks(scene):
    """Place rock fields in the world according to WorldParameters."""
    logger = core.get_logger(__name__)
    logger.info(f"placing rock fields in town...")
    world_settings = scene.cm.get_one(
        WorldParameters, entity=core.get_id("world")
    )
    for _ in range(world_settings.rock_fields):
        x = random.randint(0, scene.config.map_width - 1)
        y = random.randint(0, scene.config.map_height - 1)
        coords = {(coord.x, coord.y) for coord in scene.cm.get(Coordinates)}
        if (x, y) not in coords:
            _add_rock_field(scene, x, y)
    logger.info(f"rock fields placed.")


def _add_rock_field(scene, x: int, y: int) -> None:
    world_settings = scene.cm.get_one(
        WorldParameters, entity=core.get_id("world")
    )
    working_set = [(x, y)]
    maximum = 10
    while working_set and maximum > 0:
        working_x, working_y = working_set.pop(0)
        _add_rock(scene, working_x, working_y)
        maximum -= 1
        working_set += [
            (_x, _y)
            for _x, _y in get_3_by_3_box(working_x, working_y)
            if (
                random.random() <= world_settings.rocks_proliferation
                and 0 < _x < scene.config.map_width - 1
                and 0 < _y < scene.config.map_height - 1
            )
        ]


def _add_rock(scene, x: int, y: int) -> None:
    coords = {(coord.x, coord.y) for coord in scene.cm.get(Coordinates)}
    if (x, y) not in coords:
        rock = make_rock(x, y)
        scene.cm.add(*rock[1])
