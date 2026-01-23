from dataclasses import dataclass, field
from typing import List

from ..tags.tag import Tag, TagType


@dataclass
class IceTag(Tag):
    """Tag that marks frozen water tiles and tracks frozen state."""

    tag_type: TagType = TagType.ICE
    frozen_components: List[int] = field(default_factory=list)
    is_dirty: bool = False
