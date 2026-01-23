from dataclasses import dataclass, field
from typing import Any, Dict

from engine import constants
from engine.components.component import Component
from horderl.components.attacks.attack_effects.attack_effect import (
    AttackEffectType,
)


@dataclass
class AttackEffectResolution(Component):
    """
    Queue item describing an attack effect resolution between two entities.
    """

    source: int = constants.INVALID
    target: int = constants.INVALID
    effect_type: AttackEffectType = AttackEffectType.NONE
    parameters: Dict[str, Any] = field(default_factory=dict)
