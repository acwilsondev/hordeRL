import numpy as np

from ... import settings
from .. import Coordinates
from ..pathfinder_cost import PathfinderCost
from ..pathfinding.cost_mapper import CostMapper


class StealthyCostMapper(CostMapper):
    def get_cost_map(self, scene):
        size = (settings.MAP_WIDTH, settings.MAP_HEIGHT)
        cost = np.ones(size, dtype=np.int8, order="F")
        for cost_component in scene.cm.get(PathfinderCost):
            coords = scene.cm.get_one(Coordinates, entity=cost_component.entity)
            cost[coords.x, coords.y] = cost_component.cost

        visibility_cost = np.where(
            scene.visibility_map,
            np.ones(
                (settings.MAP_WIDTH, settings.MAP_HEIGHT), order="F", dtype=int
            )
            * 5,
            np.ones(
                (settings.MAP_WIDTH, settings.MAP_HEIGHT), order="F", dtype=int
            ),
        )
        cost *= visibility_cost

        return cost
