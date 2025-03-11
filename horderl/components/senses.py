from dataclasses import dataclass

from .. import settings
from ..components.base_components.component import Component


@dataclass
class Senses(Component):
    sight_radius: int = settings.TORCH_RADIUS
    dirty: bool = True
