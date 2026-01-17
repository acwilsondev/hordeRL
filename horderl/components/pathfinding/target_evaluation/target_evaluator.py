from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class TargetEvaluator(Component):
    """
    Data-only base component for pathfinding target evaluation.

    Systems interpret concrete subclasses to list candidate targets.
    """
