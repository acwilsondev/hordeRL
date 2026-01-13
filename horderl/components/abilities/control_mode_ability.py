from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

from engine.core import log_debug

from ..abilities.ability import Ability
from ..animation_controllers.blinker_animation_controller import BlinkerAnimationController


@dataclass
class ControlModeAbility(Ability, ABC):
    @log_debug(__name__)
    def use(self, scene, dispatcher):
        sym, color = self.get_anim()
        mode = self.get_mode()
        new_controller = mode(entity=self.entity, old_brain=dispatcher)
        blinker = BlinkerAnimationController(
            entity=self.entity, new_symbol=sym, new_color=color
        )
        scene.cm.stash_component(dispatcher)
        scene.cm.add(new_controller, blinker)

    @abstractmethod
    def get_mode(self) -> Callable:
        pass

    @abstractmethod
    def get_anim(self):
        pass
