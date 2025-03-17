import random
from dataclasses import dataclass

import tcod

from horderl.components import Coordinates
from horderl.components.ability_tracker import AbilityTracker
from horderl.components.brains.brain import Brain
from horderl.components.enums import Intention
from horderl.components.events.show_help_dialogue import ShowHelpDialogue
from horderl.content.states import confused_animation
from horderl.engine import core


@dataclass
class DizzyBrain(Brain):
    turns: int = 3

    def act(self, scene):
        action_map = KEY_ACTION_MAP
        key_event = core.get_key_event()
        if key_event:
            self._log_debug(f"received input {key_event}")
            key_code = key_event.sym
            intention = action_map.get(key_code, None)
            self._log_debug(f"translated {key_event} -> {intention}")

            tracker = scene.cm.get_one(AbilityTracker, entity=self.entity)
            if intention == Intention.NEXT_ABILITY:
                tracker.increment(scene)
            elif intention == Intention.PREVIOUS_ABILITY:
                tracker.decrement(scene)
            elif intention == Intention.USE_ABILITY:
                ability = tracker.get_current_ability(scene)
                ability.apply(scene, self.id)
            elif intention == Intention.SHOW_HELP:
                scene.cm.add(ShowHelpDialogue(entity=self.entity))
            elif intention is None:
                self._log_debug(f"found no useable intention")
                return
            else:
                coords = scene.cm.get_one(Coordinates, entity=self.entity)
                scene.cm.add(*confused_animation(coords.x, coords.y)[1])
                self._log_debug(
                    f"deferred intention {intention} (usually for movement intentions)"
                )
                self._log_debug("taking a dizzy step")
                continuing_actor = (
                    self.back_out(scene) if self.turns <= 1 else self
                )
                self.turns -= 1
                continuing_actor.intention = random.choice(STEPS)


STEPS = [
    Intention.STEP_NORTH,
    Intention.STEP_SOUTH,
    Intention.STEP_EAST,
    Intention.STEP_WEST,
]

KEY_ACTION_MAP = {
    tcod.event.KeySym.e: Intention.NEXT_ABILITY,
    tcod.event.KeySym.q: Intention.PREVIOUS_ABILITY,
    tcod.event.KeySym.SPACE: Intention.USE_ABILITY,
    tcod.event.KeySym.h: Intention.SHOW_HELP,
    tcod.event.KeySym.UP: Intention.STEP_NORTH,
    tcod.event.KeySym.DOWN: Intention.STEP_SOUTH,
    tcod.event.KeySym.RIGHT: Intention.STEP_EAST,
    tcod.event.KeySym.LEFT: Intention.STEP_WEST,
    tcod.event.KeySym.PERIOD: Intention.DALLY,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
}
