from dataclasses import dataclass

from horderl.engine.components.component import Component


@dataclass
class Material(Component):
    blocks: bool = False
    blocks_sight: bool = False
    indestructible: bool = False
