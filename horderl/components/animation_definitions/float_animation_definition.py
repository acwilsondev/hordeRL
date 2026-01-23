from dataclasses import dataclass

from .animation_definition import AnimationDefinition


@dataclass
class FloatAnimationDefinition(AnimationDefinition):
    """
    Store the data needed to float an entity upward or rightward.
    """

    timer_delay: int = 125
    duration: int = 10
    delete_on_complete: bool = True
