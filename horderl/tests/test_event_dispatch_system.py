import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.component_manager import ComponentManager
from engine.components.component import Component
from engine.components.events import Event
from horderl.systems.event_dispatch_system import run as run_event_dispatch


class DummyScene:
    """Minimal scene stub exposing a component manager."""

    def __init__(self) -> None:
        """Initialize the scene with a component manager."""
        self.cm = ComponentManager()


@dataclass
class RecordedListener(Component):
    """Listener that records event notifications for verification."""

    notifications: list[int] = field(default_factory=list)

    def on_recorded(self, scene, caller: int) -> None:
        """Record the caller entity for assertions."""
        self.notifications.append(caller)


@dataclass
class RecordedEvent(Event):
    """Event that notifies RecordedListener components."""

    def listener_type(self):
        """Return the listener type for this event."""
        return RecordedListener

    def notify(self, scene, listener: RecordedListener) -> None:
        """Notify a listener with the event's entity."""
        listener.on_recorded(scene, self.entity)


def test_event_dispatch_system_notifies_listeners_and_removes_event():
    scene = DummyScene()
    listener = RecordedListener(entity=1)
    event = RecordedEvent(entity=2)
    scene.cm.add(listener, event)

    run_event_dispatch(scene)

    assert listener.notifications == [2]
    assert scene.cm.get(RecordedEvent) == []
