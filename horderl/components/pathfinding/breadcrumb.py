from dataclasses import dataclass

from engine import constants
from engine.components.component import Component


@dataclass
class Breadcrumb(Component):
    """
    Represent a breadcrumb entity used for pathfinding visualization.

    Breadcrumbs are lightweight markers that belong to a tracked entity and
    are meant to be managed by the breadcrumb system.
    """

    owner: int = constants.INVALID
