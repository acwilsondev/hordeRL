from dataclasses import dataclass

from horderl.components.brains.brain import Brain


@dataclass
class PlayerDeadBrain(Brain):
    """
    Brain that handles input when the player is dead.

    Logic is handled by the brain system.
    """
