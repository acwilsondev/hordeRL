from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class ResetOwnerAnimationDefinition(Component):
    """
    Mark an entity whose owner should be reset when it is deleted.
    """
