from dataclasses import dataclass

from ..tags.tag import Tag


@dataclass
class PeasantTag(Tag):
    value: str = "peasant"
