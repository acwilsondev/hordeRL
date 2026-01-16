from dataclasses import dataclass

from engine.components import EnergyActor

from .ability import Ability


@dataclass
class ThwackAbility(Ability, EnergyActor):
    """
    Describe the thwack ability configuration and counters.
    """

    ability_title: str = "Thwack"
    ability_title_key: str = "ability.thwack"
    unlock_cost: int = 0
    use_cost: int = 0
    count: int = 0
    max: int = 3
    is_recharging: bool = False
