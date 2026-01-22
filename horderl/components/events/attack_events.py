from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class AttackFinished(Component):
    """
    Emitted after an entity's attack has been processed.
    """


@dataclass
class OnAttackFinishedListener(Component):
    """
    Respond to completed attacks.
    """
