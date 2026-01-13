from abc import ABC, abstractmethod
from dataclasses import dataclass
from engine.components import Coordinates

from engine import constants
from engine.components.component import Component
from horderl.i18n import t

from ...content.states import no_money_animation
from ..enums import Intention


@dataclass
class Ability(Component, ABC):
    """
    Represent a Player ability.
    """

    unlock_cost: int = constants.INVALID
    use_cost: int = constants.INVALID
    intention: Intention = ""
    ability_title_key: str | None = None

    def __post_init__(self) -> None:
        if self.ability_title_key:
            self.ability_title = t(self.ability_title_key)

    @abstractmethod
    def use(self, scene, dispatcher):
        raise NotImplementedError("Must subclass Ability")

    def apply(self, scene, dispatcher):
        if scene.gold < self.use_cost:
            self._handle_no_money(scene)
            return
        self.use(scene, dispatcher)

    def _handle_no_money(self, scene):
        scene.warn(t("warning.no_money"))
        player_coords = scene.cm.get_one(Coordinates, entity=self.entity)
        confused_anim = no_money_animation(player_coords.x, player_coords.y)
        scene.cm.add(*confused_anim[1])
