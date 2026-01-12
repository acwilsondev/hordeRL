from dataclasses import dataclass

from horderl.engine.components.component import Component


@dataclass
class Residence(Component):
    house_id: int = 0
