from dataclasses import dataclass

from ..tags.tag import Tag, TagType


@dataclass
class WaterTag(Tag):
    """Tag that marks water tiles and tracks contamination."""

    tag_type: TagType = TagType.WATER
    is_dirty: bool = False
