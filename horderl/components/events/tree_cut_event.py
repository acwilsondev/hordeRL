from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class TreeCutEvent(Component):
    """
    Emitted when a tree has been cut.
    """


@dataclass
class TreeCutListener(Component):
    """
    Respond to tree cut events.
    """
