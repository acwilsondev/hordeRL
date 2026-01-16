from dataclasses import dataclass

from ..abilities.ability import Ability
from ..show_debug import WantsToShowDebug


@dataclass
class DebugAbility(Ability):
    ability_title: str = "Show Debug"
    ability_title_key: str = "ability.debug"
    unlock_cost: int = 0
    use_cost: int = 0

    def use(self, scene, dispatcher):
        scene.cm.add(WantsToShowDebug(entity=self.entity))
