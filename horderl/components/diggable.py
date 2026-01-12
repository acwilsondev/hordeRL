from dataclasses import dataclass

from horderl.engine.components.component import Component


@dataclass
class Diggable(Component):
    is_free: bool = False
    pass
