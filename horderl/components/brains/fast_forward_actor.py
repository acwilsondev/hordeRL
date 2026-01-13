from dataclasses import dataclass

import tcod

from engine import core
from horderl.components.brains.brain import Brain
from horderl.components.enums import Intention
from horderl.components.events.attack_started_events import AttackStartListener


@dataclass
class FastForwardBrain(Brain, AttackStartListener):
    def on_attack_start(self, scene):
        self.back_out(scene)

    def act(self, scene):
        self.handle_key_event(scene, KEY_ACTION_MAP)

    def handle_key_event(self, scene, action_map):
        key_event = core.get_key_event()
        if key_event:
            self._log_debug(f"received input {key_event}")
            key_code = key_event.sym
            intention = action_map.get(key_code, None)
            self._log_debug(f"translated {key_event} -> {intention}")
            if intention == Intention.BACK:
                self.back_out(scene)
                return
        else:
            self.intention = Intention.DALLY


KEY_ACTION_MAP = {
    tcod.event.KeySym.PERIOD: Intention.DALLY,
    tcod.event.KeySym.ESCAPE: Intention.BACK,
}
