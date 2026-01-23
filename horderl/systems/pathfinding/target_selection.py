"""System-level helpers for selecting pathfinding targets."""

from __future__ import annotations

from typing import Iterable, Optional, Tuple

import numpy as np
import tcod

from engine.components import Coordinates
from engine.components.entity import Entity
from engine.logging import get_logger
from horderl.components import Attributes
from horderl.components.material import Material
from horderl.components.movement.drain_on_enter import DrainOnEnter
from horderl.components.pathfinder_cost import PathfinderCost
from horderl.components.pathfinding.cost_mapper import (
    CostMapper,
    CostMapperType,
)
from horderl.components.pathfinding.target_evaluation.target_evaluator import (
    TargetEvaluator,
    TargetEvaluatorType,
)
from horderl.components.tags.crop_info import CropInfo
from horderl.components.tags.hordeling_tag import HordelingTag
from horderl.components.tags.water_tag import WaterTag
from horderl.components.target_value import TargetValue


def get_cost_map(scene, cost_mapper: CostMapper | None) -> np.ndarray:
    """
    Build a cost map for a mapper component, falling back to defaults.

    Args:
        scene: Active scene containing configuration and components.
        cost_mapper: Optional cost mapper component for an entity.

    Returns:
        numpy.ndarray: Cost grid for pathfinding decisions.

    Components Consumed:
        - CostMapper configured with a CostMapperType.
        - Coordinates, PathfinderCost, DrainOnEnter, Attributes, WaterTag,
          Material, Entity (depending on mapper type).

    Side Effects:
        None.
    """
    mapper = cost_mapper or CostMapper(mapper_type=CostMapperType.NORMAL)
    return _build_cost_map(scene, mapper)


def _build_cost_map(scene, cost_mapper: CostMapper) -> np.ndarray:
    # Assumes the mapper instance indicates the mapping strategy.
    if cost_mapper.mapper_type == CostMapperType.NORMAL:
        return _build_normal_cost_map(scene)
    if cost_mapper.mapper_type == CostMapperType.STEALTHY:
        return _build_stealthy_cost_map(scene)
    if cost_mapper.mapper_type == CostMapperType.PEASANT:
        return _build_peasant_cost_map(scene)
    if cost_mapper.mapper_type == CostMapperType.ROAD:
        return _build_road_cost_map(scene)
    if cost_mapper.mapper_type == CostMapperType.SIMPLEX:
        return _build_simplex_cost_map(scene)
    if cost_mapper.mapper_type == CostMapperType.STRAIGHT_LINE:
        return _build_straight_line_cost_map(scene)
    raise ValueError(
        f"Unsupported cost mapper type: {cost_mapper.mapper_type}"
    )


def _build_normal_cost_map(scene) -> np.ndarray:
    # Uses PathfinderCost overrides for baseline grid.
    size = (scene.config.map_width, scene.config.map_height)
    cost = np.ones(size, dtype=np.int8, order="F")
    for cost_component in scene.cm.get(PathfinderCost):
        coords = scene.cm.get_one(Coordinates, entity=cost_component.entity)
        cost[coords.x, coords.y] = cost_component.cost
    return cost


def _build_stealthy_cost_map(scene) -> np.ndarray:
    # Visibility is penalized to favor stealthy routes.
    cost = _build_normal_cost_map(scene)
    visibility_cost = np.where(
        scene.visibility_map,
        np.ones(
            (scene.config.map_width, scene.config.map_height),
            order="F",
            dtype=int,
        )
        * 5,
        np.ones(
            (scene.config.map_width, scene.config.map_height),
            order="F",
            dtype=int,
        ),
    )
    return cost * visibility_cost


def _build_peasant_cost_map(scene) -> np.ndarray:
    # Adds hazards to the base cost map.
    cost = _build_normal_cost_map(scene)
    for drain_on_enter in scene.cm.get(DrainOnEnter):
        coords = scene.cm.get_one(Coordinates, entity=drain_on_enter.entity)
        cost[coords.x, coords.y] += drain_on_enter.damage * 20
    return cost


def _build_road_cost_map(scene) -> np.ndarray:
    # Occupied tiles and non-water terrain are heavily penalized.
    size = (scene.config.map_width, scene.config.map_height)
    cost = np.ones(size, dtype=np.uint16, order="F")
    max_x, max_y = size
    for coord in scene.cm.get(Coordinates):
        if coord.x < 0 or coord.x >= max_x or coord.y < 0 or coord.y >= max_y:
            continue
        if scene.cm.get_one(Attributes, entity=coord.entity):
            cost[coord.x, coord.y] = 10000
        elif scene.cm.get_one(WaterTag, entity=coord.entity):
            cost[coord.x, coord.y] += 2
        else:
            cost[coord.x, coord.y] += 1000
    return cost


def _build_simplex_cost_map(scene) -> np.ndarray:
    noise = tcod.noise.Noise(
        dimensions=2, algorithm=tcod.noise.Algorithm.SIMPLEX, octaves=3
    )
    cost = noise[
        tcod.noise.grid(
            shape=(scene.config.map_width, scene.config.map_height),
            scale=0.5,
            origin=(0, 0),
        )
    ]
    cost *= 10
    return cost.astype(np.uint16).transpose()


def _build_straight_line_cost_map(scene) -> np.ndarray:
    # Blocks tiles that cannot be bashed through by juggernauts.
    size = (scene.config.map_width, scene.config.map_height)
    cost = np.ones(size, dtype=np.int8, order="F")
    logger = get_logger(__name__)
    for point in scene.cm.get(Coordinates):
        material = scene.cm.get_one(Material, entity=point.entity)
        attributes = scene.cm.get_one(Attributes, entity=point.entity)
        if material and material.blocks and not attributes:
            entity = scene.cm.get_one(Entity, entity=point.entity)
            if entity:
                logger.debug(
                    "found impassible terrain: %s at position %s",
                    entity.name,
                    point.position,
                )
            cost[point.x, point.y] = 0
    return cost


def get_target_values(
    scene, evaluator: TargetEvaluator
) -> list[tuple[int, float]]:
    """
    Collect target entities and scores for a target evaluator component.

    Args:
        scene: Active scene containing components for evaluation.
        evaluator: Target evaluator component describing the strategy.

    Returns:
        List[Tuple[int, float]]: (entity, value) pairs for target selection.

    Components Consumed:
        - TargetValue for base target scores.
        - CropInfo for crop multipliers.
        - HordelingTag for ally targeting.

    Side Effects:
        None.
    """
    if evaluator.evaluator_type is TargetEvaluatorType.HORDELING:
        return [(tv.entity, tv.value) for tv in scene.cm.get(TargetValue)]
    if evaluator.evaluator_type is TargetEvaluatorType.HIGH_CROP:
        return [
            _get_crop_evaluation(scene, tv.entity, tv.value)
            for tv in scene.cm.get(TargetValue)
        ]
    if evaluator.evaluator_type is TargetEvaluatorType.ALLY:
        return [(tv.entity, 1) for tv in scene.cm.get(HordelingTag)]
    raise ValueError(
        f"Unsupported target evaluator: {type(evaluator).__name__}"
    )


def _get_crop_evaluation(scene, entity, value) -> tuple[int, float]:
    # Crops get a higher multiplier to encourage prioritization.
    multiplier = 5 if scene.cm.get_one(CropInfo, entity=entity) else 1
    return entity, value * multiplier


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
