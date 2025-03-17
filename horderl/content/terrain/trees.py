"""
This module defines tree entities that can be placed in the game world.

It provides factory functions to create different types of trees with their appropriate
components, appearances, and behaviors.

"""

from horderl.components import Appearance, Attributes, Coordinates
from horderl.components.base_components.entity import Entity
from horderl.components.death_listeners.npc_corpse import Corpse
from horderl.components.death_listeners.terrain_changes_on_death import (
    TerrainChangedOnDeath,
)
from horderl.components.faction import Faction
from horderl.components.material import Material
from horderl.components.pathfinder_cost import PathfinderCost
from horderl.components.sellable import Sellable
from horderl.components.tags.tree_tag import TreeTag
from horderl.components.tree_cut_on_die import TreeCutOnDeath
from horderl.engine import core, palettes
from horderl.engine.constants import PRIORITY_MEDIUM

wall_tree_description = (
    "This hardy species of Toshim tree towers over the village. "
    "You won't be able to cut this one down."
)


def make_wall_tree(x, y):
    """
    Creates a hardy tree entity that serves as an impassable boundary.

    This tree is static, blocks movement and vision, and cannot be cut down.
    It's typically used for creating natural walls or boundaries in the game world.

    Parameters:
        x (int): The x-coordinate where the tree will be placed
        y (int): The y-coordinate where the tree will be placed

    Returns:
        tuple: A tuple containing (entity_id, component_list) where:
            - entity_id (int): The unique identifier for this tree entity
            - component_list (list): A list of components that define the tree's behavior

    """
    entity_id = core.get_id()
    return (
        entity_id,
        [
            Entity(
                id=entity_id,
                entity=entity_id,
                name="hardy tree",
                static=True,
                description=wall_tree_description,
            ),
            Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_MEDIUM),
            Appearance(
                entity=entity_id,
                symbol="♣",
                color=palettes.WALL_TREE,
                bg_color=palettes.BACKGROUND,
            ),
            Material(entity=entity_id, blocks=True, blocks_sight=True),
            PathfinderCost(entity=entity_id, cost=100),
        ],
    )


tree_description = (
    "A tree of the Toshim Plains. You can chop it down to sell its valuable wood."
)


def make_tree(x, y):
    """
    Creates a standard tree entity that can be chopped down and sold.

    Unlike wall trees, these trees can be harvested by the player for wood,
    which can then be sold for currency. They have health points, can be damaged,
    and leave behind a corpse when destroyed.

    Parameters:
        x (int): The x-coordinate where the tree will be placed
        y (int): The y-coordinate where the tree will be placed

    Returns:
        tuple: A tuple containing (entity_id, component_list) where:
            - entity_id (int): The unique identifier for this tree entity
            - component_list (list): A list of components that define the tree's behavior,
              including Attributes for health, TreeTag for identification, and components
              for handling what happens when the tree is cut down

    """
    entity_id = core.get_id()
    return (
        entity_id,
        [
            Entity(
                id=entity_id,
                entity=entity_id,
                name="tree",
                static=True,
                description=tree_description,
            ),
            Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_MEDIUM),
            Attributes(entity=entity_id, hp=5, max_hp=5),
            Corpse(entity=entity_id, symbol="%", color=palettes.WOOD),
            Faction(entity=entity_id, faction=Faction.Options.PEASANT),
            Appearance(
                entity=entity_id,
                symbol="♣",
                color=palettes.FOILAGE_C,
                bg_color=palettes.BACKGROUND,
            ),
            Material(entity=entity_id, blocks=True, blocks_sight=True),
            TreeTag(entity=entity_id),
            TerrainChangedOnDeath(entity=entity_id),
            Sellable(entity=entity_id, value=2),
            PathfinderCost(entity=entity_id, cost=20),
            TreeCutOnDeath(entity=entity_id),
        ],
    )
