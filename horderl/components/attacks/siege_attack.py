from dataclasses import dataclass

from horderl.components.attacks.attack import Attack


@dataclass
class SiegeAttack(Attack):
    """
    Data-only marker for attacks that deal bonus damage to structures.
    """

    damage: int = 1
    structure_multiplier: int = 5
