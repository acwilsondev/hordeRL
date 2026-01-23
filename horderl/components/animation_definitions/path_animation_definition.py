from dataclasses import dataclass

from .animation_definition import AnimationDefinition


@dataclass
class PathAnimationDefinition(AnimationDefinition):
    """
    Store the data needed to step an entity through a path.
    """

    timer_delay: int = 30
    delete_on_complete: bool = True
    current_step: int = 0
