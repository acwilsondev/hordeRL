from dataclasses import dataclass

from horderl.engine.components.component import Component

from .. import settings


@dataclass
class Senses(Component):
    sight_radius: int = settings.TORCH_RADIUS
    dirty: bool = True
