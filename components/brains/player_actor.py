import logging
from dataclasses import dataclass

import tcod

from components import Coordinates
from components.ability_tracker import AbilityTracker
from components.enums import Intention
from components.brains.brain import Brain
from components.events.show_help_dialogue import ShowHelpDialogue
from components.states.dizzy_state import DizzyState
from content.states import confused_animation
from engine import core


@dataclass
class PlayerBrain(Brain):
    def act(self, scene):
        dizzy = scene.cm.get_one(DizzyState, entity=self.entity)
        if dizzy:
            core.get_key_event()
            if core.time_ms() > dizzy.next_turn:
                self.intention = Intention.DALLY
                dizzy.next_turn = core.time_ms() + 500
                dizzy.duration -= 1
                coords = scene.cm.get_one(Coordinates, entity=self.entity)
                scene.cm.add(*confused_animation(coords.x, coords.y)[1])
                if dizzy.duration <= 0:
                    scene.cm.delete_component(dizzy)
        else:
            self.handle_key_event(scene, KEY_ACTION_MAP)

    def handle_key_event(self, scene, action_map):
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
                self._log_debug(f"deferred intention {intention} (usually for movement intentions)")
                self.intention = intention

    def _handle_confused(self, scene):
        player_coords = scene.cm.get_one(Coordinates, entity=self.entity)
        confused_anim = confused_animation(player_coords.x, player_coords.y)
        scene.cm.add(*confused_anim[1])


KEY_ACTION_MAP = {
    tcod.event.K_e: Intention.NEXT_ABILITY,
    tcod.event.K_q: Intention.PREVIOUS_ABILITY,
    tcod.event.K_SPACE: Intention.USE_ABILITY,
    tcod.event.K_h: Intention.SHOW_HELP,

    tcod.event.K_UP: Intention.STEP_NORTH,
    tcod.event.K_DOWN: Intention.STEP_SOUTH,
    tcod.event.K_RIGHT: Intention.STEP_EAST,
    tcod.event.K_LEFT: Intention.STEP_WEST,
    tcod.event.K_PERIOD: Intention.DALLY,

    tcod.event.K_ESCAPE: Intention.BACK
}
