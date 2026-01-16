import numpy as np
import pytest

pytest.importorskip("tcod")

from engine.component_manager import ComponentManager
from engine.components import Coordinates
from horderl.config import Config
from horderl.systems.pathfinding.target_selection import get_new_target


class DummyScene:
    """Minimal scene fixture for pathfinding target selection tests."""

    def __init__(self):
        """
        Initialize the scene with a component manager and small map config.

        Side Effects:
            Initializes in-memory scene state for tests.
        """
        self.cm = ComponentManager()
        self.config = Config(map_width=5, map_height=5)


def test_get_new_target_prefers_best_value_to_cost_ratio():
    """
    Validate that target selection prefers the best value-to-cost ratio.

    Side Effects:
        Adds in-memory coordinates to the dummy scene component manager.
    """
    scene = DummyScene()
    near_target = 1
    far_target = 2
    scene.cm.add(
        Coordinates(entity=near_target, x=1, y=1),
        Coordinates(entity=far_target, x=4, y=4),
    )

    cost_map = np.ones((5, 5), dtype=np.int32)
    entity_values = [(near_target, 10), (far_target, 100)]

    target = get_new_target(scene, cost_map, (0, 0), entity_values)

    assert target == near_target


def test_get_new_target_returns_none_when_no_targets():
    """
    Validate that target selection returns ``None`` when no targets exist.

    Side Effects:
        None. The test only allocates a cost map and calls the selector.
    """
    scene = DummyScene()
    cost_map = np.ones((5, 5), dtype=np.int32)

    target = get_new_target(scene, cost_map, (0, 0), [])

    assert target is None
