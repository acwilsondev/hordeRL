import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.component_manager import ComponentManager
from engine.components import Coordinates
from horderl.components.brains.ability_actors.place_fence_actor import (
    PlaceFenceActor,
)
from horderl.systems.abilities import placement_system


class DummyScene:
    """Minimal scene stub exposing a component manager."""

    def __init__(self) -> None:
        """Initialize the scene with a component manager."""
        self.cm = ComponentManager()


def test_place_spawns_components_for_actor():
    scene = DummyScene()
    actor = PlaceFenceActor(entity=1)

    entity_id = placement_system.place(scene, actor, 4, 7)

    coords = scene.cm.get_one(Coordinates, entity=entity_id)
    assert coords.x == 4
    assert coords.y == 7
