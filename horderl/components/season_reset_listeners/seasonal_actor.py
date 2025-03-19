from abc import ABC, abstractmethod

from horderl.engine.components.component import Component


class SeasonResetListener(Component, ABC):
    @abstractmethod
    def on_season_reset(self, scene, season):
        raise NotImplementedError()
