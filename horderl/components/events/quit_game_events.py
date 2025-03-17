from abc import ABC, abstractmethod
from dataclasses import dataclass

from horderl.components.base_components.component import Component
from horderl.components.base_components.events import Event
from horderl.components.serialization.save_game import SaveGame
from horderl.engine import GameScene

from ... import settings
from ...scenes.start_menu import get_start_menu


@dataclass
class QuitGameListener(Component, ABC):
    """
    Respond to a request to quit the game.
    """

    @abstractmethod
    def on_quit_game(self, scene):
        raise NotImplementedError("Must inherit listener")


class QuitGame(Event):
    """
    Signal an intent to quit the game.
    """

    def listener_type(self):
        return QuitGameListener

    def notify(self, scene: GameScene, listener) -> None:
        listener.on_quit_game(scene)
        scene.cm.delete_component(self)

    def _after_remove(self, scene: GameScene) -> None:
        if settings.AUTOSAVE:
            SaveGame().act(scene)
        scene.pop()
        scene.controller.push_scene(get_start_menu())
