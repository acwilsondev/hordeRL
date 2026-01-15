import numpy as np

from engine.components import Coordinates

from .. import Attributes
from ..pathfinding.cost_mapper import CostMapper
from ..tags.water_tag import WaterTag


class RoadCostMapper(CostMapper):
    """Builds cost maps for road routing based on terrain and obstacles."""

    def get_cost_map(self, scene):
        """Return a cost grid for road pathfinding in the given scene.

        Intent:
            Produce a dense grid of traversal costs used by road routing. Costs
            are increased for non-water terrain, made higher for occupied tiles,
            and slightly increased for water tiles.

        Parameters:
            scene: Active game scene providing configuration and components.

        Returns:
            numpy.ndarray: A 2D array of traversal costs indexed by (x, y).

        Side effects:
            None.
        """
        size = (scene.config.map_width, scene.config.map_height)
        cost = np.ones(size, dtype=np.uint16, order="F")
        max_x, max_y = size
        for coord in scene.cm.get(Coordinates):
            # Some entities may live outside the map bounds; ignore them.
            if (
                coord.x < 0
                or coord.x >= max_x
                or coord.y < 0
                or coord.y >= max_y
            ):
                continue
            if scene.cm.get_one(Attributes, entity=coord.entity):
                cost[coord.x, coord.y] = 10000
            elif scene.cm.get_one(WaterTag, entity=coord.entity):
                cost[coord.x, coord.y] += 2
            else:
                cost[coord.x, coord.y] += 1000
        return cost
