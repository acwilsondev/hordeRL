from dataclasses import dataclass

from engine import constants
from engine.components import EnergyActor


@dataclass
class Brain(EnergyActor):
    """
    Store stack metadata for active brain components.

    This class only tracks the previous brain component ID and does not
    mutate the scene directly.
    """

    # Establish a brain stack
    old_brain: int = constants.INVALID
