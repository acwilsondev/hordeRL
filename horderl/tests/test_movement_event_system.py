import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.component_manager import ComponentManager
from engine.components import Coordinates
from horderl import palettes
from horderl.components import Attributes
from horderl.components.actions.attack_action import AttackAction
from horderl.components.events.dally_event import DallyEvent
from horderl.components.events.die_events import Die
from horderl.components.events.step_event import EnterEvent, StepEvent
from horderl.components.movement.die_on_enter import DieOnEnter
from horderl.components.movement.drain_on_enter import DrainOnEnter
from horderl.components.movement.heal_on_dally import HealOnDally
from horderl.components.movement.pickup_gold import PickupGoldOnStep
from horderl.components.pickup_gold import GoldPickup
from horderl.systems.movement_event_system import run as run_movement_events


@dataclass
class RecordedMessage:
    """Record message text and color for assertions."""

    text: str
    color: tuple[int, int, int]


class DummyScene:
    """Minimal scene stub exposing a component manager and message log."""

    def __init__(self) -> None:
        self.cm = ComponentManager()
        self.gold = 0
        self.messages: list[RecordedMessage] = []

    def message(self, text: str, color: tuple[int, int, int]) -> None:
        self.messages.append(RecordedMessage(text=text, color=color))


def test_step_event_collects_gold_and_removes_event() -> None:
    scene = DummyScene()
    scene.cm.add(
        PickupGoldOnStep(entity=1),
        StepEvent(entity=1, new_location=(2, 3)),
        GoldPickup(entity=2, amount=7),
        Coordinates(entity=2, x=2, y=3),
    )

    run_movement_events(scene)

    assert scene.gold == 7
    assert scene.cm.get(GoldPickup) == []
    assert scene.cm.get(StepEvent) == []
    assert scene.messages == [
        RecordedMessage(text="You found 7 gold.", color=palettes.GOLD)
    ]


def test_enter_event_triggers_damage_and_death() -> None:
    scene = DummyScene()
    scene.cm.add(
        DrainOnEnter(entity=10, damage=3),
        DieOnEnter(entity=10),
        EnterEvent(entity=1, entered=10),
    )

    run_movement_events(scene)

    attacks = scene.cm.get(AttackAction)
    deaths = scene.cm.get(Die)

    assert scene.cm.get(EnterEvent) == []
    assert len(attacks) == 1
    assert attacks[0].entity == 10
    assert attacks[0].target == 1
    assert attacks[0].damage == 3
    assert len(deaths) == 1
    assert deaths[0].entity == 10
    assert deaths[0].killer == 1


def test_dally_event_heals_after_threshold() -> None:
    scene = DummyScene()
    scene.cm.add(
        HealOnDally(entity=5, count=1, heal_count=2),
        Attributes(entity=5, hp=2, max_hp=3),
        DallyEvent(entity=5),
    )

    run_movement_events(scene)

    attributes = scene.cm.get_one(Attributes, entity=5)
    healer = scene.cm.get_one(HealOnDally, entity=5)

    assert scene.cm.get(DallyEvent) == []
    assert attributes.hp == 3
    assert healer.count == 0
    assert scene.messages == [
        RecordedMessage(
            text="You rest and your wounds heal.", color=palettes.WHITE
        )
    ]
