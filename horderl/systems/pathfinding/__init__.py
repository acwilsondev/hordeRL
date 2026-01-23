"""Pathfinding systems package."""

from __future__ import annotations

from typing import Iterable

import tcod

from horderl.components.path_node import PathNode


def get_path(
    cost_map,
    start: tuple[int, int],
    end: tuple[int, int],
    diagonal: int = 3,
) -> list[tuple[int, int]]:
    """
    Compute a path between two points using a cost map.

    Args:
        cost_map: Cost grid usable by tcod's SimpleGraph.
        start (tuple[int, int]): Starting (x, y) position.
        end (tuple[int, int]): Target (x, y) position.
        diagonal (int): Diagonal movement cost for pathfinding.

    Returns:
        list[tuple[int, int]]: Ordered list of path coordinates.

    Side Effects:
        None.
    """
    graph = tcod.path.SimpleGraph(cost=cost_map, cardinal=2, diagonal=diagonal)
    pathfinder = tcod.path.Pathfinder(graph)
    pathfinder.add_root(start)
    path = pathfinder.path_to(end).tolist()
    return path


def create_path_nodes(
    entity: int, path: Iterable[tuple[int, int]]
) -> list[PathNode]:
    """
    Build PathNode components for an ordered path.

    Args:
        entity (int): Entity that owns the path nodes.
        path (Iterable[tuple[int, int]]): Ordered path coordinates.

    Returns:
        list[PathNode]: Components representing the path steps.

    Side Effects:
        None.
    """
    return [
        PathNode(entity=entity, step=step, x=location[0], y=location[1])
        for step, location in enumerate(path)
    ]
