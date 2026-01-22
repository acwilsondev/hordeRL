from dataclasses import dataclass

from engine import constants
from engine.components import EnergyActor
from horderl.components.brains.painters.painter_brain import (
    PainterBrain,
    PainterTool,
)


@dataclass
class PlaceGoldController(PainterBrain):
    """
    Painter controller data for placing gold nuggets.
    """

    energy_cost: int = EnergyActor.INSTANT
    cursor: int = constants.INVALID
    tool_type: PainterTool = PainterTool.GOLD
