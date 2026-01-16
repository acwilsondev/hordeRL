import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.component_manager import ComponentManager
from engine.components.component import Component
from horderl.components.events.start_game_events import (
    GameStartListener,
    StartGame,
)
from horderl.systems.event_dispatch_system import run as run_event_dispatch


class DummyScene:
    """Minimal scene stub exposing a component manager."""

    def __init__(self) -> None:
        """Initialize the scene with a component manager."""
        self.cm = ComponentManager()


@dataclass
class RecordedListener(GameStartListener):
    """Listener that records event notifications for verification."""

    notifications: list[bool] = field(default_factory=list)

    def on_game_start(self, scene) -> None:
        """Record the game start notification for assertions."""
        self.notifications.append(True)


def test_event_dispatch_system_notifies_listeners_and_removes_event():
    scene = DummyScene()
    listener = RecordedListener(entity=1)
    event = StartGame(entity=2)
    scene.cm.add(listener, event)

    run_event_dispatch(scene)

    assert listener.notifications == [True]
    assert scene.cm.get(StartGame) == []
