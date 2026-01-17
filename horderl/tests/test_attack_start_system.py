import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.component_manager import ComponentManager
from horderl.components.ability_tracker import AbilityTracker
from horderl.components.events.attack_started_events import AttackStarted
from horderl.systems.attack_start_system import run as run_attack_start


class DummyScene:
    """Minimal scene stub exposing a component manager."""

    def __init__(self) -> None:
        """Initialize the scene with a component manager."""
        self.cm = ComponentManager()
        self.player = 1


def test_attack_start_system_resets_ability_tracker_and_clears_event():
    scene = DummyScene()
    tracker = AbilityTracker(entity=1, current_ability=3)
    event = AttackStarted(entity=1)
    scene.cm.add(tracker, event)

    run_attack_start(scene)

    assert tracker.current_ability == 0
    assert scene.cm.get(AttackStarted) == []
