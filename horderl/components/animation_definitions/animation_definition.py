from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class AnimationDefinition(Component):
    """
    Store shared timing and lifecycle state for animation definitions.
    """

    timer_delay: int = 0
    next_update: int = 0
    delete_on_complete: bool = False
    is_animating: bool = True
    started: bool = False
    stop_processed: bool = False
    remove_on_stop: bool = False
