from dataclasses import dataclass

from components.component import Component


@dataclass
class Attack(Component):
    damage: int = 1
