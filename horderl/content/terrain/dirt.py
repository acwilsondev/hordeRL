import random

from engine import core
from engine.components import Coordinates
from engine.components.component import Component
from engine.components.entity import Entity
from engine.constants import PRIORITY_LOWEST
from horderl import palettes
from horderl.components import Appearance
from horderl.components.diggable import Diggable
from horderl.components.material import Material
from horderl.components.season_reset_listeners.grow_grass import GrowGrass


def make_dirt(x, y):
    entity_id = core.get_id()
    appearance = '"' if random.random() < 0.5 else "'"
    entity: tuple[int, list[Component]] = (
        entity_id,
        [
            Entity(id=entity_id, entity=entity_id, name="dirt", static=True),
            Appearance(
                entity=entity_id,
                symbol=appearance,
                color=palettes.DIRT,
                bg_color=palettes.BACKGROUND,
            ),
            Coordinates(
                entity=entity_id,
                x=x,
                y=y,
                priority=PRIORITY_LOWEST,
                buildable=True,
            ),
            Material(entity=entity_id, blocks=False, blocks_sight=False),
            Diggable(entity=entity_id, is_free=True),
            GrowGrass(entity=entity_id),
        ],
    )
    return entity
