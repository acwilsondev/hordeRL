import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.component_manager import ComponentManager
from horderl.components.abilities.build_wall_ability import BuildWallAbility
from horderl.components.abilities.debug_ability import DebugAbility
from horderl.components.abilities.null_ability import NullAbility
from horderl.components.ability_tracker import AbilityTracker
from horderl.systems.abilities import ability_selection_system


class DummyScene:
    """Minimal scene stub exposing a component manager."""

    def __init__(self) -> None:
        """Initialize the scene with a component manager."""
        self.cm = ComponentManager()


def test_ability_selection_cycles_through_abilities():
    scene = DummyScene()
    tracker = AbilityTracker(entity=1, current_ability=0)
    first = DebugAbility(entity=1)
    second = BuildWallAbility(entity=1)
    scene.cm.add(tracker, first, second)

    ability = ability_selection_system.get_current_ability(scene, tracker)
    assert isinstance(ability, DebugAbility)

    ability_selection_system.increment(scene, tracker)
    ability = ability_selection_system.get_current_ability(scene, tracker)
    assert isinstance(ability, BuildWallAbility)

    ability_selection_system.decrement(scene, tracker)
    ability = ability_selection_system.get_current_ability(scene, tracker)
    assert isinstance(ability, DebugAbility)


def test_ability_selection_returns_null_ability_when_empty():
    scene = DummyScene()
    tracker = AbilityTracker(entity=1, current_ability=0)
    scene.cm.add(tracker)

    ability = ability_selection_system.get_current_ability(scene, tracker)

    assert isinstance(ability, NullAbility)
