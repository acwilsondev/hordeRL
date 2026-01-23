from engine import core
from engine.components import Coordinates
from engine.components.entity import Entity
from engine.constants import PRIORITY_LOWEST
from horderl import palettes
from horderl.components import Appearance
from horderl.components.diggable import Diggable
from horderl.components.floodable import Floodable
from horderl.components.material import Material
from horderl.components.pathfinder_cost import PathfinderCost
from horderl.components.states.move_cost_affectors import (
    MoveCostAffector,
    MoveCostAffectorType,
)


def make_hole(x, y):
    entity_id = core.get_id()
    return (
        entity_id,
        [
            Entity(id=entity_id, entity=entity_id, name="hole"),
            Appearance(
                entity=entity_id,
                symbol="O",
                color=palettes.DIRT,
                bg_color=palettes.BACKGROUND,
            ),
            Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_LOWEST),
            Material(entity=entity_id, blocks=False, blocks_sight=False),
            Diggable(entity=entity_id),
            Floodable(entity=entity_id),
            MoveCostAffector(
                entity=entity_id,
                affector_type=MoveCostAffectorType.DIFFICULT_TERRAIN,
            ),
            PathfinderCost(entity=entity_id, cost=4),
        ],
    )
