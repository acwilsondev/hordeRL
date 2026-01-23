import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.component_manager import ComponentManager
from horderl.components.die_on_attack_finished import DieOnAttackFinished
from horderl.components.events.attack_events import AttackFinished
from horderl.systems.die_on_attack_finished_system import (
    run as run_die_on_attack_finished_system,
)
from horderl.systems.event_system import run as run_event_system


class DummyScene:
    """Minimal scene stub exposing a component manager."""

    def __init__(self) -> None:
        """Initialize the scene with a component manager."""
        self.cm = ComponentManager()


def test_event_system_routes_attack_finished_events():
    scene = DummyScene()
    listener = DieOnAttackFinished(entity=1)
    event = AttackFinished(entity=1)
    scene.cm.add(listener, event)

    run_die_on_attack_finished_system(scene)
    run_event_system(scene)

    assert scene.cm.get(DieOnAttackFinished) == []
    assert scene.cm.get(AttackFinished) == []
