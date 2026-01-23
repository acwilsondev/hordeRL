from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class DallyEvent(Component):
    """
    Emitted when the owning entity dallies.
    """


class DallyListener(Component):
    """
    Marker component for entities that react to dally events.
    """
