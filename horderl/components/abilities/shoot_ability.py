from dataclasses import dataclass

from .ability import Ability


@dataclass
class ShootAbility(Ability):
    """
    Describe the ranged shoot ability configuration.
    """

    ability_title: str = "Shoot Bow"
    ability_title_key: str = "ability.shoot_bow"
    count: int = 5
    max: int = 5
    unlock_cost: int = 100
    use_cost: int = 5
