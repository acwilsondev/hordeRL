import numpy as np

import settings
from components import Coordinates
from components.pathfinder_cost import PathfinderCost
from components.pathfinding.cost_mapper import CostMapper


class NormalCostMapper(CostMapper):
    def get_cost_map(self, scene):
        size = (settings.MAP_WIDTH, settings.MAP_HEIGHT)
        cost = np.ones(size, dtype=np.int8, order="F")
        for cost_component in scene.cm.get(PathfinderCost):
            coords = scene.cm.get_one(Coordinates, entity=cost_component.entity)
            cost[coords.x, coords.y] = cost_component.cost
        return cost
