import numpy as np
from engine.components import Coordinates

from engine.components.entity import Entity

from .. import Attributes
from ..material import Material
from .cost_mapper import CostMapper


class StraightLineCostMapper(CostMapper):
    def get_cost_map(self, scene):
        size = (scene.config.map_width, scene.config.map_height)
        cost = np.ones(size, dtype=np.int8, order="F")

        points = scene.cm.get(Coordinates)
        for point in points:
            material = scene.cm.get_one(Material, entity=point.entity)
            attributes = scene.cm.get_one(Attributes, entity=point.entity)
            if material and material.blocks and not attributes:
                # You can't bash your way through this one
                entity = scene.cm.get_one(Entity, entity=point.entity)
                self._log_debug(
                    f"found impassible terrain: {entity.name} at position"
                    f" {point.position}"
                )
                cost[point.x, point.y] = 0
        return cost
