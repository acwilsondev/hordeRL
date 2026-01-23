from engine import core
from engine.components import Coordinates
from engine.components.entity import Entity
from engine.constants import PRIORITY_MEDIUM
from horderl import palettes
from horderl.components import Appearance, Attributes
from horderl.components.death_listeners.npc_corpse import Corpse
from horderl.components.faction import Faction
from horderl.components.material import Material
from horderl.components.pathfinder_cost import PathfinderCost
from horderl.components.sellable import Sellable
from horderl.systems.utilities import make_grow_into_tree


def make_sapling(x, y):
    entity_id = core.get_id()
    return (
        entity_id,
        [
            Entity(
                id=entity_id, entity=entity_id, name="sapling", static=True
            ),
            Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_MEDIUM),
            Attributes(entity=entity_id, hp=2, max_hp=2),
            Corpse(entity=entity_id, symbol="%", color=palettes.FOILAGE_C),
            Faction(entity=entity_id, faction=Faction.Options.PEASANT),
            Appearance(
                entity=entity_id,
                symbol="+",
                color=palettes.FOILAGE_C,
                bg_color=palettes.BACKGROUND,
            ),
            Material(entity=entity_id, blocks=True, blocks_sight=False),
            make_grow_into_tree(entity_id),
            PathfinderCost(entity=entity_id, cost=10),
            Sellable(entity=entity_id, value=1),
        ],
    )
