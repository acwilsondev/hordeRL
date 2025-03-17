from dataclasses import dataclass

from ..tags.tag import Tag


@dataclass
class FarmTag(Tag):
    value: str = "farm"
