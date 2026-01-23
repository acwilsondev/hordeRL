import random

from engine import core
from engine.components import Coordinates
from engine.components.component import Component
from engine.components.entity import Entity
from engine.constants import PRIORITY_LOWEST
from horderl import palettes
from horderl.components import Appearance
from horderl.components.death_listeners.drop_gold import DropGold
from horderl.components.diggable import Diggable
from horderl.components.material import Material
from horderl.components.pathfinder_cost import PathfinderCost
from horderl.components.states.move_cost_affectors import (
    MoveCostAffector,
    MoveCostAffectorType,
)


def make_rock(x, y):
    entity_id = core.get_id()
    appearance = random.choice(["%", '"', "'", "."])
    entity: tuple[int, list[Component]] = (
        entity_id,
        [
            Entity(id=entity_id, entity=entity_id, name="rock", static=True),
            Appearance(
                entity=entity_id,
                symbol=appearance,
                color=palettes.STONE,
                bg_color=palettes.BACKGROUND,
            ),
            Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_LOWEST),
            Material(entity=entity_id, blocks=False, blocks_sight=False),
            MoveCostAffector(
                entity=entity_id,
                affector_type=MoveCostAffectorType.DIFFICULT_TERRAIN,
            ),
            Diggable(entity=entity_id),
            PathfinderCost(entity=entity_id, cost=4),
        ],
    )
    if random.randint(1, 20) == 1:
        entity[1].append(DropGold(entity=entity_id))
    return entity
