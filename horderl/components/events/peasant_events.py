from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class PeasantAddedListener(Component):
    """
    Respond to peasants moving in.
    """


@dataclass
class PeasantAdded(Component):
    """
    Signal that a new peasant has moved in.
    """


@dataclass
class PeasantDiedListener(Component):
    """
    Respond to peasant death events.
    """


@dataclass
class PeasantDied(Component):
    """
    Signal that a peasant has died.
    """
