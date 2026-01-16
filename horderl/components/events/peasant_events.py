from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class PeasantAddedListener(Component, ABC):
    """
    Respond to peasants moving in.
    """

    @abstractmethod
    def on_peasant_added(self, scene):
        raise NotImplementedError()


@dataclass
class PeasantAdded(Component):
    """
    Signal that a new peasant has moved in.
    """


@dataclass
class PeasantDiedListener(Component, ABC):
    """
    Respond to peasant death events.
    """

    @abstractmethod
    def on_peasant_died(self, scene):
        raise NotImplementedError()


@dataclass
class PeasantDied(Component):
    """
    Signal that a peasant has died.
    """
