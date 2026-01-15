from engine import core
from engine.component_manager import ComponentManager
from engine.components import Coordinates

from horderl.components.flood_nearby_holes import FloodHolesController
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
    controller = FloodHolesController(entity=1, is_recharging=True)
    flooder_id = 2
    hole_id = 3

    scene.cm.add(
        WorldParameters(entity=world_id, river_rapids=1),
        Coordinates(entity=flooder_id, x=0, y=0),
        Flooder(entity=flooder_id, flood_interval=2),
        WaterTag(entity=flooder_id, is_dirty=False),
        Coordinates(entity=hole_id, x=1, y=0),
        Floodable(entity=hole_id),
    )

    run_flood_holes(scene, controller)

    assert scene.cm.get(Floodable) == []
    updated_flooder = scene.cm.get_one(Flooder, entity=flooder_id)
    assert (
        updated_flooder.next_flood_time
        == controller.flood_tick + updated_flooder.flood_interval
    )


def test_flood_holes_system_stops_when_no_adjacent_flooders():
    scene = DummyScene()
    controller = FloodHolesController(entity=1, is_recharging=True)
    flooder_id = 2
    hole_id = 3

    scene.cm.add(
        Coordinates(entity=flooder_id, x=0, y=0),
        Flooder(entity=flooder_id, flood_interval=1),
        WaterTag(entity=flooder_id, is_dirty=False),
        Coordinates(entity=hole_id, x=5, y=5),
        Floodable(entity=hole_id),
    )

    run_flood_holes(scene, controller)

    assert controller.is_recharging is False
    assert scene.cm.get(Floodable)
