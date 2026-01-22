from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class Delete(Component):
    """
    Add this to an entity to have it delete itself after some time.
    """

    next_update: int = 0
    energy: int = 0


@dataclass
class DeleteListener(Component):
    """
    A world building step.
    """
