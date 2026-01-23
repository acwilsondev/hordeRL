from dataclasses import dataclass

from engine import constants
from engine.components import EnergyActor


@dataclass
class AttackAction(EnergyActor):
    """
    Instance of a live attack.
    """

    target: int = constants.INVALID
    damage: int = 0
