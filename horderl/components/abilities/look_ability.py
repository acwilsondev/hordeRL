from dataclasses import dataclass

from .ability import Ability


@dataclass
class LookAbility(Ability):
    """
    Describe the look-around ability configuration.
    """

    ability_title: str = "Look Around"
    ability_title_key: str = "ability.look"
    unlock_cost: int = 0
    use_cost: int = 0
