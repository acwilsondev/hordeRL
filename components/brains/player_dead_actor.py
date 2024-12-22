from dataclasses import dataclass

import tcod

from components import Coordinates
from components.ability_tracker import AbilityTracker
from components.enums import Intention
from components.brains.brain import Brain
from content.states import confused_animation
from engine import core


@dataclass
class PlayerDeadBrain(Brain):
    def act(self, scene):
        self.handle_key_event(scene, KEY_ACTION_MAP)

    def handle_key_event(self, scene, action_map):
        key_event = core.get_key_event()
        if key_event:
            self._log_debug(f"received input {key_event}")
            key_code = key_event.sym
            intention = action_map.get(key_code, None)
            self._log_debug(f"translated {key_event} -> {intention}")

            tracker = scene.cm.get_one(AbilityTracker, entity=self.entity)
            if intention is Intention.NEXT_ABILITY:
                tracker.increment(scene)
            elif intention is Intention.PREVIOUS_ABILITY:
                tracker.decrement(scene)
            elif intention is Intention.USE_ABILITY:
                ability = tracker.get_current_ability(scene)
                ability.apply(scene, self.id)
            elif intention is None:
                self._log_debug(f"found no useable intention")
                scene.warn("You urge your lifeless corpse to action, without much success.")
                return


KEY_ACTION_MAP = {
    tcod.event.KeySym.e: Intention.NEXT_ABILITY,
    tcod.event.KeySym.q: Intention.PREVIOUS_ABILITY,
    tcod.event.KeySym.SPACE: Intention.USE_ABILITY,
    tcod.event.KeySym.ESCAPE: Intention.BACK
}
