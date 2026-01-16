from dataclasses import dataclass

from .ability import Ability


@dataclass
class NullAbility(Ability):
    """
    Represent a placeholder ability with no behavior.
    """

    ability_title: str = "No Abilities"
    ability_title_key: str = "ability.none"
    unlock_cost: int = 0
    use_cost: int = 0
