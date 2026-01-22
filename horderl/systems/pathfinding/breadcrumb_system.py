"""System for managing breadcrumb visualization entities."""

from __future__ import annotations

from typing import Iterable, List, Tuple

from engine import GameScene
from horderl.components.events.breadcrumb_events import (
    BreadcrumbsCleared,
    BreadcrumbsRequested,
)
from horderl.components.pathfinding.breadcrumb import Breadcrumb
from horderl.components.pathfinding.breadcrumb_tracker import BreadcrumbTracker
from horderl.content.breadcrumb import make_breadcrumb


def run(scene: GameScene) -> None:
    """
    Process breadcrumb update and cleanup requests.

    Args:
        scene: Active game scene providing component manager access.

    Side Effects:
        - Spawns breadcrumb entities to visualize paths.
        - Deletes breadcrumb entities that are cleared or orphaned.
        - Updates BreadcrumbTracker data with new breadcrumb IDs and paths.
    """
    _handle_breadcrumb_requests(scene)
    _handle_breadcrumb_clears(scene)
    _cleanup_orphaned_breadcrumbs(scene)


def _handle_breadcrumb_requests(scene: GameScene) -> None:
    for event in list(scene.cm.get(BreadcrumbsRequested)):
        tracker = scene.cm.get_one(BreadcrumbTracker, entity=event.entity)
        if tracker:
            _replace_breadcrumbs(scene, tracker, event.path)
        scene.cm.delete_component(event)


def _handle_breadcrumb_clears(scene: GameScene) -> None:
    for event in list(scene.cm.get(BreadcrumbsCleared)):
        _delete_breadcrumb_entities(scene, event.breadcrumb_ids)
        tracker = scene.cm.get_one(BreadcrumbTracker, entity=event.entity)
        if tracker:
            tracker.breadcrumbs = []
            tracker.path = []
        scene.cm.delete_component(event)


def _cleanup_orphaned_breadcrumbs(scene: GameScene) -> None:
    for breadcrumb in list(scene.cm.get(Breadcrumb)):
        if not scene.cm.get_one(BreadcrumbTracker, entity=breadcrumb.owner):
            scene.cm.delete(breadcrumb.entity)


def _replace_breadcrumbs(
    scene: GameScene,
    tracker: BreadcrumbTracker,
    path: Iterable[Tuple[int, int]],
) -> None:
    # Replace breadcrumbs to match the latest requested path.
    _delete_breadcrumb_entities(scene, tracker.breadcrumbs)
    new_breadcrumbs: List[int] = []
    for path_node in path:
        breadcrumb_entity, breadcrumb_components = make_breadcrumb(
            tracker.entity, path_node[0], path_node[1]
        )
        new_breadcrumbs.append(breadcrumb_entity)
        scene.cm.add(*breadcrumb_components)
    tracker.breadcrumbs = new_breadcrumbs
    tracker.path = list(path)


def _delete_breadcrumb_entities(
    scene: GameScene, breadcrumb_ids: Iterable[int]
) -> None:
    # Breadcrumbs are standalone entities that should be removed in full.
    for breadcrumb_id in breadcrumb_ids:
        scene.cm.delete(breadcrumb_id)
