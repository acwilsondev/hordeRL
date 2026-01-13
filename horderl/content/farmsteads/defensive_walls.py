from horderl import palettes
from horderl.components import Appearance, Attributes, Coordinates
from horderl.components.death_listeners.npc_corpse import Corpse
from horderl.components.faction import Faction
from horderl.components.material import Material
from horderl.components.pathfinder_cost import PathfinderCost
from horderl.components.sellable import Sellable
from horderl.components.structure import Structure
from horderl.engine import core
from horderl.engine.components.entity import Entity
from horderl.engine.constants import PRIORITY_MEDIUM


def make_fence(x, y):
    entity_id = core.get_id()
    return (
        entity_id,
        [
            Entity(id=entity_id, entity=entity_id, name="fence"),
            Appearance(
                entity=entity_id,
                symbol="o",
                color=palettes.WOOD,
                bg_color=palettes.BACKGROUND,
            ),
            Corpse(
                entity=entity_id,
                symbol="%",
                color=palettes.WOOD,
                bg_color=palettes.BACKGROUND,
            ),
            Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_MEDIUM),
            Attributes(entity=entity_id, hp=10, max_hp=10),
            Faction(entity=entity_id, faction=Faction.Options.PEASANT),
            Material(entity=entity_id, blocks=True, blocks_sight=False),
            PathfinderCost(entity=entity_id, cost=20),
            Structure(entity=entity_id),
            Sellable(entity=entity_id, value=2),
        ],
    )


def make_stone_wall(x, y):
    entity_id = core.get_id()
    return (
        entity_id,
        [
            Entity(id=entity_id, entity=entity_id, name="stone wall"),
            Appearance(
                entity=entity_id,
                symbol="o",
                color=palettes.STONE,
                bg_color=palettes.BACKGROUND,
            ),
            Corpse(
                entity=entity_id,
                symbol="%",
                color=palettes.STONE,
                bg_color=palettes.BACKGROUND,
            ),
            Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_MEDIUM),
            Attributes(entity=entity_id, hp=20, max_hp=20),
            Faction(entity=entity_id, faction=Faction.Options.PEASANT),
            Material(entity=entity_id, blocks=True, blocks_sight=True),
            PathfinderCost(entity=entity_id, cost=40),
            Structure(entity=entity_id),
            Sellable(entity=entity_id, value=5),
        ],
    )
