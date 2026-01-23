"""System for debug painter placement actions."""

from typing import Callable, Dict, Tuple

from engine.components import Coordinates
from engine.logging import get_logger
from horderl.components.brains.painters.painter_brain import (
    PainterBrain,
    PainterTool,
)
from horderl.content.enemies.juvenile import make_juvenile
from horderl.content.getables.gold import make_gold_nugget

PaintFactory = Callable[[int, int], Tuple[int, list]]

_PAINT_TOOL_FACTORIES: Dict[PainterTool, PaintFactory] = {
    PainterTool.GOLD: make_gold_nugget,
    PainterTool.HORDELING: make_juvenile,
}


def paint_at_cursor(scene, painter: PainterBrain) -> None:
    """
    Paint a debug entity at the painter's cursor position.

    Args:
        scene: Active scene containing a component manager.
        painter: Painter brain component storing the tool selection and cursor.

    Side effects:
        - Adds spawned entity components to the scene component manager.
        - Logs warnings when the cursor or tool selection is invalid.
    """
    logger = get_logger(__name__)
    coords = scene.cm.get_one(Coordinates, entity=painter.cursor)
    if not coords:
        logger.warning(
            "Painter cursor missing",
            extra={"entity": painter.entity, "cursor": painter.cursor},
        )
        return

    factory = _PAINT_TOOL_FACTORIES.get(painter.tool_type)
    if not factory:
        logger.warning(
            "Painter tool type unsupported",
            extra={"entity": painter.entity, "tool": painter.tool_type},
        )
        return

    _, components = factory(coords.x, coords.y)
    scene.cm.add(*components)
