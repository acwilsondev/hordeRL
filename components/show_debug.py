import logging
import os
from dataclasses import dataclass

import engine
import settings
from components import Attributes, Coordinates, Senses
from components.abilities.build_wall_ability import BuildWallAbility
from components.base_components.energy_actor import EnergyActor
from components.base_components.entity import Entity
from components.brains.brain import Brain
from components.brains.default_active_actor import DefaultActiveActor
from components.brains.painters.create_gold_actor import PlaceGoldController
from components.brains.painters.create_hordeling_actor import \
    PlaceHordelingController
from components.events.die_events import Die
from components.pathfinding.breadcrumb_tracker import BreadcrumbTracker
from components.serialization.load_game import LoadGame
from components.serialization.save_game import SaveGame
from components.wrath_effect import WrathEffect
from content.cursor import make_cursor
from content.farmsteads.houses import place_farmstead
from content.terrain.roads import connect_point_to_road_network
from gui.easy_menu import EasyMenu

"""
This module provides debugging tools and a debug menu system for the game.

It contains a ShowDebug component that creates a menu with various debug options
for testing, development, and debugging purposes. The module also includes all the
individual debug functions that can be used to modify game state, inspect entities,
manipulate the player character, and test various game systems.

NOTE: These functions are intended for development use only and should not be
accessible in production builds.
"""


@dataclass
class ShowDebug(EnergyActor):
    """
    A debug menu component that provides access to various debugging tools and options.

    This component inherits from EnergyActor and consumes zero energy (INSTANT) when activated,
    making it suitable for debug operations that shouldn't affect game balance. When activated,
    it displays a menu with various debug options that allow developers to:

    - Examine game objects and their components
    - Manipulate player attributes (health, gold)
    - Place entities in the world (hordelings, gold)
    - Test special effects (wrath)
    - Manipulate the player (teleport, suicide)
    - Toggle gameplay abilities (masonry)
    - Visualize pathfinding
    - Generate content (farmsteads)
    - Save game state

    The component self-destructs after displaying the menu to avoid multiple instances.

    Attributes:
        energy_cost (int): The energy cost for activating this component, set to
                          INSTANT (zero) to avoid affecting gameplay timing.
    """

    energy_cost: int = EnergyActor.INSTANT

    def act(self, scene):
        """
        Display the debug menu and remove this component from the entity.

        This method creates an EasyMenu with various debug options and adds it to the
        scene's GUI. Each menu option is linked to a specific debug function. After
        displaying the menu, the component removes itself from the component manager.

        Args:
            scene: The current game scene containing the GUI and component manager.
        """
        scene.gui.add_element(
            EasyMenu(
                "Debug Options",
                {
                    "examine game objects": get_examine_game_objects(scene),
                    "heal": get_heal(scene),
                    "get rich": get_rich(scene),
                    "place hordeling": get_painter(scene, PlaceHordelingController),
                    "place gold": get_painter(scene, PlaceGoldController),
                    "wrath": get_wrath(scene, self.entity),
                    "suicide": get_suicide(scene),
                    "teleport to": get_teleport_to(scene),
                    "toggle ability": get_toggle_masonry(scene),
                    "toggle pathing": get_pathfinding_for(scene),
                    "spawn a home": get_spawn_home(scene),
                    "quicksave": quick_save(scene),
                },
                settings.INVENTORY_WIDTH,
            )
        )
        scene.cm.delete_component(self)


# Entity Inspection Functions
# ---------------------------------


def get_examine_game_objects(scene):
    """
    Create a function that displays a menu of all non-static game entities for inspection.

    This debug function retrieves all non-static entities in the scene, sorts them by ID,
    and displays them in a menu. When an entity is selected from the menu, its details
    are displayed using the get_examine_object function.

    Args:
        scene: The current game scene containing entities and the GUI system.

    Returns:
        function: A callback function that displays the entity selection menu when invoked.
    """

    def out_fn():
        entities = scene.cm.get(Entity)
        entities = [e for e in entities if not e.static]
        entities = sorted(entities, key=lambda e: e.id)
        scene.gui.add_element(
            EasyMenu(
                "Examine which?",
                {
                    entity.get_readable_key(): get_examine_object(scene, entity.entity)
                    for entity in entities
                },
                settings.INVENTORY_WIDTH,
            )
        )

    return out_fn


def get_examine_object(scene, entity):
    """
    Create a function that prints detailed information about a specific entity.

    This debug function retrieves all components attached to the specified entity
    and prints them to the console for inspection. It's useful for debugging entity
    composition and component state.

    Args:
        scene: The current game scene containing the component manager.
        entity: The entity ID to examine.

    Returns:
        function: A callback function that prints entity details when invoked.
    """

    def out_fn():
        entity_blob = scene.cm.get_entity(entity)
        entity_component = entity_blob[Entity][0]
        print(f"Debug Show Item: {entity_component.name}")

        components = []

        for _, values in entity_blob.items():
            for component in values:
                if component not in components:
                    components.append(component)
        for component in components:
            print(f"\t{component}")

    return out_fn


