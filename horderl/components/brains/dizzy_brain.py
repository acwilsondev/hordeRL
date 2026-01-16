from dataclasses import dataclass

from horderl.components.brains.brain import Brain


@dataclass
class DizzyBrain(Brain):
    """
    Brain that randomizes movement while dizzy.

    Behavior is implemented in the brain system.
    """

    turns: int = 3
