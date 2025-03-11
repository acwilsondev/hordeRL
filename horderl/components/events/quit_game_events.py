from abc import ABC, abstractmethod
from dataclasses import dataclass

import settings
from components.base_components.component import Component
from components.base_components.events import Event
from components.serialization.save_game import SaveGame
from engine import GameScene
from scenes.start_menu import get_start_menu


@dataclass
class QuitGameListener(Component, ABC):
    """Respond to a request to quit the game."""

    @abstractmethod
    def on_quit_game(self, scene):
        raise NotImplementedError("Must inherit listener")


class QuitGame(Event):
    """Signal an intent to quit the game."""

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
