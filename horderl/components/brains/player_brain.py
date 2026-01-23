from dataclasses import dataclass

from horderl.components.brains.brain import Brain


@dataclass
class PlayerBrain(Brain):
    """
    Brain for player-controlled input.

    Behavior lives in brain systems; this component stores state.
    """
