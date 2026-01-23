import random

from engine import core
from horderl.components.pathfinding.cost_mapper import (
    CostMapper,
    CostMapperType,
)
from horderl.components.world_building.world_parameters import WorldParameters
from horderl.systems.pathfinding import get_path
from horderl.systems.pathfinding.target_selection import get_cost_map

from ...content.terrain.water import make_water


def place_river(scene):
    """Place a river in the world according to WorldParameters."""
    logger = core.get_logger(__name__)
    logger.info("placing river")
    cost = get_cost_map(scene, CostMapper(mapper_type=CostMapperType.SIMPLEX))
    start = (random.randint(2, scene.config.map_width - 3), 0)
    end = (
        random.randint(2, scene.config.map_width - 3),
        scene.config.map_height - 1,
    )
    river = get_path(cost, start, end, diagonal=0)
    if not river:
        logger.warning("could not find a path for river")
    for x, y in river:
        logger.debug(f"placing water ({x}, {y}))")
        params = scene.cm.get_one(WorldParameters, entity=core.get_id("world"))
        scene.cm.add(*make_water(x, y, rapidness=params.river_rapids)[1])
    logger.info("river placed.")
