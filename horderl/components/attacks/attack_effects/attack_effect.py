from abc import ABC, abstractmethod
from dataclasses import dataclass

from ...base_components.component import Component


@dataclass
class AttackEffect(Component, ABC):
    @abstractmethod
    def apply(self, scene, source, target):
        raise NotImplementedError("Attack effect apply must be implemented.")
