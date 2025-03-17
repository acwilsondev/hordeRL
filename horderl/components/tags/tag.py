from dataclasses import dataclass

from ..base_components.component import Component


@dataclass
class Tag(Component):
    value: str = ""
