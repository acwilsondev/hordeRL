from dataclasses import dataclass

from horderl.engine.components.component import Component


@dataclass
class ThwackAction(Component):
    """
    Object to signal that the owner entity is thwacking.
    """

    pass
