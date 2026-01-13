import random

from engine import core
from horderl.components.events.build_world_events import BuildWorldListener
from horderl.components.pathfinding.pathfinder import Pathfinder
from horderl.components.pathfinding.simplex_cost_mapper import (
    SimplexCostMapper,
)
from horderl.components.world_building.world_parameters import WorldParameters

from ...content.terrain.water import make_water


class PlaceRiver(BuildWorldListener):
    def on_build_world(self, scene):
        self._log_info("placing river")
        cost = SimplexCostMapper().get_cost_map(scene)
        start = (random.randint(2, scene.config.map_width - 3), 0)
        end = (
            random.randint(2, scene.config.map_width - 3),
            scene.config.map_height - 1,
        )
        river = Pathfinder().get_path(cost, start, end, diagonal=0)
        if not river:
            self._log_warning("could not find a path for river")
        for x, y in river:
            self._log_debug(f"placing water ({x}, {y})")
            params = scene.cm.get_one(
                WorldParameters, entity=core.get_id("world")
            )
            scene.cm.add(*make_water(x, y, rapidness=params.river_rapids)[1])
