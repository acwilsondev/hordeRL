from engine.components import Actor

from ..components.enums import Intention
from ..components.serialization.save_game import SaveGame
from ..scenes.start_menu import get_start_menu
from ..systems.serialization_system import save_game


def run(scene):
    quitters = [
        b for b in scene.cm.get(Actor) if b.intention is Intention.BACK
    ]
    if quitters:
        if scene.config.autosave_enabled:
            save_game(scene, SaveGame(entity=scene.player))
        scene.pop()
        scene.controller.push_scene(get_start_menu())
