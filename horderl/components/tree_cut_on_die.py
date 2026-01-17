from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class TreeCutOnDeath(Component):
    """
    Signal that a tree has been cut down.
    """
