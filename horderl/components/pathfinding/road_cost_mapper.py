import numpy as np

from ... import settings
from .. import Attributes, Coordinates
from ..pathfinding.cost_mapper import CostMapper
from ..tags.water_tag import WaterTag


class RoadCostMapper(CostMapper):
    def get_cost_map(self, scene):
        size = (settings.MAP_WIDTH, settings.MAP_HEIGHT)
        cost = np.ones(size, dtype=np.uint16, order="F")
        for coord in scene.cm.get(Coordinates):
            if scene.cm.get_one(Attributes, entity=coord.entity):
                cost[coord.x, coord.y] = 10000
            elif scene.cm.get_one(WaterTag, entity=coord.entity):
                cost[coord.x, coord.y] += 2
            else:
                cost[coord.x, coord.y] += 1000
        return cost
