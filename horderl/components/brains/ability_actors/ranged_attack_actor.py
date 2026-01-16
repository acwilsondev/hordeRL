from dataclasses import dataclass

from engine import constants
from engine.components import EnergyActor
from horderl.components.brains.brain import Brain


@dataclass
class RangedAttackActor(Brain):
    """
    Brain for ranged attack targeting.

    Input handling is delegated to the brain system.
    """

    energy_cost: int = EnergyActor.INSTANT
    target: int = 0
    shoot_ability: int = constants.INVALID
