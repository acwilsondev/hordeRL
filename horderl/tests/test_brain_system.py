from engine import constants
from engine.component_manager import ComponentManager
from engine.components import Coordinates
from horderl.components.brains.player_brain import PlayerBrain
from horderl.components.brains.sleeping_brain import SleepingBrain
from horderl.components.events.peasant_events import PeasantDied
from horderl.components.stomach import Stomach
from horderl.systems.brain_system import get_active_brains, handle_back_out


class DummyScene:
    def __init__(self):
        self.cm = ComponentManager()
        self.warn_messages = []

    def warn(self, message):
        self.warn_messages.append(message)


def test_get_active_brains_filters_by_energy():
    scene = DummyScene()
    active_brain = PlayerBrain(entity=1, energy=0)
    inactive_brain = PlayerBrain(entity=2, energy=-1)
    scene.cm.add(active_brain, inactive_brain)

    active = get_active_brains(scene)

    assert active == [active_brain]


def test_handle_back_out_cleans_sleeping_brain_stomach():
    scene = DummyScene()
    brain = SleepingBrain(entity=1)
    stomach = Stomach(entity=1, contents=2)
    scene.cm.add(brain, stomach, Coordinates(entity=2, x=0, y=0))
    scene.cm.stash_entity(2)

    handle_back_out(scene, brain)

    assert scene.warn_messages == ["A peasant has been lost!"]
    assert scene.cm.get(PeasantDied)
    assert stomach.contents == constants.INVALID
