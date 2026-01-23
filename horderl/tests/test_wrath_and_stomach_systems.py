from engine import constants
from engine.component_manager import ComponentManager
from engine.components.entity import Entity
from horderl.components.actors.hordeling_spawner import HordelingSpawner
from horderl.components.events.die_events import Die
from horderl.components.stomach import Stomach
from horderl.components.tags.tag import Tag, TagType
from horderl.components.wrath_effect import WrathEffect
from horderl.systems.stomach_system import clear_stomach, dump_stomach
from horderl.systems.wrath_system import run as run_wrath_system


class DummyScene:
    def __init__(self) -> None:
        self.cm = ComponentManager()
        self.player = 99


def test_wrath_system_purges_spawners_and_hordelings():
    scene = DummyScene()
    spawner_entity = 10
    hordeling_entity = 20
    scene.cm.add(
        HordelingSpawner(entity=spawner_entity),
        Tag(entity=hordeling_entity, tag_type=TagType.HORDELING),
        WrathEffect(entity=1),
    )

    run_wrath_system(scene)

    assert scene.cm.get(HordelingSpawner) == []
    assert scene.cm.get(WrathEffect) == []
    die_events = scene.cm.get(Die)
    assert [event.entity for event in die_events] == [hordeling_entity]


def test_stomach_system_clear_drops_stashed_entity():
    scene = DummyScene()
    stored_entity = 2
    stomach = Stomach(entity=1, contents=stored_entity)
    scene.cm.add(Entity(entity=stored_entity, name="snack"), stomach)
    scene.cm.stash_entity(stored_entity)

    clear_stomach(scene, stomach)

    assert stomach.contents == constants.INVALID
    assert stored_entity not in scene.cm.stashed_entities


def test_stomach_system_dump_unstashes_entity():
    scene = DummyScene()
    stored_entity = 3
    stomach = Stomach(entity=1, contents=stored_entity)
    scene.cm.add(Entity(entity=stored_entity, name="snack"), stomach)
    scene.cm.stash_entity(stored_entity)

    dump_stomach(scene, stomach)

    assert stomach.contents == constants.INVALID
    assert scene.cm.get_one(Entity, entity=stored_entity)
