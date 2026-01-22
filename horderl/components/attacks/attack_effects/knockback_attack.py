from dataclasses import dataclass, field

from horderl.components.attacks.attack_effects.attack_effect import (
    AttackEffect,
)


@dataclass
class KnockbackAttack(AttackEffect):
    """
    Data-only attack effect describing knockback behavior.
    """

    effect_type: str = "knockback"
    parameters: dict = field(default_factory=lambda: {"distance": 1})
