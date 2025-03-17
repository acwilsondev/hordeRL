from dataclasses import dataclass

from ..tags.tag import Tag


@dataclass
class CorpseTag(Tag):
    value: str = "corpse"
