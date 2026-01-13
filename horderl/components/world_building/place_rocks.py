import random
from dataclasses import dataclass

from engine import core
from engine.components import Coordinates
from engine.utilities import get_3_by_3_box
from horderl.components.events.build_world_events import BuildWorldListener
from horderl.components.world_building.world_parameters import WorldParameters

from ...content.terrain.rocks import make_rock


def add_rock(scene, x: int, y: int) -> None:
    coords = {(coord.x, coord.y) for coord in scene.cm.get(Coordinates)}
    if (x, y) not in coords:
        rock = make_rock(x, y)
        scene.cm.add(*rock[1])


@dataclass
class PlaceRocks(BuildWorldListener):
    def on_build_world(self, scene):
        self._log_info(f"placing rock fields in town...")
        world_settings = scene.cm.get_one(
            WorldParameters, entity=core.get_id("world")
        )
        for _ in range(world_settings.rock_fields):
            x = random.randint(0, scene.config.map_width - 1)
            y = random.randint(0, scene.config.map_height - 1)
            coords = {
                (coord.x, coord.y) for coord in scene.cm.get(Coordinates)
            }
            if (x, y) not in coords:
                self.add_rock_field(scene, x, y)

    def add_rock_field(self, scene, x: int, y: int) -> None:
        world_settings = scene.cm.get_one(
            WorldParameters, entity=core.get_id("world")
        )
        working_set = [(x, y)]
        maximum = 10
        while working_set and maximum > 0:
            working_x, working_y = working_set.pop(0)
            add_rock(scene, working_x, working_y)
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
