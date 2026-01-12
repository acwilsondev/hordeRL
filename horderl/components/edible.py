from dataclasses import dataclass

from horderl.engine.components.component import Component


@dataclass
class Edible(Component):
    sleep_for: int = 3
