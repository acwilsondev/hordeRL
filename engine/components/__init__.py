"""Stable component interfaces for external consumers.

Import component base classes and common concrete components from this module.
Other modules in :mod:`engine.components` are considered internal unless
explicitly re-exported here.
"""

from .actor import Actor
from .component import Component
from .coordinates import Coordinates
from .energy_actor import EnergyActor
from .entity import Entity

__all__ = [
    "Actor",
    "Component",
    "Coordinates",
    "EnergyActor",
    "Entity",
]
