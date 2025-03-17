from dataclasses import dataclass

import tcod

from horderl.components.ability_tracker import AbilityTracker
from horderl.components.brains.brain import Brain
from horderl.components.enums import Intention
from horderl.components.events.quit_game_events import QuitGame
from horderl.components.events.show_help_dialogue import ShowHelpDialogue
from horderl.engine import core


@dataclass
class PlayerBrain(Brain):
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
            elif intention == Intention.BACK:
                scene.cm.add(QuitGame(entity=self.entity))
            elif intention is None:
                self._log_debug(f"found no useable intention")
                return
            else:
                self._log_debug(
                    f"deferred intention {intention} (usually for movement"
                    " intentions)"
                )
                self.intention = intention


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
