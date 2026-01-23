from dataclasses import dataclass, field
from typing import List, Tuple

from engine.components.component import Component


@dataclass
class BreadcrumbTracker(Component):
    """
    Store breadcrumb visualization data for an entity.

    This component is purely data-focused and keeps track of the breadcrumb
    entities and the most recently requested path for the owner entity.
    """

    breadcrumbs: List[int] = field(default_factory=list)
    path: List[Tuple[int, int]] = field(default_factory=list)
