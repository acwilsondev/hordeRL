from dataclasses import dataclass

from engine.components.component import Component


@dataclass
class OnDieEmitPeasantDied(Component):
    """
    Translate a peasant death into a population count decrement.
    """
