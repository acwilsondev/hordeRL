from engine import core
from engine.components import Coordinates
from engine.components.component import Component
from engine.components.entity import Entity
from engine.constants import PRIORITY_LOW
from horderl.components.relationships.owner import Owner

from .. import palettes
from ..components import Appearance
from ..components.animation_definitions.sequence_animation_definition import (
    SequenceAnimationDefinition,
)


def make_explosion(x, y):
    entity_id = core.get_id()
    components: list[Component] = [
        Entity(
            id=entity_id,
            entity=entity_id,
            name="explosion",
            description="The air has ignited here.",
        ),
        Coordinates(entity=entity_id, x=x, y=y, priority=PRIORITY_LOW),
        Appearance(
            entity=entity_id,
            symbol="*",
            color=palettes.WHITE,
            bg_color=palettes.BACKGROUND,
        ),
        SequenceAnimationDefinition(
            entity=entity_id,
            sequence=[(palettes.GOLD, "*"), (palettes.FRESH_BLOOD, "*")],
        ),
    ]
    return entity_id, components
