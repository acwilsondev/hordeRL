import types

from horderl.engine.component_manager import ComponentManager
from horderl.engine.components.timed_actor import TimedActor
from horderl.systems import real_time


class DummyTimedActor(TimedActor):
    timer_delay = 500

    def act(self, scene) -> None:
        scene.acted += 1
        self.pass_turn()


def test_real_time_uses_dt_for_timed_actors():
    cm = ComponentManager()
    actor = DummyTimedActor(entity=1)
    cm.add(actor)

    scene = types.SimpleNamespace(cm=cm, acted=0)

    real_time.run(scene, 0.1)
    assert scene.acted == 1
    assert actor.current_time_ms == 100.0

    real_time.run(scene, 0.2)
    assert scene.acted == 1
    assert actor.current_time_ms == 300.0

    real_time.run(scene, 0.3)
    assert scene.acted == 2
    assert actor.current_time_ms == 600.0
