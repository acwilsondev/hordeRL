import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.component_manager import ComponentManager
from horderl.components import Attributes
from horderl.components.season_reset_listeners.reset_health import ResetHealth
from horderl.components.season_reset_listeners.reset_season import ResetSeason
from horderl.systems.season_reset_system import run as run_season_reset


class DummyScene:
    """Minimal scene stub exposing a component manager and messaging."""

    def __init__(self) -> None:
        """Initialize the scene with a component manager."""
        self.cm = ComponentManager()
        self.messages = []

    def message(self, text, color=None):  # pragma: no cover - trivial stub
        self.messages.append((text, color))


def test_season_reset_system_resets_health_and_clears_event():
    scene = DummyScene()
    attributes = Attributes(entity=1, hp=3, max_hp=10)
    reset_health = ResetHealth(entity=2)
    event = ResetSeason(entity=3, season="Summer")
    scene.cm.add(attributes, reset_health, event)

    run_season_reset(scene)

    assert attributes.hp == attributes.max_hp
    assert scene.cm.get(ResetSeason) == []
