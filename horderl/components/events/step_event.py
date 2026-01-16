from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

from engine import constants
from engine.components.component import Component


@dataclass
class StepEvent(Component):
    """
    Emitted when the owning entity takes a step.
    """

    new_location: Tuple[int, int] = (-1, -1)


class StepListener(Component, ABC):
    """
    Trigger when the owning entity takes a step.
    """

    @abstractmethod
    def on_step(self, scene, point):
        raise NotImplementedError()


@dataclass
class EnterEvent(Component):
    """
    Emitted when the owning entity steps on another entity (if that entity cares).
    """

    entered: int = constants.INVALID


class EnterListener(Component, ABC):
    """
    Trigger when an entity steps on the owning entity.
    """

    @abstractmethod
    def on_enter(self, scene, stepper):
        raise NotImplementedError()
