from dataclasses import dataclass

from horderl.engine.components.component import Component


@dataclass
class Sellable(Component):
    value: int = 0
