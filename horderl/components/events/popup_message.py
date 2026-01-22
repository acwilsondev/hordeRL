from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class PopupMessage(Component):
    """Event requesting a popup message."""

    next_update: int = 0
    message: str = ""
