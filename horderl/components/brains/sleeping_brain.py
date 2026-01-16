from dataclasses import dataclass

from engine import constants, core
from engine.components import Coordinates, EnergyActor
from engine.logging import get_logger
from horderl.components.brains.brain import Brain
from horderl.components.events.peasant_events import PeasantDied
from horderl.components.stomach import Stomach
from horderl.content.states import sleep_animation
from horderl.systems import brain_stack


@dataclass
class SleepingBrain(Brain):
    """
    Brain that sleeps for a fixed number of turns.

    Responsible for consuming turns, spawning sleep animation, and transitioning
    back to the previous brain when the sleep counter expires.
    """

    turns: int = 3
    energy_cost: int = EnergyActor.HOURLY

    def act(self, scene):
        """
        Spend one sleep turn and handle wake-up transitions.

        Args:
            scene: Active scene providing access to components and messaging.

        Side Effects:
            - Adds sleep animation components each turn.
            - Consumes energy via pass_turn().
            - Pops the brain stack when turns are exhausted.
        """
        logger = get_logger(__name__)
        logger.debug(
            "Sleeping brain tick",
            extra={"entity": self.entity, "turns_remaining": self.turns},
        )
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
