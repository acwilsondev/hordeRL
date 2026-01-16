from dataclasses import dataclass

from engine import constants, core
from engine.components import Coordinates, EnergyActor
from engine.core import log_debug
from horderl.components.brains.brain import Brain
from horderl.components.events.peasant_events import PeasantDied
from horderl.components.stomach import Stomach
from horderl.content.states import sleep_animation
from horderl.systems import brain_stack


@dataclass
class SleepingBrain(Brain):
    turns: int = 3
    energy_cost: int = EnergyActor.HOURLY

    @log_debug(__name__)
    def act(self, scene):
        self._log_debug(f"sleeping one turn")
        coords = scene.cm.get_one(Coordinates, entity=self.entity)
        scene.cm.add(*sleep_animation(coords.x, coords.y)[1])
        self.pass_turn()
        if self.turns <= 0:
            brain_stack.back_out(scene, self)
        else:
            self.turns -= 1

    def _on_back_out(self, scene):
        stomach = scene.cm.get_one(Stomach, entity=self.entity)
        if stomach:
            if stomach.contents != constants.INVALID:
                self._log_debug(f"digested the peasant")
                scene.warn("A peasant has been lost!")
                scene.cm.add(PeasantDied(entity=core.get_id("world")))
            stomach.clear(scene)
