from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class QuitGameListener(Component):
    """
    Respond to a request to quit the game.
    """


@dataclass
class QuitGame(Component):
    """
    Signal an intent to quit the game.
    """
