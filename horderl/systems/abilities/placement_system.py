"""System for spawning placement entities from placement actors."""

from __future__ import annotations

from typing import Callable, Iterable

from engine.components.component import Component
from engine.logging import get_logger
from horderl.components.brains.ability_actors.place_thing_actor import (
    PlaceThingActor,
)
from horderl.content.allies.knights import make_knight
from horderl.content.bomb import make_bomb
from horderl.content.cows import make_cow
from horderl.content.farmsteads.defensive_walls import (
    make_fence,
    make_stone_wall,
)
from horderl.content.haunch import make_haunch
from horderl.content.spike_trap import make_spike_trap
from horderl.content.terrain.saplings import make_sapling

PlacementFactory = Callable[[int, int], tuple[int, Iterable[Component]]]

_PLACEMENT_FACTORIES: dict[str, PlacementFactory] = {
    "bomb": make_bomb,
    "cow": make_cow,
    "fence": make_fence,
    "haunch": make_haunch,
    "knight": make_knight,
    "sapling": make_sapling,
    "spike_trap": make_spike_trap,
    "stone_wall": make_stone_wall,
}


def place(scene, brain: PlaceThingActor, x: int, y: int) -> int | None:
    """
    Spawn and attach components for a placement actor at a target position.

    Args:
        scene: Active scene containing a component manager.
        brain: Placement actor describing what to spawn.
        x: Target X coordinate for the new entity.
        y: Target Y coordinate for the new entity.

    Returns:
        The entity ID that was created, or None if no spawn key matched.

    Side Effects:
        - Adds components for the spawned entity to the scene component manager.
        - Logs a warning when a placement key is not recognized.
    """
    factory = _PLACEMENT_FACTORIES.get(brain.spawn_key)
    if factory is None:
        logger = get_logger(__name__)
        logger.warning(
            "Unknown placement spawn key",
            extra={"spawn_key": brain.spawn_key, "entity": brain.entity},
        )
        return None

    entity_id, components = factory(x, y)
    scene.cm.add(*components)
    return entity_id
