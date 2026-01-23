from engine import core
from engine.component_manager import ComponentManager
from horderl.components.events.peasant_events import PeasantAdded, PeasantDied
from horderl.components.events.tree_cut_event import TreeCutEvent
from horderl.components.population import Population
from horderl.components.world_beauty import WorldBeauty
from horderl.components.world_building.world_parameters import WorldParameters
from horderl.systems.population_system import run as run_population_system
from horderl.systems.world_beauty_system import run as run_world_beauty_system


class DummyScene:
    def __init__(self) -> None:
        self.cm = ComponentManager()
        self.popup_messages = []
        self.pop_calls = 0
        self.messages = []

    def popup_message(self, message: str) -> None:
        self.popup_messages.append(message)

    def pop(self) -> None:
        self.pop_calls += 1

    def message(self, text: str, color=None) -> None:
        self.messages.append((text, color))


def test_population_system_updates_population_counts():
    scene = DummyScene()
    population = Population(entity=core.get_id("world"))
    scene.cm.add(population, PeasantAdded(entity=1))

    run_population_system(scene)

    assert population.population == 1
    assert scene.cm.get(PeasantAdded) == []


def test_population_system_ends_scene_when_population_hits_zero():
    scene = DummyScene()
    population = Population(entity=core.get_id("world"), population=1)
    scene.cm.add(population, PeasantDied(entity=1))

    run_population_system(scene)

    assert population.population == 0
    assert scene.popup_messages
    assert scene.pop_calls == 1
    assert scene.cm.get(PeasantDied) == []


def test_world_beauty_system_reacts_to_tree_cut():
    scene = DummyScene()
    world_id = core.get_id("world")
    listener = WorldBeauty(
        entity=world_id, trees_cut=0, spirits_wrath=0, spirits_attitude=1
    )
    scene.cm.add(
        listener,
        WorldParameters(entity=world_id, tree_cut_anger=2),
        TreeCutEvent(entity=1),
    )

    run_world_beauty_system(scene)

    assert listener.trees_cut == 1
    assert listener.spirits_wrath == 1
    assert listener.spirits_attitude == 1
    assert scene.messages
    assert scene.cm.get(TreeCutEvent) == []
