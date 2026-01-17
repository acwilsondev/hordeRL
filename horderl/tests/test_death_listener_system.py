from engine.component_manager import ComponentManager
from engine.components import Coordinates
from horderl.components.death_listeners.drop_gold import DropGold
from horderl.components.death_listeners.schedule_rebuild import ScheduleRebuild
from horderl.components.events.die_events import Die
from horderl.components.house_structure import HouseStructure
from horderl.components.pickup_gold import GoldPickup
from horderl.systems.death_listener_system import run as run_death_listeners


class DummyScene:
    """Minimal scene stub exposing a component manager."""

    def __init__(self) -> None:
        """Initialize the scene with a component manager."""
        self.cm = ComponentManager()


def test_death_listener_system_drops_gold_on_die() -> None:
    scene = DummyScene()
    entity = 1
    scene.cm.add(
        Coordinates(entity=entity, x=2, y=3),
        DropGold(entity=entity),
        Die(entity=entity),
    )

    run_death_listeners(scene)

    gold_pickups = scene.cm.get(GoldPickup)
    assert len(gold_pickups) == 1
    gold_coords = scene.cm.get_one(Coordinates, entity=gold_pickups[0].entity)
    assert (gold_coords.x, gold_coords.y) == (2, 3)


def test_death_listener_system_schedules_rebuild_on_die() -> None:
    scene = DummyScene()
    wall = 1
    root = 10
    house = HouseStructure(entity=root)
    scene.cm.add(
        house,
        ScheduleRebuild(entity=wall, root=root),
        Die(entity=wall),
    )

    run_death_listeners(scene)

    assert house.is_destroyed is True
