from engine import core
from engine.component_manager import ComponentManager
from engine.components import Coordinates
from horderl.components.flood_nearby_holes import FloodHolesState
from horderl.components.floodable import Floodable
from horderl.components.flooder import Flooder
from horderl.components.tags.water_tag import WaterTag
from horderl.components.world_building.world_parameters import WorldParameters
from horderl.systems.flood_holes_system import run as run_flood_holes


class DummyScene:
    def __init__(self):
        self.cm = ComponentManager()


def test_flood_holes_system_fills_one_hole_and_sets_cooldown():
    scene = DummyScene()
    world_id = core.get_id("world")
    state = FloodHolesState(entity=1, is_active=True, step_delay_ms=0)
    flooder_id = 2
    hole_id = 3

    scene.cm.add(
        WorldParameters(entity=world_id, river_rapids=1),
        state,
        Coordinates(entity=flooder_id, x=0, y=0),
        Flooder(entity=flooder_id, flood_interval_ms=0),
        WaterTag(entity=flooder_id, is_dirty=False),
        Coordinates(entity=hole_id, x=1, y=0),
        Floodable(entity=hole_id),
    )

    run_flood_holes(scene)

    assert scene.cm.get(Floodable) == []
    updated_flooder = scene.cm.get_one(Flooder, entity=flooder_id)
    assert updated_flooder.next_flood_time_ms >= 0


def test_flood_holes_system_does_not_stop_when_no_adjacent_flooders():
    scene = DummyScene()
    state = FloodHolesState(entity=1, is_active=True, step_delay_ms=0)
    flooder_id = 2
    hole_id = 3

    scene.cm.add(
        state,
        Coordinates(entity=flooder_id, x=0, y=0),
        Flooder(entity=flooder_id, flood_interval_ms=0),
        WaterTag(entity=flooder_id, is_dirty=False),
        Coordinates(entity=hole_id, x=5, y=5),
        Floodable(entity=hole_id),
    )

    run_flood_holes(scene)

    assert state.is_active is True
    assert scene.cm.get(Floodable)
