import random

from engine import core
from engine.components import Coordinates
from engine.utilities import get_3_by_3_box
from horderl.components.world_building.world_parameters import WorldParameters

from ...content.terrain.water import make_swampy_water, make_water


def place_lakes(scene):
    """Place lakes in the world according to WorldParameters."""
    logger = core.get_logger(__name__)
    logger.info(f"placing lakes in town")
    world_settings = scene.cm.get_one(
        WorldParameters, entity=core.get_id("world")
    )

    for _ in range(world_settings.lakes):
        x = random.randint(0, scene.config.map_width - 1)
        y = random.randint(0, scene.config.map_height - 1)
        coords = {(coord.x, coord.y) for coord in scene.cm.get(Coordinates)}
        if (x, y) not in coords:
            _spawn_lake(scene, x, y)
    logger.info(f"lakes placed.")


def _spawn_lake(scene, x: int, y: int) -> None:
    working_set = [(x, y)]
    maximum = 50
    world_settings = scene.cm.get_one(
        WorldParameters, entity=core.get_id("world")
    )
    if world_settings.is_water_swampy:
        water_painter = make_swampy_water
    else:
        water_painter = make_water

    while working_set and maximum > 0:
        working_x, working_y = working_set.pop(0)
        _add_water(
            scene,
            working_x,
            working_y,
            water_painter,
            world_settings.river_rapids,
        )
        maximum -= 1
        working_set += [
            (_x, _y)
            for _x, _y in get_3_by_3_box(working_x, working_y)
            if (
                random.random() <= world_settings.lake_proliferation
                and 0 < _x < scene.config.map_width
                and 0 < _y < scene.config.map_height
            )
        ]


def _add_water(scene, x: int, y: int, painter, rapidness) -> None:
    coords = {(coord.x, coord.y) for coord in scene.cm.get(Coordinates)}
    if (x, y) not in coords:
        water = painter(x, y, rapidness)
        scene.cm.add(*water[1])