# Player Modification Functions
# -----------------------------


def get_heal(scene):
    """
    Create a function that fully heals the player character.

    This debug function finds the player's Attributes component and sets their
    current HP to their maximum HP, effectively healing them completely.

    Args:
        scene: The current game scene containing the component manager.

    Returns:
        function: A callback function that heals the player when invoked.
    """

    def out_fn():
        health = scene.cm.get_one(Attributes, entity=engine.constants.PLAYER_ID)
        if health:
            health.hp = health.max_hp

    return out_fn


def get_painter(scene, painter):
    """
    Create a function that switches player control to a painting mode for placing entities.

    This debug function creates a cursor at the player's position and switches the player's
    brain controller to the specified painter controller, allowing them to place entities
    in the game world. The original controller is stashed for later restoration.

    Args:
        scene: The current game scene containing the component manager.
        painter: The painter controller class to use (e.g., PlaceHordelingController).

    Returns:
        function: A callback function that activates the painter mode when invoked.
    """

    def out_fn():
        coords = scene.cm.get_one(Coordinates, entity=scene.player)
        cursor = make_cursor(coords.x, coords.y)
        scene.cm.add(*cursor[1])
        player_controller = scene.cm.get_one(Brain, entity=scene.player)
        new_controller = painter(
            entity=scene.player, old_actor=player_controller.id, cursor=cursor[0]
        )
        scene.cm.stash_component(player_controller.id)
        scene.cm.add(new_controller)

    return out_fn


def place_gold(scene):
    """
    Create a function that switches player control to gold placement mode.

    This debug function is a specific implementation of the get_painter function
    that uses the PlaceGoldController. It's maintained for backward compatibility
    but has the same functionality as get_painter(scene, PlaceGoldController).

    Args:
        scene: The current game scene containing the component manager.

    Returns:
        function: A callback function that activates gold placement mode when invoked.
    """

    def out_fn():
        coords = scene.cm.get_one(Coordinates, entity=scene.player)
        cursor = make_cursor(coords.x, coords.y)


def get_rich(scene):
    """
    Create a function that gives the player a large sum of gold.

    This debug function adds 100 gold to the player's current gold amount,
    allowing for testing of gold-dependent game mechanics without grinding.

    Args:
        scene: The current game scene containing the gold counter.

    Returns:
        function: A callback function that adds gold when invoked.
    """

    def out_fn():
        scene.gold += 100

    return out_fn


def get_suicide(scene):
    """
    Create a function that instantly kills the player character.

    This debug function adds a Die component to the player, triggering the death
    event system and allowing testing of player death mechanics without combat.

    Args:
        scene: The current game scene containing the component manager.

    Returns:
        function: A callback function that kills the player when invoked.
    """

    def out_fn():
        scene.cm.add(Die(entity=scene.player))

    return out_fn


# Movement and Teleportation Functions
# -------------------------------------


def get_teleport_to(scene):
    """
    Create a function that displays a menu of entities to teleport to.

    This debug function presents a list of all non-static entities in the game
    and allows the player to select one to teleport to. When an entity is selected,
    the get_teleport_to_entity function is called with that entity as the target.

    Args:
        scene: The current game scene containing the entities and GUI system.

    Returns:
        function: A callback function that displays the teleport menu when invoked.
    """

    def out_fn():
        entities = scene.cm.get(Entity)
        entities = [e for e in entities if not e.static]
        entities = sorted(entities, key=lambda e: e.id)
        scene.gui.add_element(
            EasyMenu(
                "Teleport to which entity?",
                {
                    entity.get_readable_key(): get_teleport_to_entity(
                        scene, entity.entity
                    )
                    for entity in entities
                },
                settings.INVENTORY_WIDTH,
            )
        )

    return out_fn


def get_teleport_to_entity(scene, entity):
    """
    Create a function that teleports the player to a specific entity's position.

    This debug function moves the player character to the same coordinates as the
    target entity and marks the player's senses as dirty to force a FOV update.

    Args:
        scene: The current game scene containing the component manager.
        entity: The target entity ID to teleport to.

    Returns:
        function: A callback function that teleports the player when invoked.
    """

    def out_fn():
        target_coords = scene.cm.get_one(Coordinates, entity=entity)
        if target_coords:
            player_coords = scene.cm.get_one(
                Coordinates, entity=engine.constants.PLAYER_ID
            )
            player_coords.x = target_coords.x
            player_coords.y = target_coords.y
            senses = scene.cm.get_one(Senses, entity=engine.constants.PLAYER_ID)
            senses.dirty = True

    return out_fn


# Special Effects and Abilities Functions
# ---------------------------------------


