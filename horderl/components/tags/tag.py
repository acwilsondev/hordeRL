from dataclasses import dataclass

from horderl.engine.components.component import Component


@dataclass
class Tag(Component):
    value: str = ""
