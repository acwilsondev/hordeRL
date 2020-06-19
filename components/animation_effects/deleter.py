from dataclasses import dataclass, field

from engine.component import Component
from engine import core


@dataclass
class AnimationDeleter(Component):
    start: int = field(default_factory=core.time_ms)
    duration: int = 40
