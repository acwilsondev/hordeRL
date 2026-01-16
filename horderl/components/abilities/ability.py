from dataclasses import dataclass

from engine import constants
from engine.components.component import Component

from ..enums import Intention


@dataclass
class Ability(Component):
    """
    Store data describing a player ability and its costs.
    """

    ability_title: str = ""
    ability_title_key: str | None = None
    unlock_cost: int = constants.INVALID
    use_cost: int = constants.INVALID
    intention: Intention = ""
