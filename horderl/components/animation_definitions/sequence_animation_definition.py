from dataclasses import dataclass, field
from typing import List, Tuple

from .animation_definition import AnimationDefinition


@dataclass
class SequenceAnimationDefinition(AnimationDefinition):
    """
    Store a sequence of appearance steps for an entity animation.
    """

    timer_delay: int = 90
    sequence: List[Tuple] = field(default_factory=list)
    current_step: int = 0
