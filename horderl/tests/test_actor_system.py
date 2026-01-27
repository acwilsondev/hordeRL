from engine.component_manager import ComponentManager
from horderl.components.actors.bomb_actor import BombActor
from horderl.components.brains.player_brain import PlayerBrain
from horderl.systems.actor_system import get_active_actors


class DummyScene:
    def __init__(self):
        self.cm = ComponentManager()


def test_get_active_actors_excludes_brains():
    scene = DummyScene()
    bomb = BombActor(entity=1, next_turn_to_act=0)
    brain = PlayerBrain(entity=2, next_turn_to_act=0)
    scene.cm.add(bomb, brain)

    actors = get_active_actors(scene)

    assert actors == [bomb]
