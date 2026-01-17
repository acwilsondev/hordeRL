from dataclasses import dataclass
from typing import Tuple

from horderl import palettes
from horderl.components.events.attack_started_events import AttackStartListener


@dataclass
class GrowCrops(AttackStartListener):
    """Data-only marker for crops that grow at the start of an attack."""

    crop_color: Tuple = palettes.FIRE
