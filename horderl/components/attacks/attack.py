from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class Attack(Component):
    """
    Data-only base component for attacks.

    Systems interpret subclasses to queue attack actions and animations.
    """

    damage: int = 1
