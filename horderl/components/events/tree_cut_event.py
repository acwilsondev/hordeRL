from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class TreeCutEvent(Component):
    """
    Emitted when a tree has been cut.
    """


class TreeCutListener(Component, ABC):
    """
    Respond to tree cut events.
    """

    @abstractmethod
    def on_tree_cut(self, scene):
        raise NotImplementedError()
