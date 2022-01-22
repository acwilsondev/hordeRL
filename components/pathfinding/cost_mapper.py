from abc import ABC, abstractmethod

from engine.base_components.component import Component


class CostMapper(Component, ABC):
    @abstractmethod
    def get_cost_map(self, scene):
        raise NotImplementedError("Cannot use abstract base class")
