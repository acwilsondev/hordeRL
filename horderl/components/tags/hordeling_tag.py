from dataclasses import dataclass

from ..tags.tag import Tag


@dataclass
class HordelingTag(Tag):
    value: str = "hordeling"
