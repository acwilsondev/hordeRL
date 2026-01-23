from dataclasses import dataclass

from engine import constants
from engine.components import EnergyActor


@dataclass
class EatAction(EnergyActor):
    """
    Instance of a live attack.
    """

    target: int = constants.INVALID
