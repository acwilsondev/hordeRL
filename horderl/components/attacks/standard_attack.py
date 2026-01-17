from dataclasses import dataclass

from horderl.components.attacks.attack import Attack


@dataclass
class StandardAttack(Attack):
    """
    Data-only marker for a standard melee attack.
    """

    damage: int = 1
