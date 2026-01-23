from engine import core
from engine.component_manager import ComponentManager
from horderl.components.events.start_game_events import StartGame
from horderl.components.serialization.load_game import LoadGame
from horderl.components.serialization.save_game import SaveGame
from horderl.components.world_building.world_parameters import WorldParameters
from horderl.systems.serialization_system import (
    run as run_serialization_system,
)


class DummyScene:
    def __init__(self):
        self.cm = ComponentManager()
        self.messages = []
        self.saved = []
        self.loaded = []

    def save_game(self, data, filename, extra) -> None:
        self.saved.append((data, filename, extra))

    def load_game(self, filename):
        self.loaded.append(filename)
        loaded_component = WorldParameters(
            entity=core.get_id("world"), world_name="Loaded World"
        )
        return {
            "active_components": {loaded_component.id: loaded_component},
            "stashed_entities": {},
            "stashed_components": {},
        }

    def message(self, text, color=None) -> None:
        self.messages.append((text, color))


def test_serialization_system_saves_game_and_removes_request():
    scene = DummyScene()
    scene.cm.add(
        WorldParameters(entity=core.get_id("world"), world_name="My World")
    )

    scene.cm.add(SaveGame(entity=1, extra={"foo": "bar"}))

    run_serialization_system(scene)

    assert scene.cm.get(SaveGame) == []
    assert scene.saved[0][1] == "./My-World.world"
    assert scene.saved[0][2] == {"foo": "bar"}


def test_serialization_system_loads_game_and_restores_start_event():
    scene = DummyScene()

    scene.cm.add(LoadGame(entity=1, file_name="save.world"))
    scene.cm.add(StartGame(entity=1))

    run_serialization_system(scene)

    assert scene.loaded == ["save.world"]
    assert scene.cm.get(LoadGame) == []
    assert scene.cm.get(StartGame)
    assert scene.cm.get(WorldParameters)
