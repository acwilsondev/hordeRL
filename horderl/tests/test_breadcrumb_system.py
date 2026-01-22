from engine.component_manager import ComponentManager
from horderl.components.events.breadcrumb_events import (
    BreadcrumbsCleared,
    BreadcrumbsRequested,
)
from horderl.components.pathfinding.breadcrumb import Breadcrumb
from horderl.components.pathfinding.breadcrumb_tracker import BreadcrumbTracker
from horderl.content.breadcrumb import make_breadcrumb
from horderl.systems.pathfinding import breadcrumb_system


class DummyScene:
    def __init__(self):
        self.cm = ComponentManager()


def test_breadcrumb_request_replaces_entities_and_updates_tracker():
    scene = DummyScene()
    tracker = BreadcrumbTracker(entity=1)
    old_breadcrumb = make_breadcrumb(1, 0, 0)
    scene.cm.add(*old_breadcrumb[1])
    tracker.breadcrumbs = [old_breadcrumb[0]]
    tracker.path = [(0, 0)]
    scene.cm.add(tracker)
    scene.cm.add(BreadcrumbsRequested(entity=1, path=[(1, 1), (2, 2)]))

    breadcrumb_system.run(scene)

    assert scene.cm.get_one(Breadcrumb, entity=old_breadcrumb[0]) is None
    assert tracker.breadcrumbs
    assert tracker.path == [(1, 1), (2, 2)]
    for breadcrumb_id in tracker.breadcrumbs:
        breadcrumb = scene.cm.get_one(Breadcrumb, entity=breadcrumb_id)
        assert breadcrumb.owner == 1


def test_breadcrumb_clear_removes_entities_and_resets_tracker():
    scene = DummyScene()
    tracker = BreadcrumbTracker(entity=2)
    breadcrumb = make_breadcrumb(2, 5, 6)
    scene.cm.add(*breadcrumb[1])
    tracker.breadcrumbs = [breadcrumb[0]]
    tracker.path = [(5, 6)]
    scene.cm.add(tracker)
    scene.cm.add(BreadcrumbsCleared(entity=2, breadcrumb_ids=[breadcrumb[0]]))

    breadcrumb_system.run(scene)

    assert scene.cm.get_one(Breadcrumb, entity=breadcrumb[0]) is None
    assert tracker.breadcrumbs == []
    assert tracker.path == []


def test_breadcrumb_system_cleans_orphans():
    scene = DummyScene()
    breadcrumb = make_breadcrumb(99, 7, 8)
    scene.cm.add(*breadcrumb[1])

    breadcrumb_system.run(scene)

    assert scene.cm.get_one(Breadcrumb, entity=breadcrumb[0]) is None
