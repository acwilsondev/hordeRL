from abc import ABC, abstractmethod
from dataclasses import dataclass

from .. import Coordinates
from ..base_components.component import Component
from ..enums import Intention
from ...content.states import no_money_animation
from horderl.engine import constants


@dataclass
class Ability(Component, ABC):
    """Represent a Player ability."""

    unlock_cost: int = constants.INVALID
    use_cost: int = constants.INVALID
    intention: Intention = ""

    @abstractmethod
    def use(self, scene, dispatcher):
        raise NotImplementedError("Must subclass Ability")

    def apply(self, scene, dispatcher):
        if scene.gold < self.use_cost:
            self._handle_no_money(scene)
            return
        self.use(scene, dispatcher)

    def _handle_no_money(self, scene):
        scene.warn("You can't afford to use that ability.")
        player_coords = scene.cm.get_one(Coordinates, entity=self.entity)
        confused_anim = no_money_animation(player_coords.x, player_coords.y)
        scene.cm.add(*confused_anim[1])