def get_wrath(scene, entity):
    """
    Create a function that triggers the wrath effect on a specified entity.

    This debug function adds a WrathEffect component to the specified entity,
    which typically creates a powerful destructive effect useful for testing
    damage mechanics and environmental interactions.

    Args:
        scene: The current game scene containing the component manager.
        entity: The entity ID to apply the wrath effect to.

    Returns:
        function: A callback function that triggers the wrath effect when invoked.
    """

    def out_fn():
        scene.cm.add(WrathEffect(entity=entity))

    return out_fn


def get_activate_ability(scene):
    """
    Create a function that displays a menu of abilities to toggle.

    This debug function presents a list of abilities that can be toggled on or off
    for the player character. It marks active abilities with an 'X'. Currently, it
    only supports the Masonry ability but is designed to be expandable.

    Args:
        scene: The current game scene containing the component manager and GUI system.

    Returns:
        function: A callback function that displays the ability toggle menu when invoked.
    """

    def out_fn():
        ability_map = {}

        has_masonry = scene.cm.get_one(BuildWallAbility, entity=scene.player)
        ability_map[f"Masonry ({'X' if has_masonry else ' '})"] = get_toggle_masonry(
            scene
        )

        scene.gui.add_element(
            EasyMenu(
                "Toggle which ability?",
                ability_map,
                settings.INVENTORY_WIDTH,
            )
        )

    return out_fn


def get_toggle_masonry(scene):
    """
    Create a function that toggles the masonry (wall building) ability for the player.

    This debug function checks if the player has the BuildWallAbility component
    and toggles its presence - removing it if present or adding it if not present.
    This allows testing of building mechanics without requiring normal progression.

    Args:
        scene: The current game scene containing the component manager.

    Returns:
        function: A callback function that toggles the masonry ability when invoked.
    """

    def out_fn():
        ability = scene.cm.get_one(BuildWallAbility, entity=scene.player)
        if ability:
            logging.info("Enabling Masonry")
            scene.cm.delete_component(ability)
        else:
            logging.info("Disabling Masonry")
            scene.cm.add(BuildWallAbility(entity=scene.player))

    return out_fn


# Debug Visualization Functions
# -------------------------------


def get_pathfinding_for(scene):
    """
    Create a function that displays a menu of entities to visualize pathfinding for.

    This debug function presents a list of all active actors in the game and allows
    the developer to select one to toggle pathfinding visualization for. The function
    filters for DefaultActiveActor components to find entities that use pathfinding.

    Args:
        scene: The current game scene containing the component manager and GUI system.

    Returns:
        function: A callback function that displays the pathfinding menu when invoked.
    """

    def out_fn():
        actors = scene.cm.get(DefaultActiveActor)
        entities = [scene.cm.get_one(Entity, entity=e.entity) for e in actors]
        entities = sorted(entities, key=lambda e: e.id)
        scene.gui.add_element(
            EasyMenu(
                "Toggle pathfinding for which?",
                {
                    entity.get_readable_key(): get_show_pathing(scene, entity.entity)
                    for entity in entities
                },
                settings.INVENTORY_WIDTH,
            )
        )

    return out_fn


def get_show_pathing(scene, entity):
    """
    Create a function that toggles pathfinding visualization for a specific entity.

    This debug function checks if the entity has a BreadcrumbTracker component and
    toggles its presence - removing it if present or adding it if not present.
    BreadcrumbTracker visually displays the path that an entity is following.

    Args:
        scene: The current game scene containing the component manager.
        entity: The entity ID to toggle pathfinding visualization for.

    Returns:
        function: A callback function that toggles pathfinding visualization when invoked.
    """

    def out_fn():
        tracker = scene.cm.get_one(BreadcrumbTracker, entity=entity)
        if tracker:
            scene.cm.delete_component(tracker)
        else:
            scene.cm.add(BreadcrumbTracker(entity=entity))

    return out_fn


# World Generation Functions
# ----------------------------


def get_spawn_home(scene):
    """
    Create a function that spawns a new farmstead in the game world.

    This debug function creates a complete farmstead at a suitable location and
    connects it to the existing road network. This allows testing of farmstead
    interactions and town expansion without waiting for normal game progression.

    Args:
        scene: The current game scene containing the component manager.

    Returns:
        function: A callback function that spawns a farmstead when invoked.
    """

    def out_fn():
        farmstead_id = place_farmstead(scene)
        farmstead_point = scene.cm.get_one(Coordinates, entity=farmstead_id).position
        connect_point_to_road_network(scene, farmstead_point, trim_start=2)

    return out_fn


def quick_save(scene):
    """
    Create a function that triggers an immediate game save.

    This debug function adds a SaveGame component to the player entity, which
    initiates the game saving process without requiring normal save triggers like
    entering a building or completing a quest. This allows testing of save/load
    functionality at any point during gameplay.

    Args:
        scene: The current game scene containing the component manager.

    Returns:
        function: A callback function that saves the game when invoked.
    """

    def out_fn():
        scene.cm.add(SaveGame(entity=scene.player))

    return out_fn
