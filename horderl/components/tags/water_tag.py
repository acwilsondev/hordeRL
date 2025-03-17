from dataclasses import dataclass

from ..tags.tag import Tag


@dataclass
class WaterTag(Tag):
    value: str = "water"
    is_dirty: bool = False
