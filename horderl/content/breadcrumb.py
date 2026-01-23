from engine import core
from engine.components import Coordinates
from engine.components.entity import Entity
from engine.constants import PRIORITY_HIGH

from .. import palettes
from ..components import Appearance
from ..components.pathfinding.breadcrumb import Breadcrumb


def make_breadcrumb(owner: int, x: int, y: int):
    """
    Build a breadcrumb entity and its components.

    Args:
        owner (int): Entity ID that owns the breadcrumb.
        x (int): X coordinate for the breadcrumb.
        y (int): Y coordinate for the breadcrumb.

    Returns:
        tuple[int, list]: Tuple of the new entity ID and its components.

    Side Effects:
        None.
    """
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
            Breadcrumb(entity=entity_id, owner=owner),
        ],
    )
