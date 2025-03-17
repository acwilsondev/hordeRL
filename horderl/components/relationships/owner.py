from dataclasses import dataclass

from ..base_components.component import Component


@dataclass
class Owner(Component):
    owner: int = None
