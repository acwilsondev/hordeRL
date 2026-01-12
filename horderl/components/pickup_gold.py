from dataclasses import dataclass

from horderl.engine.components.component import Component


@dataclass
class GoldPickup(Component):
    amount: int = 10
