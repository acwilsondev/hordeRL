import engine
import settings
from components import Entity, Coordinates, Attributes, Senses
from components.actors.actor import Actor
from components.enums import Intention
from gui.easy_menu import EasyMenu
from systems.utilities import retract_intention


def run(scene):
    for actor in [b for b in scene.cm.get(Actor) if b.intention is Intention.SHOW_DEBUG_SCREEN]:
        scene.gui.add_element(
            EasyMenu(
                "Debug Options",
                {
                    "examine game objects": get_examine_game_objects(scene),
                    "heal": get_heal(scene),
                    "suicide": get_suicide(scene),
                    "teleport to": get_teleport_to(scene)
                },
                settings.INVENTORY_WIDTH,
            )
        )
        retract_intention(scene, actor.entity)


def get_examine_game_objects(scene):
    def out_fn():
        entities = scene.cm.get(Entity)
        entities = [e for e in entities if not e.static]
        entities = sorted(entities, key=lambda e: e.id)
        scene.gui.add_element(
            EasyMenu(
                "Examine which?",
                {entity.get_readable_key(): get_examine_object(scene, entity.entity) for entity in entities},
                settings.INVENTORY_WIDTH,
            )
        )
    return out_fn


def get_examine_object(scene, entity):
    def out_fn():
        entity_blob = scene.cm.get_entity(entity)
        entity_component = entity_blob[Entity][0]
        print(f'Debug Show Item: {entity_component.name}')
        
        for _, values in entity_blob.items():
            for component in values:
                print(f'\t{component}')
    return out_fn


def get_heal(scene):
    def out_fn():
        health = scene.cm.get_one(Attributes, entity=engine.constants.PLAYER_ID)
        if health:
            health.hp = health.max_hp
    return out_fn


def get_suicide(scene):
    def out_fn():
        health = scene.cm.get_one(Attributes, entity=engine.constants.PLAYER_ID)
        if health:
            health.hp = 0
    return out_fn


def get_teleport_to(scene):
    def out_fn():
        entities = scene.cm.get(Entity)
        entities = [e for e in entities if not e.static]
        entities = sorted(entities, key=lambda e: e.id)
        scene.gui.add_element(
            EasyMenu(
                "Examine which?",
                {entity.get_readable_key(): get_teleport_to_entity(scene, entity.id) for entity in entities},
                settings.INVENTORY_WIDTH,
            )
        )
    return out_fn


def get_teleport_to_entity(scene, entity):
    def out_fn():
        target_coords = scene.cm.get_one(Coordinates, entity=entity)
        if target_coords:
            player_coords = scene.cm.get_one(Coordinates, entity=engine.constants.PLAYER_ID)
            player_coords.x = target_coords.x
            player_coords.y = target_coords.y
            senses = scene.cm.get_one(Senses, entity=engine.constants.PLAYER_ID)
            senses.dirty = True
    return out_fn
