from horderl.components import Appearance, Coordinates
from horderl.components.animation_effects.reset_owner_animation import (
    ResetOwnerAnimation,
)
from horderl.components.events.delete_event import Delete
from horderl.components.relationships.owner import Owner
from horderl.engine import core, palettes
from horderl.engine.components.entity import Entity
from horderl.engine.constants import PRIORITY_HIGH

description = (
    "The farmer swings their tool. Being untrained in the ways of farmery, you"
    " don't know how this helps."
)


def farm_animation(owner, x, y):
    entity_id = core.get_id()
    return (
        entity_id,
        [
            Entity(
                id=entity_id,
                entity=entity_id,
                name="farm_animation",
                description=description,
            ),
            Appearance(
                entity=entity_id,
                symbol="/",
                color=palettes.STONE,
                bg_color=palettes.BACKGROUND,
            ),
            Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_HIGH),
            Owner(entity=entity_id, owner=owner),
            ResetOwnerAnimation(entity=entity_id),
            Delete(entity=entity_id, next_update=core.time_ms() + 300),
        ],
    )
