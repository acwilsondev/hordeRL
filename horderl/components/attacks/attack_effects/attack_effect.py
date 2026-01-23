from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict

from engine.components.component import Component


class AttackEffectType(str, Enum):
    """
    Canonical identifiers for attack effects used by combat systems.
    """

    NONE = ""
    KNOCKBACK = "knockback"


@dataclass
class AttackEffect(Component):
    """
    Data-only description of an attack effect applied by an attacker.
    """

    effect_type: AttackEffectType = AttackEffectType.NONE
    parameters: Dict[str, Any] = field(default_factory=dict)
