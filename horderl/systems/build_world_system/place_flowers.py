import random

from engine import core
from engine.components import Coordinates
from engine.utilities import get_3_by_3_box
from horderl import palettes
from horderl.components.world_building.world_parameters import WorldParameters

from ...content.terrain.flower import make_flower


def place_flowers(scene):
    """Place flower fields in the world according to WorldParameters."""
    logger = core.get_logger(__name__)
    logger.info(f"placing flower fields...")
    world_settings = scene.cm.get_one(
        WorldParameters, entity=core.get_id("world")
    )
    if world_settings.flower_color is None:
        world_settings.flower_color = random.choice(
            [
                palettes.WHITE,
                palettes.WATER,
                palettes.FRESH_BLOOD,
                palettes.FIRE,
                palettes.GOLD,
            ]
        )
    for _ in range(world_settings.flower_fields):
        x = random.randint(0, scene.config.map_width - 1)
        y = random.randint(0, scene.config.map_height - 1)
        _add_flower_field(scene, x, y)
    logger.info(f"flower fields placed.")

def _add_flower_field(scene, x: int, y: int) -> None:
    world_settings = scene.cm.get_one(
        WorldParameters, entity=core.get_id("world")
    )
    color = world_settings.flower_color
    working_set = [(x, y)]
    maximum = 10
    while working_set and maximum > 0:
        working_x, working_y = working_set.pop(0)
        _add_flower(scene, working_x, working_y, color)
        maximum -= 1
        working_set += [
            (_x, _y)
            for _x, _y in get_3_by_3_box(working_x, working_y)
            if (
                random.random() <= world_settings.flower_proliferation
                and 0 < _x < scene.config.map_width - 1
                and 0 < _y < scene.config.map_height - 1
            )
        ]


def _add_flower(scene, x: int, y: int, color) -> None:
    coords = {(coord.x, coord.y) for coord in scene.cm.get(Coordinates)}
    if (x, y) not in coords:
        flower = make_flower(x, y, color)
        scene.cm.add(*flower[1])
    color = None
