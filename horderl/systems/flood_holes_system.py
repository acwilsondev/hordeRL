from __future__ import annotations

from typing import Iterable, Optional, Tuple, TYPE_CHECKING

from engine import core
from engine.components import Coordinates

from horderl.components.floodable import Floodable
from horderl.components.flooder import Flooder
from horderl.components.tags.water_tag import WaterTag
from horderl.components.world_building.world_parameters import WorldParameters
from horderl.content.terrain.water import make_swampy_water, make_water

if TYPE_CHECKING:
    from horderl.components.flood_nearby_holes import FloodHolesController


def run(scene, controller: "FloodHolesController") -> None:
    """
    Advance hole flooding by a single throttled step.

    Args:
        scene: The active game scene that owns the component manager.
        controller: The FloodHolesController coordinating flood timing.

    Returns:
        None.

    Side Effects:
        Deletes flooded hole entities, spawns water tiles, updates flooder cooldowns,
        and advances the controller's energy timer.
    """
    if not controller.is_recharging:
        controller.pass_turn()
        return

    controller.flood_tick += 1
    floodables = scene.cm.get(Floodable)
    flooders = scene.cm.get(Flooder)

    if not floodables or not flooders:
        controller.is_recharging = False
        controller._log_debug("done filling available floodables")
        controller.pass_turn()
        return

    target = _select_flood_target(
        scene, floodables, flooders, controller.flood_tick
    )

    if target is None:
        if not _has_adjacent_flooder(scene, floodables, flooders):
            controller.is_recharging = False
            controller._log_debug("done filling available floodables")
        controller.pass_turn()
        return

    floodable, flooder = target
    painter = _select_painter(scene, flooder)
    _fill_hole(scene, floodable.entity, painter)
    flooder.next_flood_time = controller.flood_tick + flooder.flood_interval
    controller.pass_turn()


def _select_flood_target(
    scene,
    floodables: Iterable[Floodable],
    flooders: Iterable[Flooder],
    flood_tick: int,
) -> Optional[Tuple[Floodable, Flooder]]:
    for floodable in floodables:
        for flooder in flooders:
            if not _is_adjacent(scene, floodable.entity, flooder.entity):
                continue
            if flooder.next_flood_time > flood_tick:
                continue
            return floodable, flooder
    return None


def _has_adjacent_flooder(
    scene,
    floodables: Iterable[Floodable],
    flooders: Iterable[Flooder],
) -> bool:
    return any(
        _is_adjacent(scene, floodable.entity, flooder.entity)
        for floodable in floodables
        for flooder in flooders
    )


def _select_painter(scene, flooder: Flooder):
    water_tag = scene.cm.get_one(WaterTag, entity=flooder.entity)
    if water_tag and water_tag.is_dirty:
        return make_swampy_water
    return make_water


def _fill_hole(scene, hole, painter) -> None:
    world_params = scene.cm.get_one(
        WorldParameters, entity=core.get_id("world")
    )

    coordinates = scene.cm.get_one(Coordinates, entity=hole)
    if not coordinates:
        return
    scene.cm.delete(hole)
    water = painter(
        coordinates.x, coordinates.y, rapidness=world_params.river_rapids
    )
    scene.cm.add(*water[1])


def _is_adjacent(scene, first: int, second: int) -> bool:
    first_coord: Coordinates = scene.cm.get_one(Coordinates, entity=first)
    second_coord: Coordinates = scene.cm.get_one(Coordinates, entity=second)
    return (
        first_coord
        and second_coord
        and first_coord.distance_from(second_coord) <= 1
    )
