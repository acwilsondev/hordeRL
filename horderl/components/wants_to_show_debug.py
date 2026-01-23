"""
Marker component for triggering the debug menu system.
"""

from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class WantsToShowDebug(Component):
    """
    Marker component that requests the debug menu to be displayed.

    The component is lightweight and contains no scene mutations. Systems
    are responsible for interpreting it and presenting the debug UI.
    """
