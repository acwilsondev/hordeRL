from dataclasses import dataclass

from horderl.engine.components.component import Component


@dataclass
class Owner(Component):
    owner: int = None
