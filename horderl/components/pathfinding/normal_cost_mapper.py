import numpy as np

from engine.components import Coordinates

from ..pathfinder_cost import PathfinderCost
from ..pathfinding.cost_mapper import CostMapper


class NormalCostMapper(CostMapper):
    def get_cost_map(self, scene):
        size = (scene.config.map_width, scene.config.map_height)
        cost = np.ones(size, dtype=np.int8, order="F")
        for cost_component in scene.cm.get(PathfinderCost):
            coords = scene.cm.get_one(
                Coordinates, entity=cost_component.entity
            )
            cost[coords.x, coords.y] = cost_component.cost
        return cost
