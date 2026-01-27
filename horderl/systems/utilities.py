import random

from engine import core
from engine.component_manager import ComponentManager
from engine.components import Actor, Coordinates
from engine.logging import get_logger

from ..components.events.turn_event import TurnEvent
from ..components.faction import Faction
from ..components.material import Material
from ..components.season_reset_listeners.grow_in_spring import GrowIntoTree
from ..components.world_turns import WorldTurns


def get_blocking_object(cm: ComponentManager, x: int, y: int) -> int:
    """
    Find the first blocking material at the given coordinates.

    Args:
        cm (ComponentManager): Component manager to query.
        x (int): X coordinate to inspect.
        y (int): Y coordinate to inspect.

    Returns:
        int | None: Entity id for the blocking material, or None if none exists.
    """
    materials_at_coords = filter(
        lambda material: material and material.blocks,
        iter(
            cm.get_one(Material, coord.entity)
            for coord in cm.get(Coordinates)
            if (coord.x == x and coord.y == y)
        ),
    )

    blocking_material = next(materials_at_coords, None)
    return blocking_material.entity if blocking_material else None


def get_current_turn(scene) -> int:
    """
    Return the current world turn count.

    Args:
        scene: Active scene containing the component manager.

    Returns:
        int: The current world turn count, or 0 if the component is missing.

    Side Effects:
        - None.
    """
    world_turns = scene.cm.get_one(WorldTurns, entity=core.get_id("world"))
    return world_turns.current_turn if world_turns else 0


def retract_turn(scene, entity: int):
    """
    Remove a pending TurnEvent for an entity, if present.

    Args:
        scene: Active scene containing component manager.
        entity (int): Entity id whose TurnEvent should be removed.

    Side Effects:
        - Deletes a TurnEvent component from the component manager.
    """
    logger = get_logger(__name__)
    logger.debug(
        "Retracting turn event",
        extra={"entity": entity},
    )
    turn = scene.cm.get_one(TurnEvent, entity=entity)
    if turn:
        scene.cm.delete_component(turn)


def get_actors_with_intention(scene, intention):
    """
    Yield actors matching a specific intention.

    Args:
        scene: Active scene containing component manager.
        intention: Intention value to match.

    Yields:
        Actor: Actor components with the matching intention.
    """
    for actor in scene.cm.get(Actor):
        if actor.intention is intention:
            yield actor


def get_enemies(scene, entity):
    """
    Get entities that are in a different faction than the provided entity.

    Args:
        scene: Active scene containing component manager.
        entity (int): Entity id to compare factions against.

    Returns:
        list[int]: Entity ids considered enemies.
    """
    entity_faction = scene.cm.get_one(Faction, entity=entity)
    if not entity_faction:
        # entities without a faction cannot have enemies
        return []
    return [
        f.entity
        for f in scene.cm.get(Faction)
        if f.faction != entity_faction.faction
    ]


def get_enemies_in_range(scene, entity, min_range=0, max_range=1000):
    """
    Return enemy entities within the specified distance range.

    Args:
        scene: Active scene containing component manager.
        entity (int): Entity id used as the distance origin.
        min_range (int): Minimum inclusive range.
        max_range (int): Maximum inclusive range.

    Returns:
        list[int]: Enemy entity ids within the distance range.
    """
    coords = scene.cm.get_one(Coordinates, entity)

    # get coordinates for each enemy
    enemies = get_enemies(scene, entity)
    enemy_coords = [scene.cm.get_one(Coordinates, entity=e) for e in enemies]

    # return filtered coordinates by distance < range
    return [
        enemy_coord.entity
        for enemy_coord in enemy_coords
        if min_range <= enemy_coord.distance_from(coords) <= max_range
    ]


def make_grow_into_tree(entity: int) -> GrowIntoTree:
    """
    Create a GrowIntoTree component with a randomized grow timer.

    Args:
        entity (int): Entity ID that will own the component.

    Returns:
        GrowIntoTree: Component with time_to_grow initialized.

    Side Effects:
        - None.
    """
    return GrowIntoTree(entity=entity, time_to_grow=random.randint(1200, 3600))
