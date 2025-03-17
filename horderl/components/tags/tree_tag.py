from dataclasses import dataclass

from ..tags.tag import Tag


@dataclass
class TreeTag(Tag):
    value: str = "tree"
