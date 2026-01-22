from dataclasses import dataclass, field
from typing import List, Tuple

from engine.components.component import Component


@dataclass
class BreadcrumbsRequested(Component):
    """
    Request breadcrumb updates for an entity path.

    Attributes:
        path (List[Tuple[int, int]]): Ordered path coordinates to visualize.
    """

    path: List[Tuple[int, int]] = field(default_factory=list)


@dataclass
class BreadcrumbsCleared(Component):
    """
    Request cleanup of breadcrumb entities for an owner.

    Attributes:
        breadcrumb_ids (List[int]): Entity IDs for breadcrumbs to remove.
    """

    breadcrumb_ids: List[int] = field(default_factory=list)
