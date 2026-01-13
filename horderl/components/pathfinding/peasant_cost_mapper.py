import numpy as np

from engine.components import Coordinates

from ..movement.drain_on_enter import DrainOnEnter
from ..pathfinder_cost import PathfinderCost
from ..pathfinding.cost_mapper import CostMapper


class PeasantCostMapper(CostMapper):
    """
    Apply an additional cost to anything that might be painful to step on.
    """

    def get_cost_map(self, scene):
        size = (scene.config.map_width, scene.config.map_height)
        cost = np.ones(size, dtype=np.int8, order="F")
        for cost_component in scene.cm.get(PathfinderCost):
            coords = scene.cm.get_one(
                Coordinates, entity=cost_component.entity
            )
            cost[coords.x, coords.y] = cost_component.cost

        for drain_on_enter in scene.cm.get(DrainOnEnter):
            coords = scene.cm.get_one(
                Coordinates, entity=drain_on_enter.entity
            )
            cost[coords.x, coords.y] += drain_on_enter.damage * 20

        return cost
