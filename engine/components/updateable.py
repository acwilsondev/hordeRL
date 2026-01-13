from abc import ABC, abstractmethod
from dataclasses import dataclass

from engine.components.component import Component
from engine.game_scene import GameScene

"""
Updateable component for game entities that require periodic updates.

This module provides the base abstraction for any entity that needs to be
updated during the game loop. It lives in Engine Core as a foundational
primitive used across multiple game systems.
"""


@dataclass
class Updateable(Component, ABC):
    """Abstract base class for entities that require periodic updates.

    Responsibility:
        Define the contract for anything that needs to be notified during
        each game loop tick.

    This class is intentionally minimal—a focused interface following
    Interface Segregation. Concrete implementations decide what "update"
    means (AI, animation, state decay, etc.).
    """

    @abstractmethod
    def update(self, scene: GameScene, dt_ms: int) -> None:
        """Update entity state for the given time delta.

        Args:
            scene: The current game scene.
            dt_ms: Time elapsed since last update, in milliseconds.

        Side effects:
            - May modify internal state.
            - Should not trigger rendering or IO directly (keep core logic
              separate from side effects).
        """
        raise NotImplementedError()
