from dataclasses import dataclass

from ..abilities.ability import Ability


@dataclass
class DebugAbility(Ability):
    """
    Describe the debug toggle ability configuration.
    """

    ability_title: str = "Show Debug"
    ability_title_key: str = "ability.debug"
    unlock_cost: int = 0
    use_cost: int = 0
