from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class QuitGameListener(Component, ABC):
    """
    Respond to a request to quit the game.
    """

    @abstractmethod
    def on_quit_game(self, scene):
        raise NotImplementedError("Must inherit listener")


@dataclass
class QuitGame(Component):
    """
    Signal an intent to quit the game.
    """
