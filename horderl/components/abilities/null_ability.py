from dataclasses import dataclass

from .ability import Ability


@dataclass
class NullAbility(Ability):
    ability_title: str = "No Abilities"
    ability_title_key: str = "ability.none"
    unlock_cost: int = 0
    use_cost: int = 0

    def use(self, scene, dispatcher):
        pass
