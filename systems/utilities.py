from components import Coordinates, Brain
from components.enums import Intention
from components.events.turn_event import TurnEvent
from components.faction import Faction
from components.material import Material
from engine.component_manager import ComponentManager


def get_blocking_object(cm: ComponentManager, x: int, y: int) -> int:
    materials_at_coords = filter(
        lambda material: material and material.blocks,
        iter(
            cm.get_one(Material, coord.entity)
            for coord in cm.get(Coordinates)
            if (coord.x == x and coord.y == y)
        )
    )
    blocking_material = next(materials_at_coords, None)
    return blocking_material.entity if blocking_material else None


def set_intention(scene, entity, target, intention):
    brain = scene.cm.get_one(Brain, entity=entity)
    if brain:
        brain.intention = intention
        brain.intention_target = target


def retract_intention(scene, entity):
    set_intention(scene, entity, None, Intention.NONE)


def retract_turn(scene, entity: int):
    turn = scene.cm.get_one(TurnEvent, entity=entity)
    if turn:
        scene.cm.delete_component(turn)


def get_brains_with_intention(scene, intention):
    for brain in scene.cm.get(Brain):
        if brain.intention is intention:
            yield brain


def get_enemies(scene, entity):
    entity_faction = scene.cm.get_one(Faction, entity=entity)
    if not entity_faction:
        # entities without a faction cannot have enemies
        return []
    return [f.entity for f in scene.cm.get(Faction) if f.faction is not entity_faction.faction]


def get_enemies_in_range(scene, entity, min=0, max=1000):
    coords = scene.cm.get_one(Coordinates, entity)

    # get coordinates for each enemy
    enemies = get_enemies(scene, entity)
    enemy_coords = [scene.cm.get_one(Coordinates, entity=e) for e in enemies]

    # return filtered coordinates by distance < range
    return [
        enemy_coord.entity
        for enemy_coord in enemy_coords
        if min <= enemy_coord.distance_from(coords) <= max
    ]
