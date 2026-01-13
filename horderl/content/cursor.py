from engine import core
from engine.components.entity import Entity
from engine.constants import PRIORITY_HIGH
from engine.components import Coordinates

from .. import palettes
from ..components import Appearance


def make_cursor(x, y):
    entity_id = core.get_id("cursor")
    return (
        entity_id,
        [
            Entity(id=entity_id, entity=entity_id, name="cursor"),
            Coordinates(
                entity=entity_id,
                x=x,
                y=y,
                priority=PRIORITY_HIGH,
                buildable=True,
            ),
            Appearance(
                entity=entity_id,
                symbol="X",
                color=palettes.GOLD,
                bg_color=palettes.BACKGROUND,
                render_mode=Appearance.RenderMode.HIGH_VEE,
            ),
        ],
    )
