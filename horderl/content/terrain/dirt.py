import random

from horderl.components import Appearance, Coordinates
from horderl.components.base_components.component import Component
from horderl.components.base_components.entity import Entity
from horderl.components.diggable import Diggable
from horderl.components.material import Material
from horderl.components.season_reset_listeners.grow_grass import GrowGrass
from horderl.engine import core, palettes
from horderl.engine.constants import PRIORITY_LOWEST


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
