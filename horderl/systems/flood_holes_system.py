from __future__ import annotations

from typing import Iterable, Optional, Tuple

from engine import core
from engine.components import Coordinates

from horderl.components.events.hole_dug_events import HoleDug
from horderl.components.flood_nearby_holes import FloodHolesState
from horderl.components.floodable import Floodable
from horderl.components.flooder import Flooder
from horderl.components.tags.water_tag import WaterTag
from horderl.components.world_building.world_parameters import WorldParameters
from horderl.content.terrain.water import make_swampy_water, make_water


def run(scene) -> None:
    """
    Advance hole flooding by a single throttled step.

    Args:
        scene: The active game scene that owns the component manager.

    Returns:
        None.

    Side Effects:
        Deletes flooded hole entities, spawns water tiles, updates flooder cooldowns,
        and advances the controller's timing window.
    """
    states = scene.cm.get(FloodHolesState)
    if not states:
        return

    if scene.cm.get(HoleDug):
        for state in states:
            state.is_active = True

    now_ms = core.time_ms()
    floodables = scene.cm.get(Floodable)
    flooders = scene.cm.get(Flooder)

    for state in states:
        if not state.is_active:
            continue
        if state.next_step_time_ms and now_ms < state.next_step_time_ms:
            continue

        if not floodables or not flooders:
            state.is_active = False
            continue

        target = _select_flood_target(
            scene, floodables, flooders, now_ms
        )

        if target is None:
            if not _has_adjacent_flooder(scene, floodables, flooders):
                state.is_active = False
            continue

        floodable, flooder = target
        painter = _select_painter(scene, flooder)
        _fill_hole(scene, floodable.entity, painter)
        flooder.next_flood_time_ms = now_ms + flooder.flood_interval_ms
        state.next_step_time_ms = now_ms + state.step_delay_ms


def _select_flood_target(
    scene,
    floodables: Iterable[Floodable],
    flooders: Iterable[Flooder],
    now_ms: int,
) -> Optional[Tuple[Floodable, Flooder]]:
    for floodable in floodables:
        for flooder in flooders:
            if not _is_adjacent(scene, floodable.entity, flooder.entity):
                continue
            if flooder.next_flood_time_ms > now_ms:
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
