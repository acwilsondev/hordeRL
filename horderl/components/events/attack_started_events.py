from dataclasses import dataclass

from engine.components.component import Component


class AttackStartListener(Component):
    """
    Marker component for attack start listeners.
    """


@dataclass
class AttackStarted(Component):
    """
    Emitted when the attack should begin.
    """
