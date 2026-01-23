from dataclasses import dataclass

from engine import constants
from engine.components import EnergyActor
from horderl.components.brains.painters.painter_brain import (
    PainterBrain,
    PainterTool,
)


@dataclass
class PlaceHordelingController(PainterBrain):
    """
    Painter controller data for placing hordelings.
    """

    energy_cost: int = EnergyActor.INSTANT
    cursor: int = constants.INVALID
    tool_type: PainterTool = PainterTool.HORDELING
