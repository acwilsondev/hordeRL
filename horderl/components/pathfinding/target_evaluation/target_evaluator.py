from dataclasses import dataclass
from enum import Enum

from engine.components.component import Component


class TargetEvaluatorType(Enum):
    """Enumeration of target evaluation strategies."""

    HORDELING = "hordeling"
    HIGH_CROP = "high_crop"
    ALLY = "ally"


@dataclass
class TargetEvaluator(Component):
    """
    Data-only base component for pathfinding target evaluation.

    Systems interpret concrete subclasses to list candidate targets.
    """

    evaluator_type: TargetEvaluatorType = TargetEvaluatorType.HORDELING
