"""System-level helpers for selecting pathfinding targets."""

from typing import Iterable, Optional, Tuple

import numpy as np
import tcod

from engine.components import Coordinates


def get_new_target(
    scene,
    cost_map: np.ndarray,
    start: Tuple[int, int],
    entity_values: Iterable[Tuple[int, float]],
) -> Optional[int]:
    """
    Pick the highest-value reachable entity using a Dijkstra distance map.

    Args:
        scene: Active scene containing config and component manager data.
        cost_map: Numpy-compatible cost grid used for pathfinding.
        start: (x, y) coordinates to start the distance calculation from.
        entity_values: Iterable of (entity_id, value) pairs to score.

    Returns:
        The entity id of the best target, or ``None`` when no target can be
        selected.

    Side Effects:
        None. This function allocates a distance map but does not mutate the
        scene or components.
    """
    dist = tcod.path.maxarray(
        (scene.config.map_width, scene.config.map_height), dtype=np.int32
    )
    dist[start[0], start[1]] = 0
    tcod.path.dijkstra2d(dist, cost_map, 2, 3, out=dist)
    # find the cost of all the possible targets
    best = (None, 0)
    for entity, value in entity_values:
        target_coords = scene.cm.get_one(Coordinates, entity=entity)
        cost_to_reach = float(dist[target_coords.x, target_coords.y]) ** 2
        if cost_to_reach == 0:
            cost_to_reach = 1
        value = float(value) / cost_to_reach
        if value > best[1]:
            best = (entity, value)

    return best[0]
