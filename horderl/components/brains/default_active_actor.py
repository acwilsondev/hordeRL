from dataclasses import dataclass

from engine import constants
from horderl.components.brains.brain import Brain


@dataclass
class DefaultActiveActor(Brain):
    """
    Brain that selects and pursues targets for active hostile actors.

    Responsible for acquiring a target, deciding whether to eat or attack, and
    moving toward the target using pathfinding or emergency tunneling.
    """

    target: int = constants.INVALID
    cost_map = None
