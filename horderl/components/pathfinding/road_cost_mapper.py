import numpy as np
from engine.components import Coordinates

from .. import Attributes
from ..pathfinding.cost_mapper import CostMapper
from ..tags.water_tag import WaterTag


class RoadCostMapper(CostMapper):
    def get_cost_map(self, scene):
        size = (scene.config.map_width, scene.config.map_height)
        cost = np.ones(size, dtype=np.uint16, order="F")
        for coord in scene.cm.get(Coordinates):
            if scene.cm.get_one(Attributes, entity=coord.entity):
                cost[coord.x, coord.y] = 10000
            elif scene.cm.get_one(WaterTag, entity=coord.entity):
                cost[coord.x, coord.y] += 2
            else:
                cost[coord.x, coord.y] += 1000
        return cost
