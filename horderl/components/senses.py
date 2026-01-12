from dataclasses import dataclass

from horderl.engine.components.component import Component

@dataclass
class Senses(Component):
    sight_radius: int = -1
    dirty: bool = True
