from dataclasses import dataclass
from typing import Tuple

from engine import constants
from engine.components import EnergyActor


@dataclass
class TunnelToPoint(EnergyActor):
    """
    Instance of a live attack.
    """

    target: int = constants.INVALID
    point: Tuple[int, int] = (0, 0)
