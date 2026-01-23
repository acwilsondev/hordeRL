from dataclasses import dataclass
from enum import Enum

from engine import constants
from engine.components import EnergyActor
from horderl.components.brains.brain import Brain


class PainterTool(Enum):
    """
    Supported debug painter tool selections.
    """

    GOLD = "gold"
    HORDELING = "hordeling"


@dataclass
class PainterBrain(Brain):
    """
    Provide a base class for debug object placing controllers.
    """

    energy_cost: int = EnergyActor.INSTANT
    cursor: int = constants.INVALID
    tool_type: PainterTool = PainterTool.GOLD
