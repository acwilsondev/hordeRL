from dataclasses import dataclass, field
from typing import Any, Dict

from engine import constants
from engine.components.component import Component


@dataclass
class AttackEffectResolution(Component):
    """
    Queue item describing an attack effect resolution between two entities.
    """

    source: int = constants.INVALID
    target: int = constants.INVALID
    effect_type: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
