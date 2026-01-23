import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.component_manager import ComponentManager
from engine.components import Coordinates
from horderl.components.brains.painters.create_gold_actor import (
    PlaceGoldController,
)
from horderl.components.brains.painters.create_hordeling_actor import (
    PlaceHordelingController,
)
from horderl.components.pickup_gold import GoldPickup
from horderl.components.tags.tag import Tag, TagType
from horderl.content.cursor import make_cursor
from horderl.systems.debug import painter_system


class DummyScene:
    """Minimal scene stub exposing a component manager."""

    def __init__(self) -> None:
        self.cm = ComponentManager()


def test_painter_system_spawns_gold_at_cursor():
    scene = DummyScene()
    cursor_id, cursor_components = make_cursor(3, 5)
    scene.cm.add(*cursor_components)
    painter = PlaceGoldController(entity=1, cursor=cursor_id)

    painter_system.paint_at_cursor(scene, painter)

    gold_pickups = scene.cm.get(GoldPickup)
    assert len(gold_pickups) == 1
    coords = scene.cm.get_one(Coordinates, entity=gold_pickups[0].entity)
    assert (coords.x, coords.y) == (3, 5)


def test_painter_system_spawns_hordeling_at_cursor():
    scene = DummyScene()
    cursor_id, cursor_components = make_cursor(7, 11)
    scene.cm.add(*cursor_components)
    painter = PlaceHordelingController(entity=2, cursor=cursor_id)

    painter_system.paint_at_cursor(scene, painter)

    hordeling_tags = scene.cm.get(
        Tag, query=lambda tag: tag.tag_type == TagType.HORDELING
    )
    assert len(hordeling_tags) == 1
    coords = scene.cm.get_one(Coordinates, entity=hordeling_tags[0].entity)
    assert (coords.x, coords.y) == (7, 11)
