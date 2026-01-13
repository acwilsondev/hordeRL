from engine import core
from engine.components import Coordinates
from engine.components.entity import Entity
from engine.constants import PRIORITY_HIGH

from .. import palettes
from ..components import Appearance


def make_breadcrumb(x, y):
    entity_id = core.get_id()
    return (
        entity_id,
        [
            Entity(id=entity_id, entity=entity_id, name="breadcrumb"),
            Coordinates(
                entity=entity_id,
                x=x,
                y=y,
                priority=PRIORITY_HIGH,
                buildable=True,
            ),
            Appearance(
                entity=entity_id,
                symbol="o",
                color=palettes.GOLD,
                bg_color=palettes.BACKGROUND,
                render_mode=Appearance.RenderMode.HIGH_VEE,
            ),
        ],
    )
